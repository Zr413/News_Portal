from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
from django.contrib.contenttypes.fields import GenericRelation


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def articles(self):
        return self.get_queryset().filter(content_type__model='News').order_by('-articles__pub_date')

    def comments(self):
        return self.get_queryset().filter(content_type__model='Comment').order_by('-comments__pub_date')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


# one_to_one_relation = models.OneToOneField(some_model)
# one_to_many_relation = models.ForeignKey(some_model)
# many_to_many_relation = models.ManyToManyField(some_model)


class Author(models.Model):
    full_name = models.CharField(max_length=150)
    name = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def some_method(self):
        self.name = self.full_name.split()[0]
        self.save()


class News(models.Model):
    time = models.TimeField(auto_now=False, auto_now_add=True)
    title = models.CharField(max_length=50)
    article = models.TextField()
    article_or_news = models.BooleanField(default=True)
    news_reit = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Categories', through='NewsCategories')
    # likes = models.PositiveIntegerField(default=0)
    # user_likes = models.ManyToManyField(User)
    votes = GenericRelation(LikeDislike, related_query_name='News')

    def news_date(self):
        self.time = datetime.now()
        self.save()


class Categories(models.Model):
    title = models.CharField(max_length=250, unique=True)


class NewsCategories(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.TimeField(auto_now=False, auto_now_add=True)
    comment_reit = models.IntegerField(default=0)
    votes = GenericRelation(LikeDislike, related_query_name='Comment')

    def comment_date(self):
        self.time = datetime.now()
        self.save()
