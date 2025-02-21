from rest_framework import serializers
from .models import Project, ProjectMembership, Comment
from authentication.serializers import UserSerializer
from django.contrib.auth import get_user_model


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']

class ProjectMembershipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )
        
    class Meta:
        model = ProjectMembership
        fields = ['id', 'user', 'role']
        read_only_fields = ['project']
        extra_kwargs = {
            'user': {'required': True}
        }

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author_username']
        read_only_fields = ['author']