from django.urls import path
from .views import SubjectListView, SubjectQuestionListView


urlpatterns = [
    path('subjects/', SubjectListView.as_view()),
    path('subjects/<uuid:subject_id>/questions/', SubjectQuestionListView.as_view())
]