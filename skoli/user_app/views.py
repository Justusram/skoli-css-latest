from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login, logout
from base.models import Quiz

# Create your views here.


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        form = UserForm()
        
        existing_users = User.objects.all()
        
        
        #användare fyller i the form
        if request.method == 'POST':
            form = UserForm(request.POST)
            try:
                if form.is_valid:
                    #spara inputerade datan i rätt variabler, checka att allt stämmer först
                    user = form.save(commit=False)
                    
                    #spara lösenord, checka att de stämmer överens först
                    password1 = request.POST.get('password1')
                    # password2 = request.POST.get('password2')
                    
                    # if password1 != password2:
                    #     messages.error(request, 'Lösenorden stämmer inte överens')
                        
                    # elif password2 == password1:
                    password = password1
                    #spara lösenord END
                    
                    #spara e-post start:
                    for existing_user in existing_users:
                        if user.email == existing_user.email:
                            messages.error(request, 'E-postadress används redan')
                    #spara epost END
                            
                        else:
                            #skapa användare:
                            user = User.objects.create_user(
                                name=user.name.capitalize(),
                                email=user.email.lower(),
                                password=password
                            )
                            user.save()
                            login(request, user)
                            return redirect('home')
            
            except ValueError:
                pass
                    
    context = {'form': form}               
    return render(request, 'user_app/signup.html', context)
                        

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = None
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            
        except:
            messages.error(request, 'E-post hittades inte')
            
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Lösenord är felaktigt.")   
            
    return render(request, 'user_app/login.html')
            
            
def logoutPage(request):
    logout(request)
                        
    return redirect('home')
                


def profilePage(request):
    user = request.user
    name_lst = user.name.split(' ')
    first_name = name_lst[0]
    
    all_quizzes = Quiz.objects.all()
    pending_quizzes = user.pending_quizzes.all()
    completed_quizzes = user.completed_quizzes.all()
    
    context = {
        'user': user,  # Add this line to include the user in the context
        'first_name': first_name,
        'pending_quizzes': pending_quizzes,
        'all_quizzes': all_quizzes,
        'completed_quizzes': completed_quizzes
    }
    return render(request, 'user_app/profile.html', context)

