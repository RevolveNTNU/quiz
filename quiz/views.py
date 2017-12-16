from django.views import generic

from quiz.models import Question, Tag


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
