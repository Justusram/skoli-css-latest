from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from . models import Prov, Quiz, Question, Choise
import time
import datetime
from django.http import JsonResponse




# Create your views here.

def home(request):
    
    alla_proven = Prov.objects.all()
    
    request.session['question_id'] = 0
    
    
    
    context = {'alla_proven': alla_proven}
    return render(request, 'base/home.html', context)


# ========== övningsläge:

def provPage(request, prov_title, prov_id):
    

    request.session['question_id'] = 0

    prov = Prov.objects.get(id=prov_id)
    quizzes = prov.quiz.all()
     
    
    context = {'prov': prov, 'quizzes': quizzes,}
    return render(request, 'base/prov-page.html', context)


@login_required(login_url='register-page')
def quizPage(request, prov_title, prov_id, quiz_id):

    #get all model objects
    
    
    user = request.user
    completed_questions = user.completed_questions.all()
    prov = Prov.objects.get(id=prov_id)  
    alla_quiz = prov.quiz.all()
    
    #byta quiz, från kvantitum 1 till kvantitum 2 t.ex
    if request.method == 'POST':
        formtype = request.POST.get('form-type')
        
        if formtype == 'click_quiz':
            quiz = Quiz.objects.get(id=quiz_id)
            questions = quiz.question.all()
            
            question_id = request.session['question_id'] = 0
            question = questions.first()
    
    
    #get the current id for question that is stored in session to do something with the id below
    question_id = request.session.get('question_id')
    
    #set dummy data so that if the if requierments are not fulfilled, we do not get a value error
    quiz = {'id': 0}
    question = None
    questions = []
    choises = []
    all_questions_completed = None
    question_correct_count = None
   

    # quiz_id is stored in the last url /quiz_id/ to get the current delprov the user visits 
    if int(quiz_id) > 0:
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.question.all()
        
     
        #if the id of the question does not exist in the session, create the session and set it to the first index of the questions list
        if question_id is None:
            question_id = request.session['question_id'] = 0
            question = questions.first()
            
            choises = question.choise.all()
     
        #if however, the id of question DOES exist in the session, get all the choises related to that question if there are any.
        else:
            try:
                question = questions[int(question_id)]
                choises = question.choise.all()
            
            
            
            #Gör så att när användare trycker på nästa vid sista fråga och idexerror uppstår, att om alla frågor har gjorts, så visas en bra jobbat sida:
            except IndexError:
   
                completed_questions = user.completed_questions.all()
                all_questions_completed = True
                
                for question in questions:
                    if question not in completed_questions:
                        all_questions_completed = False
            
            except ValueError:
                request.session['question_id'] = 0
                return redirect(request.path)
            
        #more dummydata
            
                
    
    
    #if the user triggers a post request
    if request.method == 'POST':
        formtype = request.POST.get('form-type')
        
        #logic for the user answer
        
        #check if answer is correct
        try:
            if formtype == 'answer-submission':
                

           
                
                answer = request.POST.get('answer')
                submitted_choise = question.choise.get(id=answer)
                
                if submitted_choise.correct_answer:
                    messages.success(request, 'Rätt, bra jobbat!')
                    
                    # Nästa fråga automatiskt när svaret är rätt: 
                    # request.session['question_id'] = question_id + 1
                    
                    #Spara frågan som gjord i användarmodellen
                    user.pending_quizzes.add(quiz)
                    user.completed_questions.add(question)
                    user.save()


                    #Get all the questions that the user has completed, so that we can check if a question is completed, in the html template
                    completed_questions = user.completed_questions.all()
                    return redirect(request.path)
            
                #if wrong answer, give error message
                else:
                    
                    
                    messages.error(request, 'Fel svar, försök igen')
                    
                    
                    
            elif formtype == 'answer-submission-last':
                
                answer = request.POST.get('answer')
                submitted_choise = question.choise.get(id=answer)
                

                if submitted_choise.correct_answer:
                    messages.success(request, 'Rätt, bra jobbat!')
                    
                    
                    # Nästa fråga automatiskt när svaret är rätt: 
                    # request.session['question_id'] = question_id + 1
                    
                    #Spara frågan som gjord i användarmodellen
                    
                    user.pending_quizzes.remove(quiz)
                    user.completed_quizzes.add(quiz)
                    user.completed_questions.add(question)
                    user.save()


                    #Get all the questions that the user has completed, so that we can check if a question is completed, in the html template
                    completed_questions = user.completed_questions.all()
                    return redirect(request.path)
            
                #if wrong answer, give error message
                else:
                    messages.error(request, 'Fel svar, försök igen')
                
                    
        except ObjectDoesNotExist:
            messages.error(request, 'du måste välja ett alternativ')
            
            

            

            
            
        
        #logic for Buttuns for navigating back forward through the quiz
        if formtype == 'back-one-question':
            
            request.session['question_id'] = question_id - 1
            return redirect(request.path)
                
               
        elif formtype == 'forward-one-question':
            request.session['question_id'] = question_id + 1
            return redirect(request.path)
        #end logic for navigating one-back-one-forward


        #button for resetting the test
        elif formtype == 'starta-om-prov':
            
            for question in questions:
                    user.completed_questions.remove(question)
                    user.save()
                    
                    completed_questions = user.completed_questions.all()
                
            del request.session['question_id']
            
            return redirect(request.path)
        
        
        # navigationbar, jump back and forth between all questions
        elif formtype == 'navigate-questions':
            question_identifier = request.POST.get('jump-question-link')
            question = Question.objects.get(id=question_identifier)
            
            for idx, i in enumerate(questions):
                if i == question:
                    question_id = idx
                    break 
                   
            request.session['question_id'] = int(question_id) 
            return redirect(request.path)
    

        
        
        
        
        
        elif formtype == 'nästa-del':
            
            request.session['question_id'] = 0
            return redirect('quiz-page', prov_title=prov.title, prov_id=prov.id, quiz_id=int(quiz_id) + 1)
        
    clicked = quiz.id 
    link_clicked = question.id  
        

            
    
    last_question = False      
    if question == questions.last():
        last_question = True
        
    first_question = False
    if question == questions.first():
        first_question = True
            
 
   
  
              
            
    
    context = { 

               'prov': prov, 
               'alla_quiz': alla_quiz,
               'quiz': quiz,
               'quiz_id': quiz_id,
               'question': question,
               'choises': choises,
               'question_id': question_id,
               'completed_questions': completed_questions,
               'all_questions_completed': all_questions_completed,
               'clicked': clicked,
               'link_clicked': link_clicked,
               'last_question': last_question,
               'first_question': first_question


               }
    return render(request, 'base/quiz_prov.html', context)



