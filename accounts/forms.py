from __future__ import absolute_import
from allauth.account.forms import ResetPasswordForm,EmailAwarePasswordResetTokenGenerator
from django import forms
from .models import CustomUser
import logging

logger = logging.getLogger(__name__)

# リライトclean_email
from allauth.account.utils import (
    filter_users_by_email,
)

# リライトsave
from django import forms
from django.urls import reverse

from allauth.utils import build_absolute_uri
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import (
    user_pk_to_url_str,
    user_username,
)

default_token_generator = EmailAwarePasswordResetTokenGenerator()


class MyResetPasswordForm(ResetPasswordForm):
    last_name = forms.CharField(label='姓', required=True, )
    first_name = forms.CharField(label='名', required=True, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # col-widget
        self.fields['last_name'].widget.attrs['maxlength'] = '15'
        self.fields['last_name'].widget.attrs['placeholder'] = '田中'
        self.fields['first_name'].widget.attrs['maxlength'] = '15'
        self.fields['first_name'].widget.attrs['placeholder'] = '太郎'

    def clean(self):
            email = self.data.get('email')
            last_name = self.data.get('last_name')
            first_name = self.data.get('first_name')
            self.users = filter_users_by_email(email, is_active=True)
            users = CustomUser.objects.filter(email__iexact=email, is_active=True).first()

            if users:
                if users.last_name != last_name or users.first_name != first_name:
                    raise forms.ValidationError("該当するアカウントが見つかりません。")
            else:
                raise forms.ValidationError("該当するアカウントが見つかりません。")

    # リライト
    def clean_email(self):
        return self.cleaned_data["email"]

    # リライト
    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        last_name = self.data.get('last_name')
        token_generator = kwargs.get("token_generator",
                                     default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse("account_reset_password_from_key",
                           kwargs=dict(uidb36=user_pk_to_url_str(user),
                                       key=temp_key))
            url = build_absolute_uri(
                request, path)

            context = {
                "last_name": last_name,
                "password_reset_url": url,
            }

            if app_settings.AUTHENTICATION_METHOD \
                    != 'email':
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key',
                email,
                context)
        return self.cleaned_data["email"]
