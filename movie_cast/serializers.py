from rest_framework import serializers
from .models import (
    Movie, Cast
)

Gender = (
    ("Male", "Male"),
    ("Female", "Female")
)


class MovieCreateSerializer(serializers.ModelSerializer):
    """
    class : Create the movie.
    """
    runtime = serializers.IntegerField(required=True)
    tagline = serializers.CharField(required=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)


class MovieListSerializer(serializers.ModelSerializer):
    """
    class : All movies.
    """
    class Meta:
        model = Movie
        fields = ["id", "title", "runtime", "language", "tagline", "created_at", "updated_at"]


class CastCreateSerializer(serializers.ModelSerializer):
    """
    class : Create cast based in movie object.
    """
    gender = serializers.ChoiceField(choices=Gender, required=True)

    class Meta:
        model = Cast
        fields = '__all__'

    def create(self, validated_data):
        return Cast.objects.create(**validated_data)