# ========== Provläge:



def provLägeÖversikt(request, prov_title, prov_id):
    
    prov = Prov.objects.get(id=prov_id)
    quizzes = prov.quiz.all()
    answered_questions = []  
    first_quiz = quizzes.first()
    request.session['question_id'] = 0

 
    
    context = {
        'prov': prov,
        'quizzes': quizzes,
        'first_quiz': first_quiz
    }
    return render(request, 'base/prov-läge-översikt.html', context)



@login_required(login_url='register-page')
def provLäge(request, prov_title, prov_id, quiz_id):
   
    user = request.user
    answered_questions = user.all_questions_answered.all()
    prov = Prov.objects.get(id=prov_id)  
    alla_quiz = prov.quiz.all()
    
    
    quiz = Quiz.objects.get(id=quiz_id)
    completed_quizzes = user.done_quiz.all()
    
    
    
    if quiz in completed_quizzes:
        return redirect('prov-läge', prov_title=prov.title, prov_id=prov.id, quiz_id=int(quiz_id) + 1)


    
    
    #get the current id for question that is stored in session to do something with the id below
    question_id = request.session.get('question_id')
    
    #set dummy data so that if the if requierments are not fulfilled, we do not get a value error
    quiz = {'id': 0}
    question = None
    questions = []
    choises = []
    current_yourchoise = None

    all_questions_answered = None
    last_question = False
    last_quiz = False
    

    # quiz_id is stored in the last url /quiz_id/ to get the current delprov the user visits 
    if int(quiz_id) > 0:
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.question.all()
        
 
        #if the id of the question does not exist in the session, create the session and set it to the first index of the questions list
        if question_id is None:
            question_id = request.session['question_id'] = 0
            question = questions.first()
            
            choises = question.choise.all()
     
        #if however, the id of question DOES exist in the session, get all the choises related to that question if there are any.
        else:
            try:
                question = questions[int(question_id)] 
                choises = question.choise.all()
 
   
            except IndexError:
                request.session['question_id'] = int(question_id) - 1
     

    
        #Current alternative
        for choise in choises:
            all_yourchoises = user.your_choise.all() #--hämta alla svar som användaren har skickat in
            if choise in all_yourchoises: #then chiose is the alternative that the user submitted earlier. Do something with the data:
                current_yourchoise = user.your_choise.get(id=choise.id) #--get the alternative that user has submitted
                
    
    clicked = question.id
    clicked_quiz = quiz.id
    
    #if the user triggers a post request
    if request.method == 'POST':
        formtype = request.POST.get('form-type')
        
        #viktigt att denna är innan ändra svar if statement nedan
        #kolla vilket av frågans alternativ som finns i all_youchoises. Detta indikerar att användaren valde just choise och submittade det ovan

        #logic for the user answer
        
        #check if answer is correct
        try:
            
            if formtype == 'answer-submission':
                
                answer = request.POST.get('answer')
                submitted_choise = question.choise.get(id=answer)
                
                #Spara användarens första svar, change kommer senare
                user.completed_provläge_quiz.add(prov)
                user.your_choise.add(submitted_choise)
                user.save()

    
                if submitted_choise.correct_answer == True:
                    
                    #Spara frågan som gjord rätt i användarmodellen
                    
                    user.correct_questions_answered.add(question)
                    user.all_questions_answered.add(question)
                    user.save()
                    
                    # Nästa fråga automatiskt när svaret är rätt: 


                    # request.session['question_id'] = question_id + 1
                    return redirect(request.path) 

                #if wrong answer, give error message
                elif submitted_choise.correct_answer == False:

                    user.all_questions_answered.add(question)
                    user.save()
                    
                    
                    # request.session['question_id'] = question_id + 1
                    return redirect(request.path)
                        # ändra svar    
                        
            #==================               
            elif formtype == 'answer-change':
                answer = request.POST.get('answer')
                submitted_choise = question.choise.get(id=answer)
                
                all_correct_questions = user.correct_questions_answered.all()
                
                #check again if the new value is correct
                if submitted_choise.correct_answer == True:
                    if question not in all_correct_questions:
                        user.correct_questions_answered.add(question)
                        user.save()

                if submitted_choise.correct_answer == False:
                    if question in all_correct_questions:
                        user.correct_questions_answered.remove(question)
                        user.save()
                
                #__________
                all_yourchoises = user.your_choise.all() #--hämta alla svar som användaren har skickat in
                answer = request.POST.get('answer')
                new_choise = question.choise.get(id=answer)
                
                
                
                for choise in choises:
                    if choise in all_yourchoises: #then chiose is the alternative that the user submitted earlier. Do something with the data:
                        
                        user.your_choise.remove(choise.id) #--remove the old alternative that user has submitted
                        user.save()
                        break
                
                
                user.your_choise.add(new_choise) #--add the new alternative 
                user.save()
                
                current_yourchoise = new_choise

                return redirect(request.path)
                
                #kolla vilket av frågans alternativ som finns i all_youchoises. Detta indikerar att användaren valde just choise och submittade det ovan
            
                    
            
            
            
            #logic for Buttuns for navigating back forward through the quiz
            elif formtype == 'back-one-question':
                
                request.session['question_id'] = question_id - 1
                return redirect(request.path)
                    
                
            elif formtype == 'forward-one-question':
                request.session['question_id'] = question_id + 1
                return redirect(request.path)
            #end logic for navigating one-back-one-forward
            
                    #navigationbar, jump back and forth between all questions
            
            elif formtype == 'navigate-questions':
                question_identifier = request.POST.get('jump-question-link')
                question = Question.objects.get(id=question_identifier)
                
                for idx, i in enumerate(questions):
                    if i == question:
                        question_id = idx
                        break 
                
                request.session['question_id'] = int(question_id) 
                return redirect(request.path)


                
        
         


                
                    
                            
            

        except ObjectDoesNotExist:
            messages.error(request, 'du måste välja ett alternativ')
  

        #Get alla svarade frågor så användaren ser vilka som är besvarade:
        answered_questions = user.all_questions_answered.all()     
            

    if question == questions.last():
        last_question = True
        
    if quiz == alla_quiz.last():
        last_quiz = True
    
    first_question = False
    if question == questions.first():
        first_question = True
        
    

    
    #render code
    context = { 

               'prov': prov, 
               'alla_quiz': alla_quiz,
               'quiz': quiz,
               'quiz_id': quiz_id,
               'question': question,
               'choises': choises,
               'question_id': question_id,
               'answered_questions': answered_questions,
               'current_yourchoise': current_yourchoise,
               'all_questions_answered': all_questions_answered,
               'last_question': last_question,
               'last_quiz': last_quiz,
               'clicked': clicked,
               'clicked_quiz': clicked_quiz



               }
    return render(request, 'base/prov-läge.html', context)




