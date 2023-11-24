from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import User
from django.utils.translation import gettext_lazy as _

from apps.accounts.validators import validate_name


class RegisterForm(UserCreationForm):
    error_messages = {
        "password_mismatch": _("Password Mismatch"),
    }
    first_name = forms.CharField(
        validators=[validate_name],
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name"}),
    )
    last_name = forms.CharField(
        validators=[validate_name],
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name"}),
    )
    email = forms.EmailField(
        error_messages={"unique": _("Email already registered")},
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password again"}),
    )
    terms_agreement = forms.BooleanField(
        label="I agree to the terms and conditions",
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "terms_agreement",
        ]

    def _post_clean(self):
        super(RegisterForm, self)._post_clean()
        password1 = self.cleaned_data["password1"]
        if len(password1) < 8:
            self.add_error("password1", "Password too short")


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
    )
