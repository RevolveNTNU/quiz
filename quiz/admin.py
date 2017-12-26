from django.contrib import admin

from quiz.models import Quiz, Question, Answer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    filter_horizontal = ['questions']


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuizAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']
    inlines = [AnswerInline]
