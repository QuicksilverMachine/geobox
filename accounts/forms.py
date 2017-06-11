from django import forms
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm


class SignupForm(forms.Form):

    field_order = ['email', 'username', 'full_name', 'password1', 'password2']

    full_name = forms.CharField(
        required=True,
        min_length=1,
        max_length=255,
        label=_("Full name"),
        widget=TextInput(attrs={'placeholder': _('Full name')})
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.fields['email'].help_text = (
            _("You will use this e-mail to log in.")
        )
        self.fields['username'].help_text = (
            _("150 characters or fewer. Letters, digits"
              " and symbols @/./+/-/_ only.")
        )
        self.fields['password1'].min_length = 6
        self.fields['password2'].min_length = 6
        self.fields['password1'].help_text = (
            _("%(min)s characters or more.") %
            {'min': self.fields['password1'].min_length}
        )

    def signup(self, request, user):
        user.full_name = self.cleaned_data['full_name']
        user.save()


class LoginFormWithoutAutofocus(LoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginFormWithoutAutofocus, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.pop("autofocus", None)
