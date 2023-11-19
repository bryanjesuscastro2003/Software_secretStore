from django.urls import path
from . import views

urlpatterns = [
    # Your URL patterns here
    path('signUp/', views.signUpService, name='SIGNUPSERVICE'),
    path('signIn/', views.signInService, name='SIGNINSERVICE'),
    path('activateAccount/<str:token>/', views.activateAccountService, name='ACTIVATEACCOUNTSERVICE'),
    path("account/resendActivator/", views.resendActivatorService, name="RESENDACTIVATORSERVICE")
]
