from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import RedirectView
from profiles import views as profile_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", profile_views.auth_page, name="login"),
    path("accounts/register/", RedirectView.as_view(url="/accounts/login/", permanent=False)),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", RedirectView.as_view(url="/accounts/login/", permanent=False)),
    path("profile/", include("profiles.urls")),
    path("symptoms/", include("symptoms.urls")),
]