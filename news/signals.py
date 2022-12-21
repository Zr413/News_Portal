from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from News_Portal import settings
from .models import Author, NewsCategories


User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.author = Author.objects.create(full_name=str(instance), user_id=instance.id)
    instance.author.save()


# @receiver(post_save, sender=News)
# def art_or_news_update(sender, instance, **kwargs):
#     if ArticleCreate():
#         instance.article_or_news = News.ARTICLE
#     else:
#         instance.article_or_news = News.NEWS


def send_notifications(preview, pk, title, subscribes):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribes,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=NewsCategories)
def notify_about_new_news(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.new_cat.all()
        subscribes: list[str] = []
        for cat in categories:
            subscribes += cat.subscribes.all()

        subscribes = [s.email for s in subscribes]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribes)
