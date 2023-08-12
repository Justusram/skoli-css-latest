from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('question/<str:question_id>', views.questionRecive, name='question-api'),
    path('submit-answer/<str:submitted_choise_id>', views.submitAnswer, name='submitanswer-api'),
    path('next-question/<str:current_question_id>', views.nextQuestion, name='next-question-api'),
    path('last-question/<str:current_question_id>', views.backOneQuestion, name='last-question-api'),
    
    path('question-provläge/<str:question_id>', views.questionReciveProvläge, name='question-provläge-api'),
    path('submit-answer-provläge/<str:submitted_choise_id>', views.submitAnswerProvläge, name='submitanswerprovläge-api'),
    path('change-answer-provläge/<str:submitted_choise_id>', views.changeAnswerProvläge, name='submitanswerprovläge-api'),

    path('next-question-provläge/<str:current_question_id>', views.nextQuestionProvläge, name='next-question-provläge-api'),
    path('last-question-provläge/<str:current_question_id>', views.backOneQuestionProvläge, name='last-question-provläge-api'),
    

]