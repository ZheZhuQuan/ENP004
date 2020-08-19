from allauth.account.forms import ResetPasswordForm
from django import forms
from .models import CustomUser
import logging

logger = logging.getLogger(__name__)

from __future__ import absolute_import
from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from allauth.utils import (
    build_absolute_uri,
)
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
# from allauth.account.app_settings import AuthenticationMethod
from allauth.account.utils import (
    user_pk_to_url_str,
    user_username,
)

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

    def clean_last_name(self):
        email = self.data.get('email')
        last_name = self.cleaned_data["last_name"]
        users = CustomUser.objects.filter(email__iexact=email).first()
        if users:
            if users.last_name != last_name:
                raise forms.ValidationError("該当アカウントがありません。--MyResetPasswordForm（姓）")
        return self.cleaned_data["last_name"]

    def clean_first_name(self):
        email = self.data.get('email')
        first_name = self.cleaned_data["first_name"]
        users = CustomUser.objects.filter(email__iexact=email).first()
        if users:
            if users.first_name != first_name:
                raise forms.ValidationError("該当アカウントがありません。--MyResetPasswordForm（名）")
        return self.cleaned_data["last_name"]


    # リライトsave
    def save(self, request, **kwargs):
        last_name = self.data.get('last_name')
        context = {"last_name": last_name, }
        super().save(self, request, **kwargs)

    
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]
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

            last_name = self.data.get('last_name')

            context = {"current_site": current_site,
                       "user": user,
                       "password_reset_url": url,
                       "request": request,
                       "last_name": last_name, }

            if app_settings.AUTHENTICATION_METHOD \
                    != AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key',
                email,
                context)
        return self.cleaned_data["email"]
        
