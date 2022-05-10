from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        existing_response = None

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
def question_response(request, question_id, option_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return redirect('exam_dashboard')