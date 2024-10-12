from pprint import pprint

from allauth.account.forms import (
    SignupForm,
    LoginForm,
    AddEmailForm,
    ChangePasswordForm,
    SetPasswordForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    UserTokenForm,
)
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.socialaccount.forms import DisconnectForm
from allauth.mfa.base.forms import AuthenticateForm, ReauthenticateForm
from allauth.mfa.totp.forms import ActivateTOTPForm, DeactivateTOTPForm
from django.contrib.auth import forms as admin_forms
from django import forms
from django.forms import EmailField, CharField, ImageField
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField, "username": CharField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = (
            "email",
            "username",
        )
        field_classes = {"email": EmailField, "username": CharField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
            "username": {"unique": _("This username has already been taken.")},
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "images",
        )
        field_classes = {
            "email": EmailField,
            "username": CharField,
            "first_name": CharField,
            "last_name": CharField,
            "images": ImageField,
        }
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
            "username": {"unique": _("This username has already been taken.")},
        }

    def clean_username(self):
        return self.cleaned_data["username"].strip()

    def clean_images(self):
        return self.cleaned_data["images"]

    def clean_email(self):
        if self.cleaned_data["email"] == "":
            self.add_error("email", 'The field "Email" is required.')
        else:
            return self.cleaned_data["email"].strip()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self):
        user = super().save()
        user.images = self.cleaned_data["images"]
        pprint(user.images)
        user.save()
        return user


class UserSignupForm(SignupForm):
    # add form fields here
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    # add form fields here
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class MyCustomLoginForm(LoginForm):
    # add form fields here
    def login(self, *args, **kwargs):
        return super().login(*args, **kwargs)


class MyCustomAddEmailForm(AddEmailForm):
    # add form fields here
    def save(self, request):
        email_address_obj = super().save(request)
        return email_address_obj


class MyCustomChangePasswordForm(ChangePasswordForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomSetPasswordForm(SetPasswordForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomResetPasswordForm(ResetPasswordForm):
    # add form fields here
    def save(self, request):
        email_address = super().save(request)
        return email_address


class MyCustomResetPasswordKeyForm(ResetPasswordKeyForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomSocialDisconnectForm(DisconnectForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomReauthenticateForm(ReauthenticateForm):
    # add form fields here
    def save(self):
        super(MyCustomAuthenticateForm, self).save()


class MyCustomAuthenticateForm(AuthenticateForm):
    # add form fields here
    def save(self):
        super(MyCustomReauthenticateForm, self).save()


class MyCustomActivateTOTPForm(ActivateTOTPForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomUserTokenForm(UserTokenForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomDeactivateTOTPForm(DeactivateTOTPForm):
    # add form fields here
    def save(self):
        super().save()
