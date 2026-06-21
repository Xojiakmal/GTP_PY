from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserGroupsViewSet, PublicGroupsViewSet, UserGroupsDeleteViewSet, LookAtGroupsViewSet

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    path('user/groups', UserGroupsViewSet.as_view()),
    path('show/groups', PublicGroupsViewSet.as_view()),

    path('user/groups/<int:group_id>', UserGroupsDeleteViewSet),
    path('show/group/<int:group_id>', LookAtGroupsViewSet),
]