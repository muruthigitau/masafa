from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_custom_email(subject, template_name, context, recipient_list, from_email=settings.DEFAULT_FROM_EMAIL, reply_email=settings.REPLY_EMAIL or settings.DEFAULT_FROM_EMAIL):
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        recipient_list,
        headers={'Reply-To': reply_email}
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

