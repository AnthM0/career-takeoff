from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("resumeEngine/", views.resume_engine, name="resume_engine"),
]