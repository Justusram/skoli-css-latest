from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('provöversikt/<str:prov_title>/<str:prov_id>/', views.provPage, name='prov-page'),
    path('prov-läge-översikt/<str:prov_title>/<str:prov_id>/', views.provLägeÖversikt, name='prov-läge-översikt'),

    path('övningsbanken/', views.övningsBanken, name='övningar-page'),
    path('provbanken/', views.provbanken, name='provbanken-page'),
    
    
    path('prov-läge/<str:prov_title>/<str:prov_id>/<str:quiz_id>/', views.provLäge, name='prov-läge'),
    path('prov/<str:prov_title>/<str:prov_id>/<str:quiz_id>/', views.quizPage, name='quiz-page'),
    path('resultat/<str:prov_title>/<str:prov_id>/<str:quiz_id>/', views.resultPage, name='quiz-results'),
    path('prov-resultat/<str:prov_title>/<str:prov_id>/<str:quiz_id>/', views.provResultPage, name='prov-results'),
    
    

    
    
    
    
    
    path('create-data/', views.createData, name='create-data') 

]
