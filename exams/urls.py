from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='exam_dashboard'),
    path('<uuid:subject_id>/', views.subject_detail, name='exam_subject_detail'),
    path('<uuid:subject_id>/questions/', views.question_detail, name='exam_subject_questions'),
    path('<uuid:question_id>/response/', views.question_response, name='exam_subject_question_response'),
]