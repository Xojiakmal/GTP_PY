from django.db import transaction
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.cache import cache

from .models import Groups
from test_app.models import Tests, Options
from result_app.models import Matches
from .serializers import GroupSerializer
from test_app.serializers import TestSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserGroupsViewSet(generics.ListCreateAPIView):
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_id = request.user.id

        groups = Groups.objects.filter(creator_id=user_id).values('id', 'group_name', 'duration', 'mode')

        return Response({
            'count': len(groups),
            'groups': groups,
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        new_data = request.data
        user_id = request.user.id

        if new_data['duration'] <= 0:
            return Response('Duration is incorrect', status=status.HTTP_400_BAD_REQUEST)

        created_group = Groups.objects.create(
            group_name = new_data['group_name'],
            duration = new_data['duration'],
            mode = new_data['mode'],
            creator_id_id = user_id,
        )

        return Response({
            'id': created_group.id,
            'group_name': created_group.group_name,
            'duration': created_group.duration,
            'mode': created_group.mode,
        }, status=status.HTTP_201_CREATED)



class PublicGroupsViewSet(generics.ListAPIView):
    queryset = Groups.objects.filter(mode='public')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def LookAtGroupsViewSet(request, *args, **kwargs):
    user_id = request.user.id
    group_id = kwargs['group_id']

    group_data = Groups.objects.filter(id=group_id).first()

    if group_data is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    tests = Tests.objects.prefetch_related('options').filter(id__in=group_data.tests_id)
    serializer = TestSerializer(tests, many=True)
    tests = serializer.data

    match_data = Matches.objects.filter(user_id=user_id, status='processing')
    match_data.delete()

    match_data = Matches.objects.create(
        user_id_id=user_id,
        group_id_id=group_id,
    )

    correct_answers = cache.get('correct_answers')

    if correct_answers is None:
        correct_answers = dict(
            Options.objects.filter(
                is_correct=True
            ).values_list("test_id", "id")
        )

        cache.set(
            "correct_answers",
            correct_answers,
            timeout=300*60
        )

    return Response({
        'match_id': match_data.id,
        'group_id': group_id,
        'group_name': group_data.group_name,
        'duration': group_data.duration,
        'mode': group_data.mode,
        'test_count': len(group_data.tests_id),
        'tests': tests,
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def UserGroupsDeleteViewSet(request, *args, **kwargs):
    user_id = request.user.id
    group_id = kwargs['group_id']

    group_data = Groups.objects.filter(creator_id_id=user_id, id=group_id).first()

    if group_data is None:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        with transaction.atomic():
            theseTests = Tests.objects.filter(id__in=group_data.tests_id)
            theseTests.delete()
            #
            group_data.delete()

    except Exception:
        return Response({}, status=status.HTTP_404_NOT_FOUND)


    return Response({}, status=status.HTTP_200_OK)