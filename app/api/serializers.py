from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from blog_posts.models import BlogPost


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = "Unable to authenticate with provided credentials."

            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 7}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class BlogPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"
        read_only_fields = ["created_at", "id", "author"]

    def create(self, validated_data):
        return BlogPost.objects.create(
            author=self.context["request"].user,
            **validated_data,
        )
