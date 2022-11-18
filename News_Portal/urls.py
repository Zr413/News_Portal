"""News_Portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.contrib.auth.models import User
from django.urls import path
# from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
#
# from news import views
# from news.models import LikeDislike
# from news.models import News, Comment

urlpatterns = [
    path('admin/', admin.site.urls),
]

# app_name = 'ajax'
# urlpatterns = [
#     url(r'^article/(?P<pk>\d+)/like/$',
#         login_required(views.VotesView.as_view(model=News, vote_type=LikeDislike.LIKE)),
#         name='article_like'),
#     url(r'^article/(?P<pk>\d+)/dislike/$',
#         login_required(views.VotesView.as_view(model=News, vote_type=LikeDislike.DISLIKE)),
#         name='article_dislike'),
#     url(r'^comment/(?P<pk>\d+)/like/$',
#         login_required(views.VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE)),
#         name='comment_like'),
#     url(r'^comment/(?P<pk>\d+)/dislike/$',
#         login_required(views.VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE)),
#         name='comment_dislike'),
# ]
