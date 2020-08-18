from allauth.account.forms import ResetPasswordForm
from .models import CustomUser
from django import forms
import logging

logger = logging.getLogger(__name__)


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
