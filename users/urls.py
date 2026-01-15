from django.urls import path
from .views import MeView, RegisterView, LoginView

urlpatterns = [
    path("me/", MeView.as_view()),
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
]
