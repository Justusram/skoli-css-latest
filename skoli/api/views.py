from django.shortcuts import render
from django.http import JsonResponse



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . serializers import QuestionSerializer, ChoiseSerializer, SubmitAnswerResponseSerializer
from base.models import Prov, Quiz, Question, Choise


# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    return Response("Api base point")



@api_view(['GET'])
def questionRecive(request, question_id):
    user = request.user
    completed_questions = user.completed_questions.all()
    
    question = Question.objects.get(id=question_id)
    question_serializer = QuestionSerializer(question, many=False)

    
    
    #Om det är första/sista frågan, för att visa/döja nästa/tillbaka knapp
    quiz = question.quiz
    all_questions = quiz.question.all()
    current_question = question
    
    for idx, question in enumerate(all_questions):
        if current_question == question:
            question_index = idx
            break
    
    sista_fråga = False
    if all_questions[question_index] == all_questions.last():
        sista_fråga = True
        
    första_fråga = False
    if all_questions[question_index] == all_questions.first():
        första_fråga = True
    #________END________
    
    
    
    completed = False
    if question in completed_questions:
        completed = True
    
    choises = question.choise.all()
    choise_serializer = ChoiseSerializer(choises, many=True)
    

    data = {
        "question": question_serializer.data,
        "choises": choise_serializer.data,
        "completed": completed,
        'första_fråga': första_fråga,
        'sista_fråga': sista_fråga,
    }

    return Response(data)


@api_view(['GET'])
def submitAnswer(request, submitted_choise_id):
    
    submitted_choise = Choise.objects.get(id=submitted_choise_id)
    

    question = submitted_choise.question
    correct_choise = question.choise.get(correct_answer=True)
    
    user = request.user
    user.pending_quizzes.add(question.quiz)
    user.save()
    
    
    subbmitted_answer = ''
    
    

    
    if correct_choise.id == submitted_choise.id:
        user.completed_questions.add(question)
        user.save()
        
        submitted_answer = 'correct'
        question_id = question.id
        
        data = {
            'submitted_answer': submitted_answer,
            'question_id': question_id
        }
        return Response(data)

        
    elif correct_choise.id != submitted_choise.id:
        submitted_answer = 'incorrect'
        
        data = {
            'submitted_answer': submitted_answer 
        }
    

        return Response(data)


        
@api_view(['GET'])
def nextQuestion(request, current_question_id):
    user = request.user
    completed_questions = user.completed_questions.all()
    
    
    current_question = Question.objects.get(id=current_question_id)
    quiz = current_question.quiz
    questions = quiz.question.all() 
    
    
    #Get the index of the current question. 
    current_question_index = None
    for idx, question in enumerate(questions):
        if question.id == current_question.id:
            current_question_index = idx
            break
        
    #Add 1 to the current index to get the next question in questions
    next_question_index = current_question_index + 1
    next_question = questions[next_question_index]
    question_serializer = QuestionSerializer(next_question, many=False)
    
    #Check if the questioni is completed
    completed = False
    if next_question in completed_questions:
        completed = True
    
    #Get all the choises for the question
    next_question_choises = next_question.choise.all()
    choise_serializer = ChoiseSerializer(next_question_choises, many=True)
  
  
  
  
    #Om det är sista frågan, för att döja nästa knapp
    all_questions = quiz.question.all()
    
    for idx, question in enumerate(all_questions):
        if next_question == question:
            question_index = idx
            break
    
    sista_fråga = False
    if all_questions[question_index] == all_questions.last():
        sista_fråga = True
        
    första_fråga = False
    if all_questions[question_index] == all_questions.first():
        första_fråga = True
    #________END________
  
  
  
    
    data = {
        "question": question_serializer.data,
        "choises": choise_serializer.data,
        "completed": completed,
        'första_fråga': första_fråga,
        'sista_fråga': sista_fråga,
    }
    
    return Response(data)





