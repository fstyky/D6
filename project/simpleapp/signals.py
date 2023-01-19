from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from project.project import settings
from project.project.settings import SITE_URL
from project.simpleapp.models import CategoryN

def send_notifications(preview, pk, title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
    {
        'text':preview,
        'link': f'{SITE_URL}/news/{pk}'
    }

    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email= settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=CategoryN)
def norify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories= instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

