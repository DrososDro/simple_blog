from api.serializers import AuthTokenSerializer, UserSerializer, BlogPostsSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from blog_posts.models import BlogPost


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CreateUserView(generics.CreateAPIView):
    """Create new User"""

    serializer_class = UserSerializer


class BlogPostViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Public API for all Blog Posts."""

    serializer_class = BlogPostsSerializer
    queryset = BlogPost.objects.all()


class MyBlogPostViewSet(viewsets.ModelViewSet):
    """A user can manage Every Blog Posts that he have made."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostsSerializer
    queryset = BlogPost.objects.all()

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)
