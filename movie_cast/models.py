from django.db import models

Gender = (
    ("Male", "Male"),
    ("Female", "Female")
)


class Movie(models.Model):
    """
    Create a movie table.
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    runtime = models.IntegerField(default=0)
    language = models.CharField(max_length=255, null=False, blank=False)
    tagline = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movie"
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["title"])
        ]


class Cast(models.Model):
    """
    Create a cast table and this table is connected with the movie table.
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    gender = models.CharField(max_length=10, choices=Gender, default="Male")
    publish_date = models.DateField()
    movie = models.ForeignKey(
        "Movie", on_delete=models.CASCADE, related_name="movie_cast", db_index=True
    )

    class Meta:
        db_table = "cast"
        verbose_name = "Cast"
        verbose_name_plural = "Casts"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["movie"])
        ]
