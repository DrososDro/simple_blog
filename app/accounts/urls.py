from django.urls import path
from accounts import views


urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_urer, name="logout"),
    path("register/", views.register_user, name="register"),
]
