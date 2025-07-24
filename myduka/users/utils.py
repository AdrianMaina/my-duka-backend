# =======================================================================
# FILE: myduka/users/utils.py (NEW)
# =======================================================================
from django.core.mail import send_mail
from django.conf import settings

def send_invite_email(email, invite_link):
    """
    Sends an invitation email to a new user using SendGrid.
    """
    subject = 'You have been invited to join MyDuka!'
    message = f"""
    Hello,

    You have been invited to join MyDuka.
    Please click the link below to create your account:
    {invite_link}

    This link will expire in 3 days.

    Thank you,
    The MyDuka Team
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Successfully sent invite email to {email}")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
