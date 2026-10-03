from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType
from pydantic import BaseModel, EmailStr
from typing import List


app = FastAPI()

class UserRegistration(BaseModel):
   name:str
   address:str
   email:EmailStr
   age:int

users = []
# here the mail_username and mail_from is same basically it is the mail id of yours! and the password can be generated from your google account , search app password and generate new one
conf = ConnectionConfig(
   MAIL_USERNAME="username",
   MAIL_PASSWORD="password",
   MAIL_FROM="username@gmail.com",
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_FROM_NAME="Name",
   MAIL_STARTTLS=True,
   MAIL_SSL_TLS=False,
   USE_CREDENTIALS=True,
   VALIDATE_CERTS=True
)


async def send_mail(email:List[str]):
   html = """
<p>Hi!, Thank for Registration , our team will contact you soon
   """
   message = MessageSchema(
       subject="Registration Confirmation",
       recipients=email,
       body=html,
       subtype=MessageType.html
   )

   fm = FastMail(conf)
   await fm.send_message(message)
   return {"message": "email has been sent"}


@app.post("/register")
async def registration(data:UserRegistration):
   users.append(data)
   await send_mail([str(data.email)])

   return data