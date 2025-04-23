from rest_framework import serializers
from .models import Movie, Actor, Cast

class MovieListSerializer(serializers.ModelSerializer):
    """Serializer for movie list view with limited fields"""
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'year_of_release', 'thumbnail')

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'date_of_birth')

class CastSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.name', read_only=True)
    actor_dob = serializers.DateField(source='actor.date_of_birth', read_only=True)

    class Meta:
        model = Cast
        fields = ('id', 'actor_name', 'actor_dob', 'character_name')

class MovieDetailSerializer(serializers.ModelSerializer):
    """Serializer for movie detail view with all fields and cast information"""
    cast = CastSerializer(source='cast_set', many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'description', 'year_of_release', 'thumbnail',
            'budget', 'box_office', 'director', 'script_writer',
            'cinematographer', 'cast'
        )

# For creating and editing actors
class ActorDetailSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ('id', 'name', 'date_of_birth', 'movies')