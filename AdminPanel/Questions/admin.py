from django.contrib import admin
from .models import Questions, Reasons


@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'category', 'city', 'question', 'answer')
    list_filter = ('city', 'category')


#@admin.register(Reasons)
#class ReasonAdmin(admin.ModelAdmin):
#    list_display = ('reason',)
