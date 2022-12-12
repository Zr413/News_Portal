from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)

from .models import News, Author
from datetime import datetime
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import NewsForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)


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
class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news',)
    raise_exception = True
    form_class = NewsForm
    model = News
    template_name = 'news_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form) and HttpResponseRedirect('/')

    def create_news(request):
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')

        return render(request, 'news_create.html', {'form': form})


# Обновление новости
class NewsUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = ('news.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form) and HttpResponseRedirect('/')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.author == post.author:
            return True
        return False


# Удаление новости
class NewsDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = ('news.delete_news',)
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.author == post.author:
            return True
        return False


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
class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news',)
    form_class = NewsForm
    model = News
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        self.object.article_or_news = News.ARTICLE
        return super().form_valid(form) and HttpResponseRedirect('/')

    def create_article(request):
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')

        return render(request, 'article_create.html', {'form': form})


# Обновление статьи
class ArticleUpdate(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = ('news.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'article_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form) and HttpResponseRedirect('/')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.author == post.author:
            return True
        return False


# Удаление статьи
class ArticleDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = ('news.delete_news',)
    model = News
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.author == post.author:
            return True
        return False
