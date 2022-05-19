from rest_framework import generics, permissions
from exams.models import Subject
from .serializers import SubjectSerializer


class SubjectListView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
