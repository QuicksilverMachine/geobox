from django.conf.urls import url, include
from accounts import views


urlpatterns = [
    # Account
    url(r'^profile/(?P<username>[\w.@+-]+)/$',
        views.profile_view,
        name="account_profile"),
    url(r'^profile/edit/(?P<slug>[\w.@+-]+)/$',
        views.UserUpdate.as_view(),
        name='account_edit'),
    url(r'^login/$',
        views.LoginView.as_view(),
        name="account_login"),
    url(r'^signup/$',
        views.SignupView.as_view(),
        name="account_signup"),
    url(r'^logout/$',
        views.LogoutView.as_view(),
        name="account_logout"),
    url(r'^password/change/$',
        views.PasswordChangeView.as_view(),
        name="account_change_password"),
    url(r'^password/set/$',
        views.PasswordSetView.as_view(),
        name="account_set_password"),
    url(r'^inactive/$',
        views.AccountInactiveView.as_view(),
        name="account_inactive"),

    # E-mail
    url(r'^email/$',
        views.EmailView.as_view(),
        name="account_email"),
    url(r'^confirm-email/$',
        views.EmailVerificationSentView.as_view(),
        name="account_email_verification_sent"),
    url(r'^confirm-email/(?P<key>\w+)/$',
        views.ConfirmEmailView.as_view(),
        name="account_confirm_email"),

    # Password reset
    url(r'^password/reset/$',
        views.PasswordResetView.as_view(),
        name="account_reset_password"),
    url(r'^password/reset/done/$',
        views.PasswordResetDoneView.as_view(),
        name="account_reset_password_done"),
    url(r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        views.PasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key"),
    url(r'^password/reset/key/done/$',
        views.PasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done"),

    url(r'^', include('allauth.urls')),
]
