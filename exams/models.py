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



class UserSubjectDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_user_subject_list')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_user_subject_list')
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        db_table = 'user_subject_details'


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, related_name='subject_questions', on_delete=models.CASCADE)
    order = models.IntegerField()
    question_text = models.TextField()
    is_multiple = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    score = models.IntegerField()
    negative_marking_allowed = models.BooleanField(default=False)
    negative_marking_score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'questions'
        unique_together = ['subject', 'order']


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
    option = models.ForeignKey(Option, related_name='option_responses', on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    score = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'responses'
        unique_together = ['user', 'question']


    def __str__(self) -> str:
        return str(self.id)
