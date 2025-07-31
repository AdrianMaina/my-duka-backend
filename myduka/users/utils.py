# =======================================================================
# FILE: myduka/users/utils.py (EDITED FOR DEBUGGING)
# =======================================================================
from django.core.mail import send_mail
from django.conf import settings
import traceback

def send_invite_email(email, invite_link):
    """
    Sends an invitation email to a new user.
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

    # --- TEMPORARY DEBUGGING LOGS ---
    print("--- SENDING EMAIL DEBUG ---")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"SENDGRID_API_KEY IS SET: {bool(settings.SENDGRID_API_KEY)}")
    print(f"DEFAULT_FROM_EMAIL: {from_email}")
    print("Attempting to send mail...")
    print(email, type(email))
    print(f"recipient_list: {recipient_list}, type: {type(recipient_list)}")

# Should output something like: 'adrian@example.com' <class 'str'>

    # --- END DEBUGGING LOGS ---

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print("Successfully sent invite email instruction.")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")


def test_email():
    print("--- TESTING EMAIL ---")
    send_mail(
        subject="Test",
        message="This is a test",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["test@example.com"],
        fail_silently=False
    )

# =======================================================================
# ... (rest of the backend files are unchanged)
# =======================================================================
