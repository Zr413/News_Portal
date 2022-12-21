from celery import shared_task
from django.shortcuts import render

from news.models import Categories


@shared_task
def subscrib(request, pk):
    user = request.user
    subscribes = Categories.objects.get(id=pk)
    subscribes.subscribes.add(user)

    message = 'Вы успешно подписались на категорию'
    return render(request, 'subscribe.html', {'categori': subscribes, 'message': message})
