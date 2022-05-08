import uuid
from django.db import models
from django.conf import settings


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'exams'


    def __str__(self) -> str:
        return self.title



class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, related_name='subject_questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    is_multiple = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'questions'


    def __str__(self) -> str:
        return self.question_text



class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, related_name='question_options', on_delete=models.CASCADE)
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'options'


    def __str__(self) -> str:
        return self.option_text



class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question_responses', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='option_responses', on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'responses'


    def __str__(self) -> str:
        return str(self.id)
