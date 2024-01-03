from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
import pyotp

from ticketwave import settings
from users.models import OneTimePassword

def generate_otp():
    totp = pyotp.TOTP('base32secret3232', interval=60)
    otp_code = totp.now()
    return otp_code

def send_code_to_user(email):
    subject = "OTP code for email verification"
    otp_code = generate_otp()
    user = get_user_model().objects.get(email)

    email_body = f'Hello, here is your requested otpcode {otp_code}. If you did not request this contact support'

    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, otp_code=otp_code)

    msg = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=from_email,
        to = [email]
    )

    msg.send(fail_silently=True)