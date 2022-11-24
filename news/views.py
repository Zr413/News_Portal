from django.views.generic import ListView, DetailView
from .models import News
from datetime import datetime


class ProductsList(ListView):
    model = News
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'articleviews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context


class ProductDetail(DetailView):
    model = News
    template_name = 'new.html'
    context_object_name = 'art_views'

