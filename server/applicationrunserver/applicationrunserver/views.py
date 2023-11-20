from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount


def googleFeedback(request):
    social_account = SocialAccount.objects.get(user=request.user)
    print(social_account.extra_data)
    return render(request, 'auth/googleFeedback.html', {})

