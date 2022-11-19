from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
# from django.db.models import Sum
from django.contrib.auth.models import User


# one_to_one_relation = models.OneToOneField(some_model)
# one_to_many_relation = models.ForeignKey(some_model)
# many_to_many_relation = models.ManyToManyField(some_model)


class Author(models.Model):
    full_name = models.CharField(max_length=150)
    name = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_new = sum(News.objects.filter(author__news__article=self).values_list('rating', flat=True))
        rating_comment = sum(Comment.objects.filter(user__comment__news=self).values_list('rating', flat=True))
        rating_comment_news = sum(Comment.objects.filter(user__comment=self).values_list('rating', flat=True))
        self.rating = rating_new * 3 + rating_comment + rating_comment_news
        self.save()

    def some_method(self):
        self.name = self.full_name.split()[0]
        self.save()


class News(models.Model):
    time = models.TimeField(auto_now=False, auto_now_add=True)
    title = models.CharField(max_length=50)
    article = models.TextField()
    article_or_news = models.BooleanField(default=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Categories', through='NewsCategories')
    rating = models.IntegerField(blank=False, default=0)

    def news_date(self):
        self.time = datetime.now()
        self.save()

    def like_new(self):
        self.rating += 1
        self.save()

    def dislike_new(self):
        self.rating -= 1
        self.save()

    # def serv(self, request):
    #     if request.method == 'POST':
    #         if request.POST.get('like'):
    #             self.like_news()
    #         if request.POST.get('dislike'):
    #             self.dislike_news()
    #
    #     return super(News, self).serv(request)


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
    rating = models.IntegerField(blank=False, default=0)

    def comment_date(self):
        self.time = datetime.now()
        self.save()

    def like_comment(self):
        self.rating += 1
        self.save()

    def dislike_comment(self):
        self.rating -= 1
        self.save()

    # def serv(self, request):
    #     if request.method == 'POST':
    #         if request.POST.get('like'):
    #             self.like_comment()
    #         if request.POST.get('dislike'):
    #             self.dislike_comment()
    #
    #     return super(Author, self).serv(request)
