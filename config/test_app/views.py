from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated
from .serializers import TestSerializer, OptionSerializer
from group_app.models import Groups
from .models import Tests, Options


# Create your views here.
class TestFromGroupsViewSet(generics.ListCreateAPIView):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        group_id = kwargs['group_id']
        user_id = request.user.id
        #
        group_data = Groups.objects.filter(creator_id=user_id, id=group_id).first()

        if group_data is None:
            return Response( {},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        tests = group_data.tests_id
        group_name = group_data.group_name
        group_duration = group_data.duration

        if tests:
            tests = Tests.objects.prefetch_related('options').filter(id__in=tests)
            serializer = TestSerializer(tests, many=True)
            tests = serializer.data
            # tests = Tests.objects.filter(id__in=tests).prefetch_related('options')
            # tests = Tests.objects.prefetch_related('options').filter(id__in=tests).values()

        return Response({
            'group_name': group_name,
            'match_duration': group_duration,
            'tests': tests,
        }, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        new_data = request.data
        group_id = kwargs['group_id']
        user_id = request.user.id

        group_data = Groups.objects.filter(creator_id=user_id, id=group_id).first()

        if group_data is None:
            return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        try:
            with transaction.atomic():
                addTest = Tests.objects.create(
                    content=new_data['content'],
                    type=new_data['type'],
                )
                oldTestsId = group_data.tests_id

                if oldTestsId:
                    oldTestsId.append(addTest.id)
                else:
                    oldTestsId = [addTest.id]
                group_data.tests_id = oldTestsId
                group_data.save()

        except Exception:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'id': addTest.id,
                'content': addTest.content,
                'type': addTest.type,
            }, status=status.HTTP_201_CREATED)



class OptionFromGroupsViewSet(generics.CreateAPIView):
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        new_data = request.data
        group_id = kwargs['group_id']
        test_id = kwargs['test_id']
        user_id = request.user.id

        group_data = Groups.objects.filter(creator_id=user_id, id=group_id).first()

        if group_data is None:
            return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)


        addOption = Options.objects.create(
            test_id_id=test_id,
            content=new_data['content'],
            is_correct=new_data['is_correct'],
        )


        return Response({
            'option_id': addOption.id,
            'group_id': group_id,
            'test_id': test_id,
        }, status=status.HTTP_201_CREATED)


    # def delete(self, request, *args, **kwargs):
    #     new_data = request.data
    #     group_id = kwargs['group_id']
    #     test_id = kwargs['test_id']
    #     user_id = request.user.id
    #
    #     group_data = Groups.objects.filter(creator_id=user_id, id=group_id)
    #
    #     if group_data is None:
    #         return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #
    #     # group_data.delete()
    #
    #     return Response({}, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def OptionDeleteFromGroupsViewSet(request, *args, **kwargs):
    # new_data = request.data
    option_id = kwargs['option_id']
    group_id = kwargs['group_id']
    test_id = kwargs['test_id']
    user_id = request.user.id

    group_data = Groups.objects.filter(creator_id=user_id, id=group_id).first()

    if group_data is None or test_id not in group_data.tests_id:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    thisOption = Options.objects.filter(test_id_id=test_id, id=option_id)

    thisOption.delete()


    return Response({
        'option': thisOption,
    }, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def TestDeleteFromGroupsViewSet(request, *args, **kwargs):
    # new_data = request.data
    # option_id = kwargs['option_id']
    group_id = kwargs['group_id']
    test_id = kwargs['test_id']
    user_id = request.user.id

    group_data = Groups.objects.filter(creator_id=user_id, id=group_id).first()

    if group_data is None or test_id not in group_data.tests_id:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    try:
        with transaction.atomic():

            if group_data.tests_id:
                thisTest = Tests.objects.get(id=test_id)
                thisTest.delete()

                group_data.tests_id.remove(test_id)
                group_data.save()


    except Exception:
        return Response('', status=status.HTTP_400_BAD_REQUEST)



    return Response({}, status=status.HTTP_200_OK)