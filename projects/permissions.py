from rest_framework import permissions

from projects.models import ProjectMembership, Project

class ProjectPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        try:
            membership = ProjectMembership.objects.get(
                user=request.user,
                project=obj
            )
        except ProjectMembership.DoesNotExist:
            return False

        if request.method in permissions.SAFE_METHODS:
            return membership.role in ['OWNER', 'EDITOR', 'READER']
        elif request.method in ['PUT', 'PATCH']:
            return membership.role in ['OWNER', 'EDITOR']
        elif request.method == 'DELETE':
            return membership.role == 'OWNER'
        return False

class CommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        project_id = view.kwargs.get('project_pk')
        try:
            membership = ProjectMembership.objects.get(
                user=request.user,
                project_id=project_id
            )
            return membership.role in ['OWNER', 'EDITOR']
        except ProjectMembership.DoesNotExist:
            return False
        
class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        project_id = view.kwargs.get('project_pk')
        try:
            membership = ProjectMembership.objects.get(
                user=request.user,
                project_id=project_id
            )
            return membership.role in ['OWNER', 'EDITOR']
        except ProjectMembership.DoesNotExist:
            return False