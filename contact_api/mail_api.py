import os
from fastapi import FastAPI
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# メール設定
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
TO_ADDRESS = os.getenv("TO_ADDRESS")

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/send")
def send_mail(data: ContactForm):

    body = f"""
名前: {data.name}
メール: {data.email}

お問い合わせ内容:
{data.message}
"""

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "お問い合わせフォームより"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = TO_ADDRESS
    msg["Date"] = formatdate()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)

        return {"status": "ok"}

    except Exception as e:
        print("Error:", e)
        return {"status": "error", "detail": str(e)}
