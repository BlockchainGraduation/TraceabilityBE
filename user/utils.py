import random
import string
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def generate_otp(length=6):
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp


def send_otp_email(email, otp):
    subject = "Your OTP for Login"
    message = f"Your OTP is: {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, f"SimpRaidenEi <{from_email}>", recipient_list)
