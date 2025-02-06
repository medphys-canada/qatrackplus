from django.conf import settings
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from django.urls import path

from qatrack.accounts import views
from qatrack.qatrack_core.views import handle_404

urlpatterns = [
    path('ping/', views.ping, name="ping_server"),
    path('logout/', auth_views.LogoutView.as_view(), name="auth_logout"),
    path('details/', views.AccountDetails.as_view(), name="account-details"),

    path('groups/', views.GroupsApp.as_view(), name="groups-app"),
]

if settings.ACCOUNTS_PASSWORD_RESET:
    urlpatterns += [
        path('password/change/', views.ChangePasswordView.as_view(), name="account-change-password"),
        re_path(
            r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.ResetPasswordConfirmView.as_view(),
            name='account-password-reset-confirm'
        ),
    ]

if settings.ACCOUNTS_SELF_REGISTER:
    urlpatterns += [
        path('register/', views.RegisterView.as_view(), name="account-register"),
    ]
else:
    urlpatterns += [
        path('register/', handle_404, name="account-register"),
    ]

if settings.USE_ADFS:
    urlpatterns.append(path('oauth2/callback', views.QATrackOAuth2CallbackView.as_view(), name="oauth-callback"))
    urlpatterns.append(path('oauth2/', include('django_auth_adfs.urls')))

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
    path('', include('django_registration.backends.one_step.urls')),
]
