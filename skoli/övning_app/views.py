from django.shortcuts import render, redirect
from .models import Övning
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
def övningar(request):
    
    request.session['fråga_id'] = None

    provs = []
    user = request.user
    alla_övningar = Övning.objects.all()

    
    övningar_lst = alla_övningar
    clicked = 'alla-övningar'      
            
    if request.method == 'POST':
        formtype = request.POST.get('form-type')
        
        if formtype == 'alla-delar':
            övningar_lst = []
            clicked = 'alla-övningar'
            for quiz in alla_övningar:
                övningar_lst.append(quiz)
                
            
        if formtype == 'ORD':
            övningar_lst = []
            clicked = 'ORD'
            for övning in alla_övningar:
                if 'ord' or 'ORD' in övning.name:
                    övningar_lst.append(övning)
                
           
            
        if formtype == 'LÄS':
            övningar_lst = []
            clicked = 'LÄS'
            for quiz in alla_övningar:
                if 'läs' or 'LÄS' in quiz.name:
                    övningar_lst.append(quiz)
            
            
        if formtype == 'MEK':
            övningar_lst = []
            clicked = 'MEK'
            for quiz in alla_övningar:
                if 'mek' or 'MEK' in quiz.name:
                    övningar_lst.append(quiz)


        if formtype == 'ELF':
            övningar_lst = []
            clicked = 'ELF'
            for quiz in alla_övningar:
                if 'elf' or 'ELF' in quiz.name:
                    övningar_lst.append(quiz)
                    
        
        if formtype == 'XYZ':
            övningar_lst = []
            clicked = 'XYZ'
            for quiz in alla_övningar:
                if 'xyz' or 'XYZ' in quiz.name:
                    övningar_lst.append(quiz)

        if formtype == 'KVA':
            övningar_lst = []
            clicked = 'KVA'
            for quiz in alla_övningar:
                if 'kva' or 'KVA' in quiz.name:
                    övningar_lst.append(quiz)

        if formtype == 'NOG':
            övningar_lst = []
            clicked = 'NOG'
            for quiz in alla_övningar:
                if 'nog' or 'NOG' in quiz.name:
                    övningar_lst.append(quiz)
                    
        if formtype == 'DTK':
            övningar_lst = []
            clicked = 'DTK'
            for quiz in alla_övningar:
                if 'dtk' or 'DTK' in quiz.name:
                    övningar_lst.append(quiz)
                    
                    

    gjorda_övningar = []
    påbörjade_övningar = []
        
    if user.is_authenticated:    
        gjorda_övningar = user.gjorda_övningar.all()
        påbörjade_övningar = user.påbörjade_övningar.all()
        
    context = {
        'gjorda_övningar': gjorda_övningar,
        'påbörjade_övningar': påbörjade_övningar,
        'alla_övningar': alla_övningar,
        'övningar_lst': övningar_lst,
        'clicked': clicked,
    }
    
    return render(request, 'övning_app/övningar.html', context)


