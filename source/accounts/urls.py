from django.urls import path

from .views import (
    LogInView, ResendActivationCodeView, RemindUsernameView, SignUpView, ActivateView, LogOutView,
    ChangeEmailView, ChangeEmailActivateView, ChangeProfileView, ChangePasswordView,
    RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView, LandingPageView, MyAccountPageView, PaymentSuccessView,
    PaymentFailedView, subscription_view, create_checkout_session, CancelSubscriptionView, CancelSubscriptionSuccessView, CancelSubscriptionFailedView
)

# from .main.views import IndexPageView

app_name = 'accounts'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/', LogOutView.as_view(), name='log_out'),
    path('landing-page/', LandingPageView.as_view(), name='landing_page'),

    path('my-account/', MyAccountPageView.as_view(), name='my_account'),

    path('resend/activation-code/', ResendActivationCodeView.as_view(),
         name='resend_activation_code'),

    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<code>/', ActivateView.as_view(), name='activate'),

    path('restore/password/', RestorePasswordView.as_view(),
         name='restore_password'),

    path('restore/password/done/', RestorePasswordDoneView.as_view(),
         name='restore_password_done'),
    path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(),
         name='restore_password_confirm'),

    path('remind/username/', RemindUsernameView.as_view(), name='remind_username'),

    path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('change/email/', ChangeEmailView.as_view(), name='change_email'),
    path('cancel/subscription/failed', CancelSubscriptionFailedView.as_view(),
         name='cancel_subscription_failed'),
    path('cancel/subscription/success', CancelSubscriptionSuccessView.as_view(),
         name='cancel_subscription_success'),
    path('cancel/subscription/', CancelSubscriptionView.as_view(),
         name='cancel_subscription'),
    path('change/email/<code>/', ChangeEmailActivateView.as_view(),
         name='change_email_activation'),

    # path('payment_processing/',PaymentProcessing.as_view(), name='processing'),
    path('checkout/success/', PaymentSuccessView.as_view(), name='success'),
    path('checkout/failed/', PaymentFailedView.as_view(), name='failed'),
    path('checkout/<int:subscription_id>/',
         create_checkout_session, name='create_checkout_session'),
    path('subscription/', subscription_view, name="subscription")
]
