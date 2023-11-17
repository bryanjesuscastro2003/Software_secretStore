from django.urls import path
from . import views


urlpatterns = [
    # Your URL patterns here
    path('signUp/', views.signUpService, name='SIGNUPSERVICE'),


]
