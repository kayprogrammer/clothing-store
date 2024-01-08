from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),

    # EMAIL ACTIVATION
    path(
        "verify-email/<uidb64>/<token>/<user_id>/",
        views.VerifyEmail.as_view(),
        name="verify-email",
    ),
]
