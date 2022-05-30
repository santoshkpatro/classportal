from django.urls import path
from .views import SubjectListView, SubjectQuestionListView, QuestionDetailView, QuestionResponseView, SubjectScoreView, SubjectDetailView


urlpatterns = [
    path('subjects/', SubjectListView.as_view()),
    path('subjects/<uuid:pk>/', SubjectDetailView.as_view()),
    path('subjects/<uuid:subject_id>/questions/', SubjectQuestionListView.as_view()),
    path('subjects/<uuid:subject_id>/questions/detail/', QuestionDetailView.as_view()),
    path('subjects/<uuid:subject_id>/score/', SubjectScoreView.as_view()),
    path('questions/<uuid:question_id>/response/', QuestionResponseView.as_view()),
]