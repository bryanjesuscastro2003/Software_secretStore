from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("authService.urls")),
    path("accounts/", include("allauth.urls")),
    path("dashboard/", include("dashboardService.urls")),
]
