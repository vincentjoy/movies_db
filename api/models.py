from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year_of_release = models.IntegerField()
    thumbnail = models.ImageField(upload_to='movie_thumbnails/', null=True, blank=True)

    # Additional fields for movie details
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    box_office = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    director = models.CharField(max_length=100, null=True, blank=True)
    script_writer = models.CharField(max_length=100, null=True, blank=True)
    cinematographer = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Actor(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    movies = models.ManyToManyField(Movie, through='Cast', related_name='actors')

    def __str__(self):
        return self.name

class Cast(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('actor', 'movie')

    def __str__(self):
        return f"{self.actor.name} as {self.character_name} in {self.movie.title}"