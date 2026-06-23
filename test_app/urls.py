from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestFromGroupsViewSet, OptionFromGroupsViewSet, OptionDeleteFromGroupsViewSet, TestDeleteFromGroupsViewSet

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('user/tests/<int:group_id>', TestFromGroupsViewSet.as_view()),
    path('user/option/<int:group_id>/<int:test_id>', OptionFromGroupsViewSet.as_view()),

    path('user/option/<int:group_id>/<int:test_id>/<int:option_id>', OptionDeleteFromGroupsViewSet),
    path('user/tests/<int:group_id>/<int:test_id>', TestDeleteFromGroupsViewSet),

]