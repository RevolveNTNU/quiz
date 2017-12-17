from django.http import HttpResponseRedirect, HttpResponseBadRequest
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


class QuizCreateView(generic.View):

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        if not name:
            return HttpResponseBadRequest('Name is required')
        questions = request.POST.getlist('questions')
        quiz, _ = Quiz.objects.get_or_create(name=name)
        quiz.questions.set(questions)
        return HttpResponseRedirect(reverse('quiz', args=(name)))
