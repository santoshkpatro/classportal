from rest_framework import serializers
from exams.models import Subject, Question, Option


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'title',
            'description'
        ]


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'order',
            'question_text',
        ]


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = [
            'id',
            'option_text'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    question_options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'order',
            'question_text',
            'question_options'
        ]