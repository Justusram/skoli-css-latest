from django.db import models



# Create your models here.




class Prov(models.Model): # Ma4 2013 HT
    title = models.CharField(max_length=100)
    
    
    
class Quiz(models.Model):
    prov = models.ForeignKey(Prov, related_name='quiz', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='question', on_delete=models.CASCADE)
    text = models.CharField(max_length=2500)
    question_count = models.IntegerField(blank=True, null=True)
    img = models.ImageField(blank=True)
    
    question_description_txt = models.CharField(max_length=200000, blank=True, null=True)
    question_description_img = models.ImageField(blank=True)
    # explanation = models.TextField()
    
    
class Choise(models.Model): #Svaren
    question = models.ForeignKey(Question, related_name='choise', on_delete=models.CASCADE, blank=True, null=True)
    header = models.CharField(max_length=15)# Bokstaven
    text = models.CharField(max_length=1500, blank=True)
    img = models.ImageField(blank=True)
    correct_answer = models.BooleanField(default=False)
    

    
    
    
    

    
    




    



    
    
