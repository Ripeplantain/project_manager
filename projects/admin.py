from django.contrib import admin
from .models import Project, ProjectMembership, Comment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')

@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'project__title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'author', 'created_at')
    search_fields = ('content', 'author__username', 'project__title')
