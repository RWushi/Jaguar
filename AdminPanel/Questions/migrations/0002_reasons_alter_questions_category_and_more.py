# Generated by Django 5.1.1 on 2024-10-21 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reasons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(verbose_name='Причина')),
            ],
            options={
                'verbose_name': 'Причина',
                'verbose_name_plural': 'Причины',
                'db_table': 'reasons',
            },
        ),
        migrations.AlterField(
            model_name='questions',
            name='category',
            field=models.CharField(choices=[('Медицинская справка', 'Медицинская справка'), ('Вождение', 'Вождение'), ('Теория', 'Теория'), ('Внутренние экзамены', 'Внутренние экзамены'), ('Экзамен в ГИБДД', 'Экзамен в ГИБДД'), ('Оплата услуг', 'Оплата услуг')], max_length=20, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='city',
            field=models.CharField(choices=[('Воронеж', 'Воронеж'), ('Москва', 'Москва'), ('Санкт-Петербург', 'Санкт-Петербург')], max_length=20, verbose_name='Город'),
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField(verbose_name='Номер')),
                ('operator_calls', models.SmallIntegerField(default=0, editable=False, verbose_name='Вызов оператора')),
                ('clicks', models.SmallIntegerField(default=0, editable=False, verbose_name='Число кликов')),
                ('category', models.CharField(choices=[('Медицинская справка', 'Медицинская справка'), ('Вождение', 'Вождение'), ('Теория', 'Теория'), ('Внутренние экзамены', 'Внутренние экзамены'), ('Экзамен в ГИБДД', 'Экзамен в ГИБДД'), ('Оплата услуг', 'Оплата услуг')], max_length=20, verbose_name='Категория')),
                ('city', models.CharField(choices=[('Воронеж', 'Воронеж'), ('Москва', 'Москва'), ('Санкт-Петербург', 'Санкт-Петербург')], max_length=20, verbose_name='Город')),
                ('date', models.DateField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questions.questions')),
            ],
            options={
                'verbose_name': 'Статистика',
                'verbose_name_plural': 'Статистика',
                'db_table': 'statistics',
                'unique_together': {('city', 'category', 'question')},
            },
        ),
    ]
