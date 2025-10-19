"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from accounts.views import CustomRegisterView
from accounts.views import health_check


# ==========================
# Social Login Views
# ==========================
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter


# ==========================
# Swagger / API Schema
# ==========================
schema_view = get_schema_view(
    openapi.Info(
        title="Apra Nova Backend API",
        default_version="v1",
        description="Comprehensive API documentation for Apra Nova Django backend",
        contact=openapi.Contact(email="support@apranova.dev"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ==========================
# URL Patterns
# ==========================
urlpatterns = [
    # Redirect root ("/") → Swagger UI
    path("", RedirectView.as_view(url="/swagger/", permanent=False)),

    # Admin
    path("admin/", admin.site.urls),

    # Social auth endpoints
    path("api/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("api/auth/github/", GitHubLogin.as_view(), name="github_login"),

    # Swagger / ReDoc documentation
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),

    # Authentication & User APIs
    path("api/auth/registration/", CustomRegisterView.as_view(), name="custom_register"),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/social/", include("allauth.socialaccount.urls")),
    path("api/users/", include("accounts.urls")),
]
