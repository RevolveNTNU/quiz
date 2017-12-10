from django.views.generic import ListView

from quiz.models import Question


class QuizView(ListView):
    template_name = 'index.html'
    model = Question
    context_object_name = 'questions'
