from django.forms import ModelForm
from .models import Prov, Quiz, Question, Choise
        
        
class ProvForm(ModelForm):
    class Meta:
        model = Prov
        fields = '__all__'
        exclude = ('completed',)
        
        
class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ('img', 'question_count',)
        

        
        
        