#===========ALLA RESULTAT FUNCTIONS=================================#
def resultPage(request, prov_title, prov_id, quiz_id):
    
    request.session['question_id'] = 0
    user = request.user
    answered_questions = user.all_questions_answered.all()
    prov = Prov.objects.get(id=prov_id)  
    alla_quiz = prov.quiz.all()
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.question.all()
    next_quiz_name = None
    
    #mark the quiz as completed, to create functionality to restrict the user to edit the quiz if he clicks back.
    user.done_quiz.add(quiz)
    user.completed_provläge_quiz.add(prov) #lägg in quiz i användarens gjorda quiz, så visas prov som påbörjat, sen kan även sidan blockeras
    user.save()

    all_correct_answers = user.correct_questions_answered.all()
    all_answers = user.all_questions_answered.all()
    quiz_correct_answers = []
    quiz_wrong_answers = []
    
    #Set value for next_quiz_id so that nästa provdel button will work
    quiz_index = None
    for index, q in enumerate(alla_quiz):
        if q.id == quiz.id:
            quiz_index = index
            break
    
    next_quiz_id = None
    if quiz_index is not None and quiz_index < len(alla_quiz) - 1:
        next_quiz = alla_quiz[quiz_index + 1]
        next_quiz_id = next_quiz.id
        next_quiz_name = next_quiz.name

            
    for question in all_answers:
        if question in questions: #så att endbart just detta quizzets frågor visas
            if question in all_correct_answers:
                quiz_correct_answers.append(question) #lägg till frågan som matchade i lista
                
            elif question not in all_correct_answers:
                quiz_wrong_answers.append(question) #lägg till frågan som matchade i lista
                  
    
    question_correct_count = len(quiz_correct_answers)
    
    context = {
        'question_correct_count': question_correct_count,
        'quiz_correct_answers': quiz_correct_answers,
        'quiz_wrong_answers': quiz_wrong_answers,
        'next_quiz_id': next_quiz_id,
        'prov': prov,
        'next_quiz_name': next_quiz_name,
        'quiz': quiz
        
    }
    return render(request, 'base/quiz-results.html', context)

