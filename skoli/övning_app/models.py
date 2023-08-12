from django.db import models

# Create your models here.


class Övning(models.Model): #ORD ELF XYZ osv osv...
    name = models.CharField(max_length=100)


class Fråga(models.Model):
    Övning = models.ForeignKey(Övning, related_name='fråga', on_delete=models.CASCADE)
    text = models.CharField(max_length=2500)
    question_count = models.IntegerField(blank=True, null=True)
    img = None
    # explanation = models.TextField()
    
    
class Alternativ(models.Model): #Svaren
    question = models.ForeignKey(Fråga, related_name='alternativ', on_delete=models.CASCADE, blank=True, null=True)
    header = models.CharField(max_length=15)# Bokstaven
    text = models.CharField(max_length=1500, blank=True)
    img = models.ImageField(blank=True)
    correct_answer = models.BooleanField(default=False)