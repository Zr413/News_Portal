from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, TemplateView)

import news
from .models import News, Author
from datetime import datetime
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import NewsForm
from django.http import HttpResponseRedirect
from django.shortcuts import render


# from django.db.models import Q

# Вывод списка новостей и статей
class NewsList(ListView):
    model = News
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'articleviews'
    paginate_by = 4

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['next_sale'] = None
        return context


# Вывод статьи или новости
class NewsDetail(DetailView):
    model = News
    template_name = 'new.html'
    context_object_name = 'art_views'


# Создание новости
class NewsCreate(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'news_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get(id=self.request.user.author.id)
        return super().form_valid(form) and HttpResponseRedirect('/news/')

    def create_news(request):
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/news/')

        return render(request, 'news_create.html', {'form': form})


# Обновление новости
class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


# Удаление новости
class NewsDelete(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


# Поиск по полям статей и новостей
class NewsSearch(ListView):
    model = News
    template_name = 'news_search.html'
    context_object_name = 'articlesearch'
    ordering = ['-time']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


# Создание статьи
class ArticleCreate(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'article_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get(id=self.request.user.author.id)
        self.object.article_or_news = News.ARTICLE
        return super().form_valid(form) and HttpResponseRedirect('/news/')

    def create_article(request):
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/news/')

        return render(request, 'article_create.html', {'form': form})


# Обновление статьи
class ArticleUpdate(UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'article_edit.html'


# Удаление статьи
class ArticleDelete(DeleteView):
    model = News
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')
