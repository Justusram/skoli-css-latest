from django.urls import path
from . import views 

urlpatterns = [
    path('övningar/', views.övningar, name='alla-övningar'),
    path('övning/<str:övning_name>/<str:övning_id>', views.övningPage, name='övning-page')
    
    
]