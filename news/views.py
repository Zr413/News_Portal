import logging
from datetime import datetime
from django.utils import timezone
import pytz  # Импортируем стандартный модуль для работы с часовыми поясами
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)

from .filters import NewsFilter
from .forms import NewsForm
from .models import News, Categories

logger = logging.getLogger(__name__)


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
        # context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['next_sale'] = None
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# Вывод статьи или новости
class NewsDetail(DetailView):
    logger.info("INFO")

    model = News
    template_name = 'new.html'
    context_object_name = 'art_views'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# Создание новости
class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    logger.info("INFO")

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Обновление новости
class NewsUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    logger.info("INFO")

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Удаление новости
class NewsDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    logger.info("INFO")

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Поиск по полям статей и новостей
class NewsSearch(ListView):
    logger.info("INFO")

    model = News
    template_name = 'news_search.html'
    context_object_name = 'articlesearch'
    ordering = ['-time']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# Создание статьи
class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    logger.info("INFO")

    permission_required = ('news.add_news',)
    raise_exception = True
    form_class = NewsForm
    model = News
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        form.instance.article_or_news = News.ARTICLE
        return super().form_valid(form) and HttpResponseRedirect('/')

    def create_article(request):
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')

        return render(request, 'article_create.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Обновление статьи
class ArticleUpdate(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    logger.info("INFO")

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Удаление статьи
class ArticleDelete(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    logger.info("INFO")

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# @login_required
# def upgrade_me(request):
#     user = request.user
#     premium_group = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         premium_group.user_set.add(user)
#     return redirect('/')

# Вывод всех категорий по выбранному значению
class CategoriListView(ListView):
    logger.info("INFO")

    model = News
    template_name = 'categori_list.html'
    context_object_name = 'categori_news_list'

    def get_queryset(self):
        self.new_cat = get_object_or_404(Categories, id=self.kwargs['pk'])
        queryset = News.objects.filter(new_cat=self.new_cat).order_by('-time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.new_cat.subscribes.all()
        context['new_cat'] = self.new_cat
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# Подписка на выбранную категорию новостей
@login_required
def subscrib(request, pk):
    user = request.user
    subscribes = Categories.objects.get(id=pk)
    subscribes.subscribes.add(user)

    message = 'Вы успешно подписались на категорию'
    return render(request, 'subscribe.html', {'categori': subscribes, 'message': message})
