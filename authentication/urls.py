from django.urls import path

from .views import AuthViewSet

urlpatterns = [
    path("login/", AuthViewSet.as_view({"post": "login"}), name="login"),
    path("logout/", AuthViewSet.as_view({"post": "logout"}), name="logout"),
    path("register/", AuthViewSet.as_view({"post": "register"}), name="register"),
]