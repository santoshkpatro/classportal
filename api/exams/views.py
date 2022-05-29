import uuid
from rest_framework import generics, permissions, exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response as RESTResponse
from exams.models import Option, Question, Response, Subject
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



class QuestionResponseView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return RESTResponse(data={'detail': 'Question not available'}, status=status.HTTP_404_NOT_FOUND)
        
        option_id = request.query_params.get('option_id', None)
        if not option_id:
            return RESTResponse(data={'detail': 'Please provide option id'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            option = Option.objects.get(id=option_id)
        except Option.DoesNotExist:
            return RESTResponse(data={'detail': 'Option not available'}, status=status.HTTP_404_NOT_FOUND)

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
            response = Response(user=self.request.user, question=question, option=option, score=score, is_correct=is_correct)
            response.save()

        return RESTResponse(data={'detail': 'Response taken'}, status=status.HTTP_201_CREATED)
