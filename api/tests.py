from django.test import TestCase
from .models import Movie, Actor, Cast
from datetime import date

class ModelTests(TestCase):
    """Tests for models logic and relationships."""

    def setUp(self):
        # Create test movie
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="A test movie description",
            year_of_release=2023,
            budget=1000000.00,
            box_office=5000000.00,
            director="Test Director",
            script_writer="Test Writer",
            cinematographer="Test Cinematographer"
        )

        # Create test actor
        self.actor = Actor.objects.create(
            name="Test Actor",
            date_of_birth=date(1990, 1, 1)
        )

        # Create cast relationship
        self.cast = Cast.objects.create(
            actor=self.actor,
            movie=self.movie,
            character_name="Test Character"
        )

    def test_movie_model(self):
        """Test movie model string representation and fields."""
        self.assertEqual(str(self.movie), "Test Movie")
        self.assertEqual(self.movie.director, "Test Director")
        self.assertEqual(self.movie.year_of_release, 2023)

    def test_actor_model(self):
        """Test actor model string representation and fields."""
        self.assertEqual(str(self.actor), "Test Actor")
        self.assertEqual(self.actor.date_of_birth, date(1990, 1, 1))

    def test_cast_model(self):
        """Test cast model string representation and relationships."""
        self.assertEqual(str(self.cast), "Test Actor as Test Character in Test Movie")
        self.assertEqual(self.cast.actor, self.actor)
        self.assertEqual(self.cast.movie, self.movie)

    def test_actor_movies_relationship(self):
        """Test the many-to-many relationship between actors and movies."""
        self.assertIn(self.movie, self.actor.movies.all())
        self.assertIn(self.actor, self.movie.actors.all())