# Generated by Django 4.1.3 on 2023-01-26 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('rating', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, unique=True)),
                ('subscribes', models.ManyToManyField(related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('article', models.TextField()),
                ('article_or_news', models.CharField(choices=[('NW', 'Новости'), ('AR', 'Статья')], default='NW', max_length=2)),
                ('rating', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author')),
            ],
        ),
        migrations.CreateModel(
            name='NewsCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.categories')),
                ('new_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.news')),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='new_cat',
            field=models.ManyToManyField(through='news.NewsCategories', to='news.categories'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.news')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
