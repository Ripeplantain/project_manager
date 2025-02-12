from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, ProjectMembership, Comment
from .serializers import ProjectSerializer, ProjectMembershipSerializer, CommentSerializer
from .permissions import ProjectPermission, CommentPermission, RolePermission

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def get_queryset(self):
        user_memberships = ProjectMembership.objects.filter(user=self.request.user)
        return Project.objects.filter(projectmembership__in=user_memberships)

    def perform_create(self, serializer):
        project = serializer.save()
        ProjectMembership.objects.create(
            user=self.request.user,
            project=project,
            role='OWNER'
        )

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        try:
            membership = ProjectMembership.objects.get(
                user=request.user,
                project=project
            )
            if membership.role != 'OWNER':
                return Response(
                    {'error': 'Only owners can add members'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except ProjectMembership.DoesNotExist:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProjectMembershipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def get_queryset(self):
        return Comment.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            project_id=self.kwargs['project_pk']
        )
        
class ProjectMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMembershipSerializer
    permission_classes = [RolePermission]

    def get_queryset(self):
        return ProjectMembership.objects.filter(project_id=self.kwargs['project_pk']).select_related('user')

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs['project_pk'])