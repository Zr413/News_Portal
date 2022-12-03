from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView, TemplateView)
from .models import News, Author
from datetime import datetime
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import NewsForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q


class NewsList(ListView):
    model = News
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'articleviews'
    paginate_by = 3

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


class NewsDetail(DetailView):
    model = News
    template_name = 'new.html'
    context_object_name = 'art_views'


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


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


# class NewsSearch(ListView):
#     model = News
#     template_name = 'news_search.html'
#     context_object_name = 'articlesearch'
#
#     def get_queryset(self):
#         # Получаем не отфильтрованный кверисет всех моделей
#         queryset = News.objects.all()
#         q = self.request.GET.get("q")
#         if q:
#             return queryset.filter(Q(title__icontains=q) | Q(time__icontains=q) | Q(article_or_news__icontains=q))
#         return queryset


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


# class ContactFormView(News):
#     template_name = 'news_create.html'
#     form_class = ArticleNew
#     success_url = '/article/'
#
#     def form_valid(self, form):
#         self.objects = form.save(commit=False)
#         article_or_news = News.article_or_news
#         return super().form_valid(form)
