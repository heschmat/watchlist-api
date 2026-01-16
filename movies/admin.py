from django.contrib import admin
from .models import Movie, Review, Favorite, Genre


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "created_at")
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "created_at")
    list_filter = ("movie",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "created_at")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
