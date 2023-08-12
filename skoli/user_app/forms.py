from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserForm(forms.ModelForm):
    name = forms.CharField(max_length=30, label='Namn')
    email = forms.EmailField()
    
    password1 = forms.CharField(label='Lösenord', widget=forms.PasswordInput)

   
    class Meta:
        model = User
        fields = ['name', 'email', 'password1']
    
