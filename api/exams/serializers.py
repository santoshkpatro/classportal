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

    # def get_options(self, obj):
    #     serializer = OptionSerializer(instance=obj.question_options, many=True)
    #     return serializer.data