# Generated by Django 4.1.3 on 2022-11-30 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactFormView',
            fields=[
                ('news_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='news.news')),
            ],
            bases=('news.news',),
        ),
    ]