from django.contrib import admin
from django.utils.html import format_html
from datetime import datetime

class CustomDateRangeFilter(admin.SimpleListFilter):
    title = 'Пользовательский диапазон дат'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('custom', 'Выбрать диапазон'),
        )

    def queryset(self, request, queryset):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            try:
                # Преобразуем строки в объекты даты для корректной фильтрации
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                return queryset.filter(date__range=(start_date, end_date))
            except ValueError:
                pass  # Игнорируем ошибки преобразования

        return queryset

    def choices(self, changelist):
        query_string = changelist.get_query_string({}, [self.parameter_name])

        yield {
            'selected': changelist.params.get(self.parameter_name) == '',
            'query_string': query_string,
            'display': format_html(
                '<form method="get" action="{}" autocomplete="off">'
                '<input type="hidden" name="{}" value="custom" />'
                '<input type="date" name="start_date" placeholder="Начальная дата" /> '
                '<input type="date" name="end_date" placeholder="Конечная дата" /> '
                '<input type="submit" value="Фильтровать" />'
                '</form>',
                query_string,
                self.parameter_name,
            ),
        }
