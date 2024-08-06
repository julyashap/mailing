import secrets

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView
from config import settings
from users.forms import RegistrationForm
from users.models import User
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            token = secrets.token_hex(8)
            user.token = token
            user.save()
            host = self.request.get_host()
            url = f'http://{host}/users/email-confirm/{token}/'
            send_mail(
                'Подтверждение почты MailServ',
                f'Здравствуйте! Чтобы зарегистрироваться, перейдите, пожайлуста, по ссылке:\n\n{url}',
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            return super().form_valid(form)


def email_confirm(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return render(request, 'users/email_confirm.html')


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'


@permission_required('users.can_change_is_active')
def user_blocking(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    return redirect(reverse('users:user_list'))


@permission_required('users.can_change_is_active')
def user_unblocking(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    return redirect(reverse('users:user_list'))
