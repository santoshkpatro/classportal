from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Question, Response, Subject, Option


@login_required(login_url='login')
def dashboard(request):
    subjects = Subject.objects.filter(is_active=True)
    context = {
        'subjects': subjects
    }
    return render(request, 'exams/dashboard.html', context=context)



@login_required(login_url='login')
def subject_detail(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
        return render(request, 'exams/subject_detail.html', {'subject': subject})
    except Subject.DoesNotExist:
        messages.error(request, 'Invalid subject ID')
        return redirect('exam_dashboard')


@login_required(login_url='login')
def question_detail(request, subject_id):
    try:
        order = request.GET.get('order', 1)
        subject = Subject.objects.get(id=subject_id)
        questions = Question.objects.filter(subject=subject).order_by('order')

        try:
            selected_question = questions.get(order=order)
        except Question.DoesNotExist:
            return redirect('exam_subject_questions', subject_id=subject_id)

        options = Option.objects.filter(question=selected_question)
        
        try:
            existing_response = Response.objects.get(question=selected_question, user=request.user)
        except Response.DoesNotExist:
            existing_response = None
        
        context = {
            'subject': subject,
            'questions': questions, 
            'selected_question': selected_question, 
            'options': options,
            'existing_response': existing_response
        }

        return render(request, 'exams/question_detail.html', context=context)
    except Subject.DoesNotExist:
        messages.error(request, 'Invalid subject ID')
        return redirect('exam_dashboard')


@login_required(login_url='login')
def question_response(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        messages.error(request, 'Unable to find question')
        return redirect('exam_dashboard')
    
    try:
        option = Option.objects.get(id=request.GET['option_id'])
    except Option.DoesNotExist:
        messages.error(request, 'Unable to find option')
        return redirect('exam_dashboard')

    if option.question_id != question.id:
        messages.error(request, 'Invalid Option Access')
        return redirect('exam_subject_questions', subject_id=question.subject.id)

    try:
        existing_response = Response.objects.get(question=question, user=request.user)
    except Response.DoesNotExist:
        existing_response = None

    # Calculating score
    if option.is_correct:
        is_correct = True
        score = question.score
    else:
        is_correct = False
        score = 0

    if existing_response:
        existing_response.option = option
        existing_response.score = score
        existing_response.is_correct = is_correct
        existing_response.save()
    else:
        response = Response(user=request.user, question=question, option=option, score=score, is_correct=is_correct)
        response.save()

    try:
        next_question = Question.objects.get(subject=question.subject, order=question.order + 1)
        return redirect(reverse('exam_subject_questions', kwargs={'subject_id': question.subject.id}) + f'?order={next_question.order}')
    except Question.DoesNotExist:
        return redirect('exam_subject_questions', subject_id=question.subject.id)

    
def subject_score_detail(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
        questions = Question.objects.filter(subject=subject)
        responses = Response.objects.filter(question__in=questions, user=request.user)
        score = responses.aggregate(Sum('score'))['score__sum']

        context = {
            'subject': subject,
            'questions': questions,
            'responses': responses,
            'score': score
        }
        return render(request, 'exams/subject_score_detail.html', context=context)
    except Subject.DoesNotExist:
        messages.error(request, 'Invalid subject ID')
        return redirect('exam_dashboard')