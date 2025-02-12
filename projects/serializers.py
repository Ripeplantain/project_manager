from rest_framework import serializers
from .models import Project, ProjectMembership, Comment
from authentication.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']

class ProjectMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProjectMembership
        fields = ['id', 'user', 'project', 'role']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author_username']
        read_only_fields = ['author']