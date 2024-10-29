from django.db import models

CATEGORY_CHOICES = (
    ('Медицинская справка', 'Медицинская справка'),
    ('Вождение', 'Вождение'),
    ('Теория', 'Теория'),
    ('Внутренние экзамены', 'Внутренние экзамены'),
    ('Экзамен в ГИБДД', 'Экзамен в ГИБДД'),
    ('Оплата услуг', 'Оплата услуг'))

CITY_CHOICES = (
    ('Воронеж', 'Воронеж'),
    ('Москва', 'Москва'),
    ('Санкт-Петербург', 'Санкт-Петербург'))


class Questions(models.Model):
    number = models.SmallIntegerField(verbose_name="Номер")
    question = models.TextField(verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="Категория")

    city = models.CharField(
        max_length=20,
        choices=CITY_CHOICES,
        verbose_name="Город")

    def __str__(self):
        return f"Вопрос №{self.number}"

    class Meta:
        db_table = 'questions'
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Statistics(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name="Вопрос")
    number = models.SmallIntegerField(verbose_name="Номер")

    operator_calls = models.SmallIntegerField(
        verbose_name="Вызов оператора",
        default=0,
        editable=False)

    clicks = models.SmallIntegerField(
        verbose_name="Число кликов",
        default=0,
        editable=False)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="Категория")

    city = models.CharField(
        max_length=20,
        choices=CITY_CHOICES,
        verbose_name="Город")

    date = models.DateField(verbose_name="Дата")

    class Meta:
        constraints = [models.UniqueConstraint(
                fields=['city', 'category', 'number', 'date'],
                name='unique_statistics')]
        db_table = 'statistics'
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"


class Reasons(models.Model):
    reason = models.TextField(verbose_name="Причина")

    class Meta:
        db_table = 'reasons'
        verbose_name = "Причина"
        verbose_name_plural = "Причины"
