import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(
        random.randint(100000, 999999)
    )


def send_otp_email(email, otp, subject="Intela Group OTP"):

    message = (
        f"Your OTP is: {otp}\n\n"
        "This OTP is valid for 10 minutes."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )