"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from projects.views import (
    ProjectViewSet,
    ContributorViewSet,
    CommentViewSet,
    IssueViewSet,
)
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserViewSet, RegisterViewSet

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("projects", ProjectViewSet, basename="projects")

contributors_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
contributors_router.register(
    "contributors", ContributorViewSet, basename="contributors"
)

issues_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
issues_router.register("issues", IssueViewSet, basename="issues")

comments_router = routers.NestedSimpleRouter(issues_router, r"issues", lookup="issue")
comments_router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", include(router.urls)),
    path("", include(contributors_router.urls)),
    path("", include(issues_router.urls)),
    path("", include(comments_router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", RegisterViewSet.as_view({"post": "create"}), name="signup"),
    path(
        "projects/<int:pk>/subscription/",
        ProjectViewSet.as_view({"post": "project_subscription"}),
    ),
    path(
        "users/<int:pk>/delete_all_data/",
        UserViewSet.as_view({"delete": "delete_all_data"}),
    ),
]