@api_view(['GET'])
def backOneQuestion(request, current_question_id):
    user = request.user
    completed_questions = user.completed_questions.all()
    
    
    current_question = Question.objects.get(id=current_question_id)
    quiz = current_question.quiz
    questions = quiz.question.all()
  
    
    #Get the index of the current question. 
    current_question_index = None
    for idx, question in enumerate(questions):
        if question.id == current_question.id:
            current_question_index = idx
            break
        
    #Minus 1 to the current index to get the before this question in questions

    last_question_index = current_question_index - 1
    last_question = questions[last_question_index]
    question_serializer = QuestionSerializer(last_question, many=False)
    
    #Check if the questioni is completed
    completed = False
    if last_question in completed_questions:
        completed = True
    
    #Get all the choises for the question
    last_question_choises = last_question.choise.all()
    choise_serializer = ChoiseSerializer(last_question_choises, many=True)
    
    
    
    #Om det är första frågan,  döj tbx knapp
    all_questions = quiz.question.all()
    
    for idx, question in enumerate(all_questions):
        if last_question == question:
            question_index = idx
            break
    
    sista_fråga = False
    if all_questions[question_index] == all_questions.last():
        sista_fråga = True
        
    första_fråga = False
    if all_questions[question_index] == all_questions.first():
        första_fråga = True
    #________END________
    
    

    data = {
        "question": question_serializer.data,
        "choises": choise_serializer.data,
        "completed": completed,
        'första_fråga': första_fråga,
        'sista_fråga': sista_fråga,
    }
    
    return Response(data)
    

#PROVLÄGE: ==================================================================

@api_view(['GET'])
def questionReciveProvläge(request, question_id):
    user = request.user
    answered_questons = user.all_questions_answered.all()
    
    question = Question.objects.get(id=question_id)
    question_serializer = QuestionSerializer(question, many=False)

    
    #Om det är första/sista frågan, för att visa/döja nästa/tillbaka knapp
    quiz = question.quiz
    all_questions = quiz.question.all()
    current_question = question
    
    for idx, question in enumerate(all_questions):
        if current_question == question:
            question_index = idx
            break
    
    sista_fråga = False
    if all_questions[question_index] == all_questions.last():
        sista_fråga = True
        
    första_fråga = False
    if all_questions[question_index] == all_questions.first():
        första_fråga = True
    #________END________
    
    
    answered = False
    if question in answered_questons:
        answered = True
        
    choises = question.choise.all()
    choises_serializer = ChoiseSerializer(choises, many=True)
    
    current_choise = None
    if answered == True:
        all_submitted_choises = user.your_choise.all()
        for choise in choises:
            if choise in all_submitted_choises:
                current_choise = choise
                choise_serializer = ChoiseSerializer(current_choise, many=False)
                break

        data = {
            "question": question_serializer.data,
            "choises": choises_serializer.data,
            "answered": answered,
            "current_choise": choise_serializer.data,
            "första_fråga": första_fråga,
            "sista_fråga": sista_fråga,
                
        }
    
    else:
        data = {
            "question": question_serializer.data,
            "choises": choises_serializer.data,
            "answered": answered,
            "current_choise": current_choise,
            "första_fråga": första_fråga,
            "sista_fråga": sista_fråga,
        }

    
    return Response(data)


@api_view(['GET'])
def submitAnswerProvläge(request, submitted_choise_id):
    
    submitted_choise = Choise.objects.get(id=submitted_choise_id)
    

    question = submitted_choise.question
    correct_choise = question.choise.get(correct_answer=True)
    
    prov = question.quiz.prov
    
    user = request.user
    user.your_choise.add(submitted_choise)
    user.all_questions_answered.add(question)
    user.completed_provläge_quiz.add(prov)
    user.save()
    
    
    if correct_choise.id == submitted_choise.id:
        user.correct_questions_answered.add(question)
        user.save()
        
    question_id = question.id
        
    data = {
        'question_id': question_id
    }
    return Response(data)


@api_view(['GET'])
def changeAnswerProvläge(request, submitted_choise_id):
    user = request.user
    submitted_choise = Choise.objects.get(id=submitted_choise_id)
    
    
    question = submitted_choise.question
    all_question_choises = question.choise.all()
    correct_choise = question.choise.get(correct_answer=True)
   
    all_your_choises = user.your_choise.all()
    for choise in all_question_choises:
        if choise in all_your_choises:
            user.your_choise.remove(choise)
            user.save()
    

    user.your_choise.add(submitted_choise)
    user.all_questions_answered.add(question)
    user.save()
    
    
    if correct_choise.id == submitted_choise.id:
        user.correct_questions_answered.add(question)
        user.save()
    else:
        user.correct_questions_answered.remove(question)
        user.save()
        

        
    question_id = question.id
        
    data = {
        'question_id': question_id
    }
    return Response(data)
   

