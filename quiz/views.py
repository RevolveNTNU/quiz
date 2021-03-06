from django.db import transaction
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from quiz.models import Question, Tag, Quiz, Answer


class SearchView(generic.TemplateView):
    template_name = 'search.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
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
            except TypeError:
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
        return HttpResponseRedirect(reverse('quiz', args=(name,)))


class QuestionCreateView(generic.ListView):
    template_name = 'createQuestion.html'
    model = Tag
    context_object_name = 'tags'
    question = None
    auto_included_tags = [Tag.objects.get_or_create(pk=tag)[0] for tag in [
        'team18',
        'not-verified'
    ]]

    def apply_tags(self, pk_extra_tags=None):
        for tag in self.auto_included_tags:
            tag.question_set.add(self.question)
        for tag in pk_extra_tags:
            tag, created = Tag.objects.get_or_create(pk=tag)
            tag.question_set.add(self.question)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        params = request.POST
        self.question = Question.objects.create(text=params['question'])
        self.apply_tags(pk_extra_tags=params.getlist('tags'))
        Answer.objects.create(text=params['answer'], question=self.question, correct=True)
        for option in params.getlist('incorrect-options'):
            Answer.objects.create(text=option, question=self.question, correct=False)
        return self.get(self, request, *args, **kwargs)
