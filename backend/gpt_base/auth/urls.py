from django.urls import path

from gpt_base.auth.views.view_api import (
    reset_password, forgot_password, change_password, get_me, verify_email, change_email_login,
    confirm_change_email_login, check_verify_token, resend_verify_email, check_session
)
from gpt_base.auth.views.view_set import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('token', CustomTokenObtainPairView.as_view()),
    path('token/refresh', CustomTokenRefreshView.as_view()),
    # path('forgot-password', forgot_password),
    # path('reset-password', reset_password),
    path('change-password', change_password),
    path('me', get_me),
    # path('verify-email', verify_email),
    # path('verify-email/resend', resend_verify_email),
    # path('change-email', change_email_login),
    # path('change-email/confirm', confirm_change_email_login),
    # path('verify-token/check', check_verify_token),
    path('session', check_session),
]
