from django.contrib.auth.models import User
us1 = User.objects.create_user('user1')
us2 = User.objects.create_user('user2')


from news.models import *
auth1 = Author.objects.create(full_name='Иванов Иван Иванович', user_id=2)
auth2 = Author.objects.create(full_name='Сидоров Сидор Сидорович', user_id=3)

cat1 = Categories.objects.create(title='Новости экономики')
cat2 = Categories.objects.create(title='Новости IT технологий')
cat3 = Categories.objects.create(title='Новости бабки со скамейки')
cat4 = Categories.objects.create(title='киберпреступления сусликов')


news1 = News.objects.create(title='Хакер', article='Хакеры (Типичный хакер лохмат, бородат, способен часами разговаривать с отладчиком о чём-то им одним понятном… да что там часами — сутками напролёт, программирует в основном по ночам, предпочитая низкоуровневые языки, а также всяческую эзотерику вроде Лиспа. Ближайшей к хакерам разновидностью компьютерного специалиста является админ, противоположностью — погромист.', author_id=1)
news2 = News.objects.create(title='новость it', article_or_news=0, article='IT новость', author_id=1)
news3 = News.objects.create(title='Освоение марса', article_or_news=0, article='Пришлось продать луну клингонам', author_id=2)

News.objects.get(id=1).new_cat.add(Categories.objects.get(id=3))
News.objects.get(id=2).new_cat.add(Categories.objects.get(id=4))
News.objects.get(id=2).new_cat.add(Categories.objects.get(id=2))
News.objects.get(id=3).new_cat.add(Categories.objects.get(id=1))

comm1 = Comment.objects.create(text='Какойто комментарий', news_id=2, user_id=2)
comm2 = Comment.objects.create(text='Какойто комментарий', news_id=2, user_id=2)
comm3 = Comment.objects.create(text='Какойто комментарий', news_id=1, user_id=3)
comm4 = Comment.objects.create(text='Какойто комментарий', news_id=3, user_id=2)
comm5 = Comment.objects.create(text='Какойто комментарий', news_id=3, user_id=1)
comm6 = Comment.objects.create(text='Какойто комментарий', news_id=3, user_id=3)
comm7 = Comment.objects.create(text='Какойто комментарий', news_id=1, user_id=1)
comm8 = Comment.objects.create(text='это не те дроиды, что вы ищите', news_id=3, user_id=1)
comm9 = Comment.objects.create(text='sfddxfgfggmhkkjlj;', news_id=1, user_id=3)

comm10 = Comment.objects.create(text='это не те дроиды, что вы ищите', news=News.objects.get(id=2), user=Author.objects.get(id=1).user)
comm11 = Comment.objects.create(text='dfgsdfgsdfgsdfgsfgdfg', news=News.objects.get(id=3), user=Author.objects.get(id=3).user)



like = News.objects.get(id=2)
News.like(like)
Comment.objects.get(id=1).like()
Comment.objects.get(id=2).like()
Comment.objects.get(id=1).like()



pre = News.objects.all().order_by('-rating').values('time', 'author_id', 'rating', 'title', 'id')[0]

News.preview(News.objects.get(id=(pre.get('id'))))

Comment.objects.filter(user_id=(pre.get('author_id'))).values('time', 'user_id', 'rating', 'text')



Comment.objects.get(id=3).like()

a = Author.objects.get(id=1)
a.update_rating()
a.rating

pre = News.objects.all().order_by('-rating').values('time', 'author_id', 'rating', 'title', 'id')[0]

News.preview(News.objects.get(id=(pre.get('id'))))

Comment.objects.filter(user_id=(pre.get('author_id'))).values('time', 'user_id', 'rating', 'text')

Author.objects.all().order_by('-rating').values('full_name', 'rating')[0]