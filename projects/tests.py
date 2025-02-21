from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from utils.roles import MembershipRole
from .models import Project, ProjectMembership, Comment


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.test_user = self.User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = self.User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.test_user)


class ProjectViewSetTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description'
        )
        self.membership = ProjectMembership.objects.create(
            user=self.test_user,
            project=self.project,
            role=MembershipRole.OWNER.value
        )

    def test_create_project(self):
        """Should create a new project and assign user as OWNER"""
        url = reverse('project-list')
        response = self.client.post(url, {
            'title': 'New Project',
            'description': 'New Description'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        self.assertTrue(ProjectMembership.objects.filter(
            user=self.test_user,
            role=MembershipRole.OWNER.value
        ).exists())

    def test_list_projects(self):
        """Should list all projects for authenticated user"""
        url = reverse('project-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_add_member(self):
        """Should allow OWNER to add a member to a project"""
        url = reverse('project-add-member', kwargs={'pk': self.project.pk})
        member_data = {
            'user': self.other_user.id,
            'role': MembershipRole.EDITOR.value
        }

        response = self.client.post(url, member_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ProjectMembership.objects.filter(
            user=self.other_user,
            project=self.project
        ).exists())


class CommentViewSetTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description'
        )
        self.membership = ProjectMembership.objects.create(
            user=self.test_user,
            project=self.project,
            role=MembershipRole.EDITOR.value
        )

    def test_create_comment(self):
        """Should create a comment on a project"""
        url = reverse('project-comment-list', kwargs={'project_pk': self.project.pk})
        response = self.client.post(url, {'content': 'Test Comment'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.test_user)

    def test_list_comments(self):
        """Should list all comments for a project"""
        Comment.objects.create(
            content='Test Comment',
            author=self.test_user,
            project=self.project
        )

        url = reverse('project-comment-list', kwargs={'project_pk': self.project.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
