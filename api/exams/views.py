from rest_framework import generics, permissions, exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response as RESTResponse
from exams.models import Question, Response, Subject
from .serializers import SubjectSerializer, QuestionListSerializer, QuestionSerializer, OptionSerializer


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
    serializer_class = QuestionListSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        subject_id = self.kwargs.get('subject_id', None)
        if subject_id is None:
            raise SubjectIDException
        return super().get_queryset().filter(subject_id=subject_id).order_by('order')


class QuestionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, subject_id):
        order = request.query_params.get('order', 1)
        try:
            question = Question.objects.get(subject_id=subject_id, order=order)
            serializer = QuestionSerializer(instance=question)

            try:
                existing_response = Response.objects.get(user=request.user, question=question)
            except Response.DoesNotExist:
                existing_response = None

            if not existing_response:
                return RESTResponse(data={
                    'question': serializer.data, 
                    'existing_response_option': None
                }, status=status.HTTP_200_OK)

            existing_response_serializer = OptionSerializer(instance=existing_response.option)
            
            return RESTResponse(data={
                    'question': serializer.data, 
                    'existing_response_option': existing_response_serializer.data
                }, status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return RESTResponse(data={'detail': 'Question not available!'}, status=status.HTTP_404_NOT_FOUND)
