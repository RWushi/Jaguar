# Generated by Django 5.1.1 on 2024-09-10 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField(verbose_name='Номер')),
                ('question', models.TextField(verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
                ('category', models.CharField(choices=[('medical', 'Медицинская справка'), ('driving', 'Вождение'), ('theory', 'Теория'), ('internal_exam', 'Внутренние экзамены'), ('gibdd_exam', 'Экзамен в ГИБДД'), ('payment', 'Оплата услуг')], max_length=20, verbose_name='Категория')),
                ('city', models.CharField(choices=[('voronezh', 'Воронеж'), ('moscow', 'Москва'), ('spb', 'Санкт-Петербург')], max_length=20, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'db_table': 'questions',
            },
        ),
    ]