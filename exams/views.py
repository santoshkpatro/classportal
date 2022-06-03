from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Question, Response, Subject, Option, UserSubjectDetail


@login_required(login_url='login')
def dashboard(request):
    incomplete_subjects = Subject.objects.filter(subject_user_subject_list__is_complete=False, subject_user_subject_list__user=request.user)
    complete_subjects = Subject.objects.filter(subject_user_subject_list__is_complete=True, subject_user_subject_list__user=request.user)
    subjects = Subject.objects.filter(is_active=True)
    subjects = subjects.difference(complete_subjects).difference(incomplete_subjects)
    context = {
        'subjects': subjects,
        'incomplete_subjects': incomplete_subjects,
        'complete_subjects': complete_subjects,
    }

    return render(request, 'exams/dashboard.html', context=context)


@login_required(login_url='login')
def start_exam(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id, is_active=True)
    except Subject.DoesNotExist:
        messages.warning(request, 'No subject info found')
        return redirect('exam_dashboard')

    try:
        existing_user_subject = UserSubjectDetail.objects.get(user=request.user, subject=subject)
    except UserSubjectDetail.DoesNotExist:
        user_subject = UserSubjectDetail.objects.create(user=request.user, subject=subject, start_time=timezone.now().time())

    return redirect('exam_subject_questions', subject_id=subject.id)


@login_required(login_url='login')
def subject_detail(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
        question_count = Question.objects.filter(subject=subject).count
        return render(request, 'exams/subject_detail.html', {'subject': subject, 'question_count': question_count})
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
        responses = Response.objects.filter(question__in=questions, user=request.user).order_by('question__order')
        score = responses.aggregate(Sum('score'))['score__sum']
        total_score = questions.aggregate(Sum('score'))['score__sum']

        context = {
            'subject': subject,
            'questions': questions,
            'responses': responses,
            'score': score,
            'total_score': total_score
        }
        return render(request, 'exams/subject_score_detail.html', context=context)
    except Subject.DoesNotExist:
        messages.error(request, 'Invalid subject ID')
        return redirect('exam_dashboard')


def end_exam(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id, is_active=True)
    except Subject.DoesNotExist:
        messages.warning(request, 'No subject info found')
        return redirect('exam_dashboard')

    try:
        user_subject = UserSubjectDetail.objects.get(user=request.user, subject=subject)
    except UserSubjectDetail.DoesNotExist:
        messages.error(request, 'Invalid exam question access')
        return redirect('exam_dashboard')

    user_subject.end_time = timezone.now().time()
    user_subject.is_complete = True
    user_subject.save()

    return redirect('exam_subject_score_detail', subject_id=subject.id)