def provResultPage(request, prov_title, prov_id, quiz_id):
    
    #Start of the last quizzs results:
    request.session['question_id'] = 0
    user = request.user
    answered_questions = user.all_questions_answered.all()
    prov = Prov.objects.get(id=prov_id)  
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.question.all()
    quizzes = prov.quiz.all()

    
    #mark the prov as completed, to create functionality to restrict the user to edit the quiz if he clicks back.
    user.completed_provläge_quiz.remove(prov)
    user.completed_provläge_prov.add(prov)
    user.save


    all_correct_answers = user.correct_questions_answered.all()
    all_answers = user.all_questions_answered.all()
    quiz_correct_answers = []
    quiz_wrong_answers = []
    

            
    for question in all_answers:
        if question in questions: #så att endbart just detta quizzets frågor visas
            if question in all_correct_answers:
                quiz_correct_answers.append(question) #lägg till frågan som matchade i lista
                
            elif question not in all_correct_answers:
                quiz_wrong_answers.append(question) #lägg till frågan som matchade i lista
                
  
                
    question_correct_count = len(quiz_correct_answers)
    #=====================================================================================================================================================#
    
    #Hämta alla frågor som är kopplade till provet:
    all_prov_questions = []
    for quiz in quizzes:
        quiz_questions = quiz.question.all()
        for question in questions:
            all_prov_questions.append(question)
            
            
    #Hämta quiz
    quiz_1 = quizzes[0]
    quiz_2 = quizzes[1]
    quiz_3 = quizzes[2]
    quiz_4 = quizzes[3]
    
    

    
    #Hämta alla frågor för vaje quiz:
    quiz_1_questions = quiz_1.question.all()
    quiz_2_questions = quiz_2.question.all()
    quiz_3_questions = quiz_3.question.all()
    quiz_4_questions = quiz_4.question.all()
            
    #Se hur många rätt respektive fel varje quiz hade    
    quiz_1_correct_count = 0
    quiz_2_correct_count = 0
    quiz_3_correct_count = 0
    quiz_4_correct_count = 0
    
    quiz_1_wrong_count = 0
    quiz_2_wrong_count = 0
    quiz_3_wrong_count = 0
    quiz_4_wrong_count = 0
    
    
    for question in quiz_1_questions:
        if question in all_correct_answers:
            quiz_1_correct_count += 1
        elif question not in all_correct_answers:
            quiz_1_wrong_count += 1      
    
    for question in quiz_2_questions:
        if question in all_correct_answers:
            quiz_2_correct_count += 1
        elif question not in all_correct_answers:
            quiz_2_wrong_count += 1

    for question in quiz_3_questions:
        if question in all_correct_answers:
            quiz_3_correct_count += 1
        elif question not in all_correct_answers:
            quiz_3_wrong_count += 1

    for question in quiz_4_questions:
        if question in all_correct_answers:
            quiz_4_correct_count += 1
        elif question not in all_correct_answers:
            quiz_4_wrong_count += 1

    
    
    #Poängskala:
    resultat = quiz_1_correct_count + quiz_2_correct_count + quiz_3_correct_count + quiz_4_correct_count
    
    if resultat <= 38:
        poäng = 0.0
    
    elif resultat <= 44:
        poäng = 0.1

    elif resultat <= 50:
        poäng = 0.2

    elif resultat <= 58:
        poäng = 0.3    

    elif resultat <= 64:
        poäng = 0.4      

    elif resultat <= 72:
        poäng = 0.5      
    
    elif resultat <= 78:
        poäng = 0.6  

    elif resultat <= 84:
        poäng = 0.7  

    elif resultat <= 92:
        poäng = 0.8  
        
    elif resultat <= 98:
        poäng = 0.9  
        
    elif resultat <= 106:
        poäng = 1.0  

    elif resultat <= 112:
        poäng = 1.1  
        
    elif resultat <= 118:
        poäng = 1.2  
        
    elif resultat <= 124:
        poäng = 1.3  
        
    elif resultat <= 130:
        poäng = 1.4  
        
    elif resultat <= 136:
        poäng = 1.5  
        
    elif resultat <= 140:
        poäng = 1.6  

    elif resultat <= 144:
        poäng = 1.7  
        
    elif resultat <= 148:
        poäng = 1.8  
        
    elif resultat <= 152:
        poäng = 1.9 

    elif resultat <= 160:
        poäng = 2.0  
        

            

    
    
    
    
    context = {
        'question_correct_count': question_correct_count,
        'quiz_correct_answers': quiz_correct_answers,
        'quiz_wrong_answers': quiz_wrong_answers,
        'prov': prov,
        
        'poäng': poäng,
        'resultat': resultat,
        
        'quiz_1': quiz_1,
        'quiz_2': quiz_2,
        'quiz_3': quiz_3,
        'quiz_4': quiz_4,
            
        
        'quiz_1_correct_count': quiz_1_correct_count,
        'quiz_2_correct_count': quiz_2_correct_count,
        'quiz_3_correct_count': quiz_3_correct_count,
        'quiz_4_correct_count': quiz_4_correct_count,
        
        'quiz_1_wrong_count': quiz_1_wrong_count,
        'quiz_2_wrong_count': quiz_2_wrong_count,
        'quiz_3_wrong_count': quiz_3_wrong_count,
        'quiz_4_wrong_count': quiz_4_wrong_count,
    }
    return render(request, 'base/prov-results.html', context)






