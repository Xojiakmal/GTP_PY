# from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .serializers import GetResultSerializer
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from test_app.models import Options
from group_app.models import Groups
from .models import Matches

# Create your views here.

@swagger_auto_schema(
    method="POST",
    request_body=GetResultSerializer,
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ProgressResultView(request, *args, **kwargs):
    group_id = kwargs['group_id']
    serializer = GetResultSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    group_data = Groups.objects.filter(id=group_id).first()
    match_data = Matches.objects.get(id=data['match_id'])

    all_test_count = len(data['results'])
    correct_answers = cache.get('correct_answers')

    try:
        point = 0
        for info in data['results']:
            if correct_answers.get(info['question_id']) == info['answer_id']:
                point += 1

        correct_percent = (point / all_test_count) * 100

        if (timezone.now() - match_data.start_time).total_seconds() > group_data.duration * 60:
            correct_percent = 0
            point = 0

        match_data.end_time = timezone.now()
        match_data.status = 'completed'
        match_data.result = correct_percent
        match_data.save()

        return Response({
            'group_name':group_data.group_name,
            'test_count': all_test_count,
            'correct_answer': point,
            'percent': correct_percent,
        }, status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)