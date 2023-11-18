from django.core.mail import EmailMessage

def send_email(title, body, email_to):
    """
    Sends an email with the given title, body, and recipient email address.

    Parameters:
    - title (str): The title of the email.
    - body (str): The body of the email.
    - email_to (str): The recipient email address.

    Returns:
    None
    """
    email = EmailMessage(
        title,
        body,
        'jesusbryan155@gmail.com',
        [email_to]
    )
    email.send()