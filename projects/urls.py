from django.urls import path, include
from rest_framework import routers

from .views import ProjectViewSet, CommentViewSet, ProjectMembershipViewSet


router = routers.DefaultRouter()

router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'projects/(?P<project_pk>[^/.]+)/comments', CommentViewSet, basename='project-comment')
router.register(r'projects/(?P<project_pk>[^/.]+)/memberships', ProjectMembershipViewSet, basename='project-membership')

urlpatterns = [
    path('', include(router.urls))
]