from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email, email_token):
    """Sends an activation email to the user"""
    subject = 'Please verify your account'
    email_from= settings.EMAIL_HOST_USER
    message = f'hi, please click in the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
    send_mail(subject,message,email_from,[email])

