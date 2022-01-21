"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import include, path
from .views import QuizListApi, StartQuizApi, SubmitQuizApi, QuizDetailApi


def redirect_frontend_app(request):
    new_port = '8080'
    hostname = request.get_host().split(':')[0]
    url = 'http://' + hostname + ':' + new_port + '/'
    return redirect(url)


quiz_patterns = [
    path('', QuizListApi.as_view(), name='list'),
    path('<quiz_pass_id>/', QuizDetailApi.as_view(), name='detail'),
    path('<quiz_id>/start/', StartQuizApi.as_view(), name='start-quiz'),
    path('<quiz_pass_id>/submit/', SubmitQuizApi.as_view(), name='submit-quiz')
]

urlpatterns = [
    path('', redirect_frontend_app),
    path('admin/', admin.site.urls),
    path('quiz/', include((quiz_patterns, 'quiz'))),
]
