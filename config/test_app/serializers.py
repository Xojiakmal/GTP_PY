from rest_framework import serializers
from .models import Tests, Options

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ['id', 'content', 'is_correct']



class TestSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Tests
        fields = ['id', 'content', 'type', 'options']


