from django.contrib.auth import get_user_model

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Author, NewsCategories
from .tasks import send_notifications

User = get_user_model()

# Создание имени автора по умолчанию от имени пользователя
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.author = Author.objects.create(full_name=str(instance), user_id=instance.id)
    instance.author.save()


# Отправка уведомления подписчику, в случае добавления новости
@receiver(m2m_changed, sender=NewsCategories)
def notify_about_new_news(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.new_cat.all()
        subscribes: list[str] = []
        for cat in categories:
            subscribes += cat.subscribes.all()

        subscribes = [s.email for s in subscribes]

        send_notifications.delay(instance.preview(), instance.pk, instance.title, subscribes)
