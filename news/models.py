from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# from django.core.validators import MinValueValidator
# from django.core.exceptions import ValidationError


# one_to_one_relation = models.OneToOneField(some_model)
# one_to_many_relation = models.ForeignKey(some_model)
# many_to_many_relation = models.ManyToManyField(some_model)

# Таблица с сущностью автора
class Author(models.Model):
    full_name = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    # Обновление рейтинга автора на основании лайков и дизлайков
    def update_rating(self):
        news_rat = News.objects.aggregate(rat_a=Sum('rating'))
        n_rat = news_rat.get('rat_a')

        comment_rat = Comment.objects.aggregate(rat_c=Sum('rating'))
        c_rat = comment_rat.get('rat_c')

        self.rating = n_rat * 3 + c_rat
        self.save()


# Промежуточная таблица для новостей и категорий
class NewsCategories(models.Model):
    new_key = models.ForeignKey('News', on_delete=models.CASCADE)
    cat_key = models.ForeignKey('Categories', on_delete=models.CASCADE)


# Категории
class Categories(models.Model):
    title = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.title.title()


# Новости
class News(models.Model):
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    title = models.CharField(max_length=50)
    article = models.TextField()
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новости'),
        (ARTICLE, 'Статья'),
    )
    article_or_news = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    new_cat = models.ManyToManyField(Categories, through='NewsCategories')
    rating = models.IntegerField(blank=False, default=0)

    # Время добавления
    def date(self):
        self.time = datetime.now()
        self.save()

    # Лайки и дизлайки новостей
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # Превью новости
    def preview(self):
        if len(self.article) > 124:
            return f'{self.article[:124]}...'
        return f'{self.article}'

    def __str__(self):
        # chars = ["*", "#", "%", "&", "?", "@"]
        # base_mat = ["хакер", "борода"]
        # value = self.article.lower().split(' ')
        #
        # for word in value:
        #     if word in base_mat:
        #         temp = random.sample(chars, len(word))
        #         i = ''.join(temp)
        #         value = [x.replace(word, i) for x in value]
        #
        # self.article = ' '.join(value)
        return f'{self.time.date()}, {self.title.title()}: {self.article}'


# STOP_LIST = [
#     'мат',
#     'мат',
#     'мат',
# ] , "#", "%", "&", "?", "@"


# Таблица с комментариями
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    rating = models.IntegerField(blank=False, default=0)

    # Время добавления
    def date(self):
        self.time = datetime.now()
        self.save()

    # Лайки и дизлайки новостей
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # def clean_text(self):
    #     text = self.cleaned_data['text']
    #     for word in STOP_LIST:
    #         if word in text:
    #             raise models.ValidationError("Вы позволили себе немного лишнего! Одумайтесь и исправьте текст!")
    #     self.save()

    # def serv(self, request):
    #     if request.method == 'POST':
    #         if request.POST.get('like'):
    #             self.like_comment()
    #         if request.POST.get('dislike'):
    #             self.dislike_comment()
    #
    #     return super(Author, self).serv(request)
