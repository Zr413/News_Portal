from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, NewsSearch

urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>/', NewsDetail.as_view(), name='news-details'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('search/', NewsSearch.as_view(), name='news_search'),
   # path('create/', ArticleCreate.as_view(), name='articcle_create'),
   # path('<int:pk>/edit/', ArticleUpdate.as_view(), name='articcle_edit'),
   # path('<int:pk>/delete/', ArticleDelete.as_view(), name='articcle_delete')
]

