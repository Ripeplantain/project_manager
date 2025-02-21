from rest_framework import permissions, viewsets, status, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.core.validators import EmailValidator
from authentication.serializers import UserSerializer



class AuthViewSet(viewsets.ViewSet):
    renderer_classes = [renderers.JSONRenderer]
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def users(self, request):
        user_model = get_user_model()
        users = user_model.objects.all()
        return Response(self.serializer_class(users, many=True).data)

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            )
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def logout(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def register(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if email:
            email_validator = EmailValidator()
            try:
                email_validator(email)
            except ValidationError:
                return Response({"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)

        user_model = get_user_model()
        try:
            user = user_model.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
