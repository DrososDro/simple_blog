from django.urls import path, include
from api import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("blog-posts", views.BlogPostViewSet)
router.register("my-blog-posts", views.MyBlogPostViewSet)


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs",
    ),
    path(
        "token/",
        views.CreateTokenView.as_view(),
        name="token",
    ),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("", include(router.urls)),
]
