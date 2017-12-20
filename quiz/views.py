from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from quiz.models import Question, Tag, Quiz


class SearchView(generic.TemplateView):
    template_name = 'search.html'
    http_method_names = ['get']
    extra_context = {
        'tags': Tag.objects.all()
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(
            tags__in=request.GET.getlist('include')
        ).exclude(
            tags__in=request.GET.getlist('exclude')
        )
        return self.render_to_response(context)


class QuizView(generic.DetailView):
    template_name = 'quiz.html'
    model = Quiz


class QuizResultView(generic.DetailView):
    template_name = 'quiz_result.html'
    model = Quiz
    request = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['answered'] = [
                int(answer) for question, answer in self.request.POST.items()
                if question.isdigit() and answer.isdigit()
            ]
        return context

    def increment_answered(self, quiz):
        for question in quiz.questions.all():
            try:
                answer_pk = int(self.request.POST.get(str(question.pk)))
            except ValueError:
                break
            # Atomic incrementation
            question.answer_set.filter(pk=answer_pk).update(answered=F('answered') + 1)

    def post(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, pk=kwargs['pk'])
        self.increment_answered(quiz)
        return self.get(self, request, *args, **kwargs)


class QuizCreateView(generic.View):

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        if not name:
            return HttpResponseBadRequest('Name is required')
        questions = request.POST.getlist('questions')
        quiz, _ = Quiz.objects.get_or_create(name=name)
        quiz.questions.set(questions)
        return HttpResponseRedirect(reverse('quiz', args=(name)))