def övningsBanken(request):
    request.session['question_id'] = 0
    

    provs = Prov.objects.all()
    user = request.user
    alla_övningar = []
    
    for prov in provs:
        quizzes = prov.quiz.all()
        for quiz in quizzes:
            alla_övningar.append(quiz)
    
    övningar_lst = alla_övningar
    clicked = 'alla-övningar'      
            
    if request.method == 'POST':
        formtype = request.POST.get('form-type')
        
        if formtype == 'alla-delar':
            övningar_lst = []
            clicked = 'alla-övningar'
            for quiz in alla_övningar:
                övningar_lst.append(quiz)
                
            
        if formtype == 'kvantitativ1':
            övningar_lst = []
            clicked = 'kvantitativ 1'
            for quiz in alla_övningar:
                if 'vantitativ 1' in quiz.name:
                    övningar_lst.append(quiz)
                
           
            
        if formtype == 'kvantitativ2':
            övningar_lst = []
            clicked = 'kvantitativ 2'
            for quiz in alla_övningar:
                if 'vantitativ 2' in quiz.name:
                    övningar_lst.append(quiz)
            
            
        if formtype == 'verbal1':
            övningar_lst = []
            clicked = 'verbal 1'
            for quiz in alla_övningar:
                if 'erbal 1' in quiz.name:
                    övningar_lst.append(quiz)
        
        
        if formtype == 'verbal2':
            övningar_lst = []
            clicked = 'verbal 2'
            for quiz in alla_övningar:
                if 'erbal 2' in quiz.name:
                    övningar_lst.append(quiz)
                    
                    
        elif formtype == 'starta-om-prov':
            quiz_id = request.POST.get('quiz-id-övning')
            quiz = Quiz.objects.get(id=quiz_id)
            prov_title = request.POST.get('prov-title-övning')
            prov_id = request.POST.get('prov-id-övning')
            
            questions = quiz.question.all()
            for question in questions:
                    user.completed_questions.remove(question)
                    user.save()
                    
                    completed_questions = user.completed_questions.all()
                
            del request.session['question_id']
            
            return redirect('quiz-page', prov_title=prov_title, prov_id=prov_id, quiz_id=quiz.id)
    
    if user.is_authenticated:
        completed_quizzes = user.completed_quizzes.all()
    else:
        completed_quizzes = []
        
    pending_quizzes = []
    if user.is_authenticated:
        pending_quizzes = user.pending_quizzes.all()

        
        
    
    context = {
        'alla_övningar': alla_övningar,
        'övningar_lst': övningar_lst,
        'clicked': clicked,
        'completed_quizzes': completed_quizzes,
        'pending_quizzes': pending_quizzes
    }
    return render(request, 'base/övnings-banken.html', context)



