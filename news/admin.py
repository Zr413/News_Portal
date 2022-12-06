from django.contrib import admin
from .models import Categories, News, Author, Comment

admin.site.register(Categories)
admin.site.register(News)
admin.site.register(Author)
admin.site.register(Comment)
