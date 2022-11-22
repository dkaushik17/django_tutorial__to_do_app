"""
core URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from core import views

urlpatterns = [

    # Admin site url
    path(
        route='admin/',
        view=admin.site.urls,
        name="admin-site"
    ),

    # ============================= Demo APIs ============================== #

    # API 101
    path(
        route='hello-world',
        view=views.hello_world,
        name="hello-world"
    ),
    path(
        route='hello/<slug:user>/<int:num>',
        view=views.hello_user,
        name="hello-user"
    ),

    # ========================== Version 1 APIs =========================== #
    # REST API 101
    # Version 1 APIs
    # These APIs use function based views
    path(
        route='api/v1/',
        view=include("todos.api.v1.urls")
    ),

    # ========================== Version 2 APIs =========================== #

    # # Version 2 APIs
    # # These APIs use serializers classes for for validation & serialization,
    # # pagination clases for pagination and filterset clases for filtering.
    path(
        route='api/v2/',
        view=include("todos.api.v2.urls")
    ),

    # ========================== Version 3 APIs =========================== #

    # # Version 3 APIs
    # # These APIs use GenericAPIView and GenericViewset
    path(
        route='api/v3/',
        view=include("todos.api.v3.urls")
    ),

    # ========================== Version 4 APIs =========================== #

    # # Version 4 APIs
    # # These APIs use mixins
    path(
        route='api/v4/',
        view=include("todos.api.v4.urls")
    ),

    # # Auth APIs
    path(
        route='api/token/',
        view=jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        route='api/token/refresh/',
        view=jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'
    ),

]
