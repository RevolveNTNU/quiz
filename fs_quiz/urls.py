"""fs_quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from quiz.views import SearchView, QuizCreateView, QuizListView, QuizView, QuizResultView, QuestionCreateView

urlpatterns = [
    path('', SearchView.as_view()),
    path('create_quiz', QuizCreateView.as_view(), name='create_quiz'),
    path('create_question', QuestionCreateView.as_view(), name='create_question'),
    path('quiz', QuizListView.as_view(), name='quiz_list'),
    path('quiz/<slug:pk>', QuizView.as_view(template_name='quiz.html'), name='quiz'),
    path('quiz_old/<slug:pk>', QuizView.as_view(template_name='quiz_old.html'), name='quiz_old'),
    path('quiz_east/<slug:pk>', QuizView.as_view(template_name='quiz_east.html'), name='quiz_east'),
    path('quiz_result/<slug:pk>', QuizResultView.as_view(), name='quiz_result'),
    path('admin/', admin.site.urls),
]
