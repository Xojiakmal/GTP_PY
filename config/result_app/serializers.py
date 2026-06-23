from .models import Matches
from rest_framework import serializers


class QuestAndAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()


class GetResultSerializer(serializers.Serializer):
    results = QuestAndAnswerSerializer(many=True)
    match_id = serializers.IntegerField()