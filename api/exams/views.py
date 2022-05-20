from rest_framework import generics, permissions, exceptions
from exams.models import Question, Subject
from .serializers import SubjectSerializer, QuestionSerializer


class SubjectIDException(exceptions.APIException):
    status_code = 404
    default_detail = 'Subject ID is not available'


class SubjectListView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class SubjectQuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        subject_id = self.kwargs.get('subject_id', None)
        if subject_id is None:
            raise SubjectIDException
        return super().get_queryset().filter(subject_id=subject_id).order_by('order')