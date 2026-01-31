from django.conf import settings
from django.db import models

from core.validators import validate_image_file

User = settings.AUTH_USER_MODEL


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to="movies/posters/", validators=[validate_image_file])
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genres = models.ManyToManyField("Genre", related_name="movies", blank=True)

    def __str__(self):
        return f'{self.title} ({self.release_date.year if self.release_date else "N/A"})'


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    image = models.ImageField(
        upload_to="movies/reviews/",
        validators=[validate_image_file],
        null=True,
        blank=True,
    )
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "user"],
                name="one_review_per_user_per_movie",
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.movie}"


class Favorite(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "user"],
                name="one_favorite_per_user_per_movie",
            )
        ]
    def __str__(self):
        return f"{self.user} ❤ {self.movie}"


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # ⚠️ A ManyToMany relationship must be defined on ONE side only.
    # movies = models.ManyToManyField(Movie, related_name="genres")

    def __str__(self):
        return self.name
