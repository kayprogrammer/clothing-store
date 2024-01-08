from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from apps.accounts.models import User
from .senders import SendEmail, email_verification_generate_token
from .forms import LoginForm, RegisterForm


class RegisterView(View):
    def get(self, request):
        print(request.get_host())
        form = RegisterForm()
        context = {"form": form}
        return render(request, "accounts/register.html", context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "accounts/email-verification-request.html")
        context = {"form": form}
        return render(request, "accounts/register.html", context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request, "accounts/login.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if not user:
                messages.error(request, "Invalid Credentials")
                return redirect("login")
            login(request, user)
            return redirect("/")
        context = {"form": form}
        return render(request, "accounts/login.html", context)

class VerifyEmail(View):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs['uid']
        token = kwargs['token']
        user_id = kwargs['user_id']
        try:
            user_obj = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "You entered an invalid link")
            return redirect(reverse("login"))

        try:
            uid = force_str(urlsafe_base64_decode(kwargs.get("uidb64")))
            user = User.objects.get(id=uid)
        except Exception as e:
            user = None

        if user:
            if user.id != user_obj.id:
                messages.error(request, "You entered an invalid link")
                return redirect(reverse("login"))

            if email_verification_generate_token.check_token(user, kwargs["token"]):
                user.is_email_verified = True
                user.save()
                messages.success(request, "Verification successful!")
                # request.session["activation_email"] = None
                SendEmail.welcome(request, user)
                return redirect(reverse("login"))
            
        return render(
            request, "accounts/email-activation-failed.html", {"email": user_obj.email}
        )