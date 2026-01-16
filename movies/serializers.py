from rest_framework import serializers
from .models import Movie, Review, Favorite


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Review
        fields = (
            "id",
            "movie",
            "user_email",
            "text",
            "image",
            "rating",
            "created_at",
        )
        read_only_fields = ("movie",)
