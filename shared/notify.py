from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.users.api.serializers import UserSerializer

def email_message_send(
    subject, 
    html_message, 
    to, 
    attachment=None,
):
    mail = EmailMessage(
        subject=subject,
        body=html_message,
        to=[to],
        from_email=settings.FROM_EMAIL,
    )
    mail.content_subtype = "html"
    if attachment is not None:
        mail.attach_file(attachment.file.path)
    mail.send()
    

def notify(
    user,
    subject,
    mail_template,
    attachment=None,
    *args,
    **kwargs
):
    context = {"user": UserSerializer(user).data}
    if "token" in kwargs:
        context["link"] = f'http://localhost:3000/pdf-help/auth/reset-password/{str(kwargs.get("token"))}'
    html_message = render_to_string(mail_template, context)
    email_message_send(
        subject=subject, 
        html_message=html_message, 
        to=user.email, 
        attachment=attachment
    )
