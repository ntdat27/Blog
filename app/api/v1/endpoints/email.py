
from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from typing import List
from dotenv import load_dotenv
import mailtrap as mt
from app.core.config import Settings
import os

from app.models.email import EmailSchema

router = APIRouter()

@router.post("/send-mail")
def send_mail(email_request: EmailSchema):
    
    mail = mt.Mail(
    sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
    to=[mt.Address(email=email_request.email)],
    subject=email_request.subject,
    text=email_request.body,
    category="Integration Test",
)
    client = mt.MailtrapClient(token = "0b27180095cff0eb94571e0ea7d7d993")
    response = client.send(mail)
    return response