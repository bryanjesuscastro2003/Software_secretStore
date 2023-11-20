from django.urls import path
from . import views

urlpatterns = [
    path('signUp/', views.signUpService, name='SIGNUPSERVICE'),
    path('signIn/', views.signInService, name='SIGNINSERVICE'),
    path('logout/', views.logoutService, name="LOGOUTSERVICE"),
    path('activateAccount/<str:token>/', views.activateAccountService, name='ACTIVATEACCOUNTSERVICE'),
    path("account/resendActivator/", views.resendActivatorService, name="RESENDACTIVATORSERVICE"), 
    path("account/forgetPassword/", views.forgetPasswordStep1Service, name="FORGETPASSWORDST1SERVICE"),
    path("account/forgetPassword/<str:token>/", views.forgetPasswordStep2Service, name="FORGETPASSWORDST2SERVICE" ), 
    path("accounts/inactive/", views.googleFeedback, name="account_inactive" ), 
] 
