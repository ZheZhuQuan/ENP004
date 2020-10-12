# Log用
import logging

# リダイレクト、ビュー
from django.urls import reverse_lazy
from django.views import generic

# モデル
from .models import *
from accounts.models import CustomUser

# メッセージ用
from django.contrib import messages

# ログインを要求する用
from django.contrib.auth.mixins import LoginRequiredMixin

# 404、500など
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    """（仮）HP"""
    template_name = "index.html"


class EmployeeListView(generic.ListView):
    """社員一覧画面"""
    model = Profile
    template_name = "ENP001_employee_list.html"
    context_object_name = 'member_list'
    paginate_by = 6

    def get_queryset(self):
        profiles = Profile.objects.order_by('user_id')
        return profiles


class EmployeeView(generic.ListView, LoginRequiredMixin):
    """社員詳細画面"""
    model = Profile
    template_name = "ENP002_employee.html"
    context_object_name = 'member_list'

    def get_queryset(self):
        logger.info('ユーザー：{}'.format(self.request.user))
        profiles = Profile.objects.filter(id=self.request.user.id).first()

        return profiles

class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    """社員詳細画面編集"""
    model = Profile
    # slug_url_kwarg = "id"
    # slug_field =
    template_name = 'ENP002_employee.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('profile_app:profile')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)

        my_data = get_object_or_404(Profile, user=self.request.user)
        edit_data = self.kwargs['pk']
        logger.info("\n編集のユーザー：{}\nログインユーザー：{}".format(edit_data, my_data.id))
        if my_data.id != edit_data:
            logger.error("自分のプロフィールではない！！！")
            raise PermissionDenied

        # form_kwargs['initial'] = {'test2': my_data.species}
        return form_kwargs

    def form_valid(self, form):
        # 元々のソース
        form = form_save(self.request, form, 'プロフィール更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新が失敗しました。")
        return super().form_invalid(form)