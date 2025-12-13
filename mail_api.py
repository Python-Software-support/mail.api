import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
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
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
TO_ADDRESS = os.getenv("TO_ADDRESS")

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/send")
def send_mail(data: ContactForm):

    payload = {
        "from": "onboarding@resend.dev",
        "to": [TO_ADDRESS],
        "subject": "お問い合わせフォームより",
        "text": f"""名前: {data.name}
メール: {data.email}

お問い合わせ内容:
{data.message}
"""
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(
        "https://api.resend.com/emails",
        json=payload,
        headers=headers
    )

    if r.status_code == 200:
        return {"status": "ok"}
    else:
        return {"status": "error", "detail": r.text}