@api_view(['GET'])
def nextQuestionProvläge(request, current_question_id):
    user = request.user
    answered_questions = user.all_questions_answered.all()
    
    
    current_question = Question.objects.get(id=current_question_id)
    quiz = current_question.quiz
    questions = quiz.question.all()
    
    #Get the index of the current question. 
    current_question_index = None
    for idx, question in enumerate(questions):
        if question.id == current_question.id:
            current_question_index = idx
            break
        
    #Add 1 to the current index to get the next question in questions
    next_question_index = current_question_index + 1
    next_question = questions[next_question_index]
    question_serializer = QuestionSerializer(next_question, many=False)
    
    #Check if the questioni is completed
    answered = False
    if next_question in answered_questions:
        answered = True
    
    #Get all the choises for the question
    next_question_choises = next_question.choise.all()
    choises_serializer = ChoiseSerializer(next_question_choises, many=True)
  
  
  
  
    #Om det är första frågan,  döj tbx knapp
    all_questions = quiz.question.all()
    
    for idx, question in enumerate(all_questions):
        if next_question == question:
            question_index = idx
            break
    
    sista_fråga = False
    if all_questions[question_index] == all_questions.last():
        sista_fråga = True
        
    första_fråga = False
    if all_questions[question_index] == all_questions.first():
        första_fråga = True
    #________END________ 
  
  
  
  
  
    next_your_choise = None
    if answered == True:
        all_submitted_choises = user.your_choise.all()
        for choise in next_question_choises:
            if choise in all_submitted_choises:
                next_your_choise = choise
                choise_serializer = ChoiseSerializer(next_your_choise, many=False)
                break
            
      
     
    

        data = {
            "question": question_serializer.data,
            "choises": choises_serializer.data,
            "answered": answered,
            "current_choise": choise_serializer.data,
            "första_fråga": första_fråga,
            "sista_fråga": sista_fråga,
            
        }
    
    else:
        data = {
            "question": question_serializer.data,
            "choises": choises_serializer.data,
            "answered": answered,
            "current_choise": next_your_choise,
            "första_fråga": första_fråga,
            "sista_fråga": sista_fråga,
        }

    
    return Response(data)









@api_view(['GET'])
def backOneQuestionProvläge(request, current_question_id):
    user = request.user
    answered_questions = user.all_questions_answered.all()
    
    
    current_question = Question.objects.get(id=current_question_id)
    quiz = current_question.quiz
    questions = quiz.question.all()
    
    #Get the index of the current question. 
    current_question_index = None
    for idx, question in enumerate(questions):
        if question.id == current_question.id:
            current_question_index = idx
            break
        
    #Add 1 to the current index to get the next question in questions
    last_question_index = current_question_index - 1
    last_question = questions[last_question_index]
    question_serializer = QuestionSerializer(last_question, many=False)
    
    #Check if the questioni is completed
    answered = False
    if last_question in answered_questions:
        answered = True
    
    #Get all the choises for the question
    last_question_choises = last_question.choise.all()
    choises_serializer = ChoiseSerializer(last_question_choises, many=True)
  
  
    #Om det är första frågan,  döj tbx knapp
    all_questions = quiz.question.all()
    
    for idx, question in enumerate(all_questions):
        if last_question == question:
            question_index = idx
            break
    
    sista_fråga = False
    if all_questions[question_index] == all_questions.last():
        sista_fråga = True
        
    första_fråga = False
    if all_questions[question_index] == all_questions.first():
        första_fråga = True
    #________END________
  
  
  
  
    last_your_choise = None
    if answered == True:
        all_submitted_choises = user.your_choise.all()
        for choise in last_question_choises:
            if choise in all_submitted_choises:
                last_your_choise = choise
                choise_serializer = ChoiseSerializer(last_your_choise, many=False)
                break
            
  
        data = {
            "question": question_serializer.data,
            "choises": choises_serializer.data,
            "answered": answered,
            "current_choise": choise_serializer.data,
            "första_fråga": första_fråga,
            "sista_fråga": sista_fråga,
            
        }
    
    else:
        data = {
            "question": question_serializer.data,
            "choises": choises_serializer.data,
            "answered": answered,
            "current_choise": last_your_choise,
            "första_fråga": första_fråga,
            "sista_fråga": sista_fråga,
        }

    
    return Response(data)