from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
import pyotp
import random
from ticketwave import settings


def generate_key():
    # Generate TOTP secret key for the user
    i = random.randint(0,1000000)
    hotp = pyotp.HOTP(pyotp.random_base32())
    secret_key = hotp.secret
    hotp_code = hotp.at(i)

    return i, hotp_code, secret_key



def send_code_to_user(email):
    subject = "OTP code for email verification"
    i, hotp_code, secret_key = generate_key()
    user = get_user_model().objects.get(email=email)
    user.secret_key = str(i) + '-' + secret_key
    user.save()

    email_body = f'Hello, here is your requested otpcode {hotp_code}. If you did not request this contact support'

    from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=from_email,
        to = [email]
    )

    msg.send(fail_silently=True)