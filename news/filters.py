from django_filters import DateFilter
from django_filters import DateFromToRangeFilter
from django.forms import DateInput
from django_filters import FilterSet
from .models import News


# Создаем свой набор фильтров для модели News.
class NewsFilter(FilterSet):
    time = DateFromToRangeFilter(
        field_name='time',
        lookup_expr='qt',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'},
        ),
    )
    # label = 'tme',
    # empty_label = 'Введите значение'

    class Meta:
        model = News
        fields = {'title': ['icontains']}
