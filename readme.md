# Запуск
# terminal_1
python manage.py runserver
# terminal_2
celery -A News_Portal worker -l INFO -P eventlet
# terminal_3
celery -A News_Portal beat -l INFO 