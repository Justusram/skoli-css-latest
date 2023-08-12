from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from base.models import Prov, Question, Choise, Quiz 
from övning_app.models import Fråga, Övning



# Create your models here.
class MyUserManger(BaseUserManager):
    
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Du måste ange en korrekt e-post')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, name, password=None):
        
        user = self.create_user(
            email=email,
            name=name
            
        )
        
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user
    
    


class User(AbstractBaseUser):
    
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    
    
    #Övningsläge 
    pending_provs = models.ManyToManyField(Prov, related_name='pending_provs', blank=True)
    #se kommentar i slutet
    pending_quizzes = models.ManyToManyField(Quiz, related_name='pending_quizzes', blank=True)
    completed_quizzes =  models.ManyToManyField(Quiz, related_name='completed_quizzes', blank=True) # vänta med denna, nån variabel skapas i base/views.py för när resultatet är klart så sparas provet som completed_prov
    completed_questions = models.ManyToManyField(Question, related_name='completed_questions', blank=True)
    
    

    #Provläge
    all_questions_answered = models.ManyToManyField(Question, related_name='all_questions_answered', blank=True)
    correct_questions_answered = models.ManyToManyField(Question, related_name='correct_questions_answered', blank=True)
    completed_provläge_prov =  models.ManyToManyField(Prov, related_name='completed_provläge', blank=True)
    completed_provläge_quiz =  models.ManyToManyField(Prov, related_name='completed_provläge_quiz', blank=True)
    done_quiz = models.ManyToManyField(Quiz, related_name='done_quiz', blank=True)
    your_choise = models.ManyToManyField(Choise, related_name='your_choise', blank=True)
    
    
    
    #Övningar
    besvarade_frågor = models.ManyToManyField(Fråga, related_name='besvarade_frågor', blank=True)
    påbörjade_övningar =  models.ManyToManyField(Övning, related_name='påbörjade_övningar', blank=True)
    gjorda_övningar =  models.ManyToManyField(Övning, related_name='gjorda_övningar', blank=True)
    

    #Save restultat
    
    
    #end provläge
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = MyUserManger()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
   
   
# due to circular error, class User(AbstrectBaseUser) is found in base.models
    

    
    
    
    
    