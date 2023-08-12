from rest_framework import serializers
from base.models import Prov, Quiz, Question, Choise

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        
class ChoiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choise
        fields = '__all__'
        

class SubmitAnswerResponseSerializer(serializers.Serializer):
    submitted_answer = serializers.CharField()
    