def övningPage(request, övning_name, övning_id):
      
    user = request.user
    # completed_questions = user.completed_questions.all()
    

    
    
    #get the current id for question that is stored in session to do something with the id below
    fråga_id = request.session.get('fråga_id')
    
    #set dummy data so that if the if requierments are not fulfilled, we do not get a value error
    # quiz = {'id': 0}
    fråga = None
    frågor = []
    choises = []
    alternativen = []
   

    # quiz_id is stored in the last url /quiz_id/ to get the current delprov the user visits 
    if int(övning_id) > 0:
        övning = Övning.objects.get(id=övning_id)
        frågor = övning.fråga.all()
        
     
        #if the id of the question does not exist in the session, create the session and set it to the first index of the questions list
        if fråga_id is None:
            fråga_id = request.session['fråga_id'] = 0
            fråga = frågor.first()
            
            alternativen = fråga.alternativ.all()
     
        #if however, the id of question DOES exist in the session, get all the choises related to that question if there are any.
        else:
            try:
                fråga = frågor[int(fråga_id)]
                alternativen = fråga.alternativ.all()
            
            
            
            #Gör så att när användare trycker på nästa vid sista fråga och idexerror uppstår, att om alla frågor har gjorts, så visas en bra jobbat sida:
            # except IndexError:
   
            #     completed_questions = user.completed_questions.all()
            #     all_questions_completed = True
                
            #     for question in questions:
            #         if question not in completed_questions:
            #             all_questions_completed = False
            
            except IndexError:
                request.session['fråga_id'] = 1

            
            except ValueError:
                request.session['fråga_id'] = 0
                return redirect(request.path)
            
        #more dummydata
        clicked = övning.id 
    link_clicked = fråga.id   
    
    
    besvarade_frågor = request.session.get('besvarade_frågor')
    
    if besvarade_frågor == None:
        request.session['besvarade_frågor'] = []         
                
                
                


    
    
    
    #if the user triggers a post request
    if request.method == 'POST':
        formtype = request.POST.get('form-type')
        
        #logic for the user answer
        
        #check if answer is correct
        try:
            if formtype == 'answer-submission':
                

           
                
                answer = request.POST.get('answer')
                submitted_choise = fråga.alternativ.get(id=answer)
                
                if submitted_choise.correct_answer:
                    messages.success(request, 'Rätt, bra jobbat!')
                    
                    # Nästa fråga automatiskt när svaret är rätt: 
                    # request.session['question_id'] = question_id + 1
                    
                    #Spara frågan som gjord i användarmodellen
                    # user.pending_quizzes.add(quiz)
                    # user.completed_questions.add(question)
                    # user.save()
                    
                    if user.is_authenticated:
                        user.påbörjade_övningar.add(övning)
                        user.besvarade_frågor.add(fråga)
                        user.save()
                    
                    else:
                        request.session['besvarade_frågor'].append(fråga)



                    #Get all the questions that the user has completed, so that we can check if a question is completed, in the html template
                    return redirect(request.path)
            
                #if wrong answer, give error message
                else:
                    
                    
                    messages.error(request, 'Fel svar, försök igen')
                    
                    
                    
            elif formtype == 'answer-submission-last':
                
                answer = request.POST.get('answer')
                submitted_choise = fråga.alternativ.get(id=answer)
                
                if user.is_authenticated:
                    user.gjorda_övningar.add(övning)
                    user.save()

                if submitted_choise.correct_answer:
                    messages.success(request, 'Rätt, bra jobbat!')
                    
                    
                    # Nästa fråga automatiskt när svaret är rätt: 
                    # request.session['question_id'] = question_id + 1
                    
                    #Spara frågan som gjord i användarmodellen
                    
                    # user.pending_quizzes.remove(quiz)
                    # user.completed_quizzes.add(quiz)
                    # user.completed_questions.add(question)
                    # user.save()
                    
                    if user.is_authenticated:
                        user.besvarade_frågor.add(fråga)
                        user.påbörjade_övningar.remove(övning)
                        user.gjorda_övningar.add(övning)
                        user.save()
                    
                    elif not user.is_authenticated:
                        request.session['besvarade_frågor'].append(fråga)


                    #Get all the questions that the user has completed, so that we can check if a question is completed, in the html template
                    return redirect(request.path)
            
                #if wrong answer, give error message
                else:
                    messages.error(request, 'Fel svar, försök igen')
                
                    
        except ObjectDoesNotExist:
            messages.error(request, 'du måste välja ett alternativ')
            
            

            

            
            
        
        #logic for Buttuns for navigating back forward through the quiz
        if formtype == 'back-one-question':
            
            request.session['fråga_id'] = fråga_id - 1
            return redirect(request.path)
                
               
        elif formtype == 'forward-one-question':
            request.session['fråga_id'] = fråga_id + 1
            return redirect(request.path)
        #end logic for navigating one-back-one-forward


        #button for resetting the test
        # elif formtype == 'starta-om-prov':
            
            # for question in frågor:
            #         user.completed_questions.remove(question)
            #         user.save()
                    
            #         completed_questions = user.completed_questions.all()
                
            # del request.session['question_id']
            
            # return redirect(request.path)
        
        
        #navigationbar, jump back and forth between all questions
        elif formtype == 'navigate-questions':
            fråga_id = request.POST.get('jump-question-link')
            
            request.session['fråga_id'] = int(fråga_id) - 1
            return redirect(request.path)
        
        
        elif formtype == 'nästa-del':
            
            request.session['question_id'] = 0
            # return redirect('quiz-page', prov_title=prov.title, prov_id=prov.id, quiz_id=int(quiz_id) + 1)
        

            
    
    last_fråga = False      
    if fråga == frågor.last():
        last_fråga = True
        
    first_fråga = False
    if fråga == frågor.first():
        first_fråga = True
            
 
   
  
              
            
    if not user.is_authenticated:
        besvarade_frågor = request.session.get('besvarade_frågor', [])
        context = { 

                'quiz': fråga,
                'frågor': frågor,
                #    'quiz_id': quiz_id,

                'question': fråga,
                'choises': alternativen,
                'question_id': fråga_id,
                'completed_questions': besvarade_frågor,
                'clicked': clicked,
                'link_clicked': link_clicked,
                'last_question': last_fråga,
                'first_question': first_fråga


                }
    else:
        besvarade_frågor = user.besvarade_frågor.all()
        context = { 
            'quiz': fråga,
            'frågor': frågor,
            #    'quiz_id': quiz_id,

            'question': fråga,
            'choises': alternativen,
            'question_id': fråga_id,
            'completed_questions': besvarade_frågor,
            'clicked': clicked,
            'link_clicked': link_clicked,
            'last_question': last_fråga,
            'first_question': first_fråga
        }
    
    return render(request, 'övning_app/övning-page.html', context)