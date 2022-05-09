from django.contrib import admin
from .models import Subject, Question, Option, Response

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']


class OptionInline(admin.StackedInline):
    model = Option
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'subject', 'order', 'score', 'is_multiple', 'is_active']
    inlines = [OptionInline]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'is_correct', 'score']