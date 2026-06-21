from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # # Users
    # path('user/groups', UserGroupsViewSet.as_view()),
    # path('user/tests/<int:group_id>', TestFromGroupsViewSet.as_view()),
    #
    # # Show
    # path('show/groups', PublicGroupsViewSet.as_view()),

]