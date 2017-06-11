from allauth.account import views
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import UpdateView
from accounts.forms import LoginFormWithoutAutofocus
from accounts.models import User
from map.models import Map


def profile_view(request, username):
    webapp_user = get_object_or_404(User, username=username)
    user_maps = Map.objects.filter(user=webapp_user)
    return render(request, 'accounts/profile.html',
                  {'webapp_user': webapp_user,
                   'user_maps': user_maps})


class UserUpdate(UpdateView):
    model = User
    fields = ['full_name', 'profile_picture']
    slug_field = 'username'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        if self.request.is_ajax():
            return HttpResponse(user.get_absolute_url())
        else:
            return super(UserUpdate, self).form_valid(form)

    def get_object(self, queryset=None):
        user = super(UserUpdate, self).get_object()
        if not user == self.request.user and not self.request.user.is_staff:
            raise Http404
        return user


class AccountInactiveView(views.AccountInactiveView):
    template_name = 'accounts/account_inactive.html'


class EmailView(views.EmailView):
    template_name = 'accounts/email.html'


class ConfirmEmailView(views.ConfirmEmailView):
    template_name = 'accounts/email_confirm.html'


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginFormWithoutAutofocus


class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'accounts/password_change.html'


class PasswordResetView(views.PasswordResetView):
    template_name = 'accounts/password_reset.html'


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetFromKeyView(views.PasswordResetFromKeyView):
    template_name = 'accounts/password_reset_from_key.html'


class PasswordResetFromKeyDoneView(views.PasswordResetFromKeyDoneView):
    template_name = 'accounts/password_reset_from_key_done.html'


class PasswordSetView(views.PasswordSetView):
    template_name = 'accounts/password_set.html'


class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'


class EmailVerificationSentView(views.EmailVerificationSentView):
    template_name = 'accounts/verification_sent.html'