def provbanken(request):
    request.session['question_id'] = 0

    alla_prov = Prov.objects.all()
    user = request.user
    started_provs = 0
    finished_provs = 0
    
    if user.is_authenticated:
        all_answered_questions = user.all_questions_answered.all()
    
    
    if user.is_authenticated:
        started_provs = user.completed_provläge_quiz.all()
        finished_provs =  user.completed_provläge_prov.all()
        
        
      
      
    
    
    context = {
        'alla_prov': alla_prov, 
        'started_provs': started_provs,
        'finished_provs': finished_provs

    }
    return render(request, 'base/provbanken.html', context)



































































































#Not now

def createData(request):
    
    session_data = request.session.items()
    

    
    context = {

            'session_data': session_data
            
    }
    return render(request, 'base/create_data.html', context)

























# def create_objects0(request):

#     if request.method == 'POST':
#         matematik_4 = Course.objects.create(title='Matematik 4')

#         delprov_b = Quiz.objects.create(name='Delprov B', course=matematik_4)


#         #question1:
#         question1 = Question.objects.create(quiz=delprov_b, text="Ange ett komplext tal z på formen z = a + bi så att")
#         subquestion1_a = SubQuestion.objects.create(question=question1, header='a)', text="Im z = 4")
#         subquestion1_b = SubQuestion.objects.create(question=question1, header='b)', text="arg z = 45°")

#         choise1_a = Choise.objects.create(subquestion=subquestion1_a, correct_answer='z = 2 + 4i')
#         choise1_b = Choise.objects.create(subquestion=subquestion1_b, correct_answer='z = 2 + 4i')
        
#     return render(request, 'base/home.html')