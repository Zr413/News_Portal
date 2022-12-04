from django import forms
from .models import News
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title',
            'article',
        ]

    # Валидация поля тема
    def clean(self):
        cleaned_data = super().clean()
        article = cleaned_data.get("article")
        if article is not None and len(article) < 3:
            raise ValidationError({
                "article": "Статья не может быть менее 10 символов."
            })

        title = cleaned_data.get("title")
        if title == article:
            raise ValidationError(
                "Текст темы и статьи не должны быть идентичны."
            )

        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Тема не должна начинаться со строчной буквы"
            )
        return title

    def clean_article(self):
        article = self.cleaned_data["article"]
        if article[0].islower():
            raise ValidationError(
                "Статья не должна начинаться со строчной буквы"
            )
        return article

# class ArtForm(forms.ModelForm):
#     class Meta:
#         model = News
#         fields = [
#             'title',
#             'article',
#             'article_or_news'
#         ]

# def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.fields["article_or_news"] = 'ARTICLE'  # будем отображать поле на странице как e-mail

# def clean_article_or_news(self):
#     cleaned_data = super().clean()
#     article_or_news = self.cleaned_data.get("article_or_news")
#     cleaned_data["article_or_news"] = article_or_news
#     return cleaned_data
