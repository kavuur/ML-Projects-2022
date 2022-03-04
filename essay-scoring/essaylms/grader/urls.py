from django.urls import path
# from django.conf.urls import urls

from grader import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.question, name='question'),
    path('<int:question_id>/essay<int:essay_id>/', views.essay, name='essay'),
]