from django.contrib import admin

from movie_cast.models import (
    Movie, Cast
)

# Register your models here.

admin.site.register(Movie)
admin.site.register(Cast)
