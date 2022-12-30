from django.urls import path
from movie_cast import views

urlpatterns = [
    path('movie/create', views.MovieCreateView.as_view(), name='movie_create'),
    path('movie/list', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<int:id>', views.MovieDetailsView.as_view(), name='movie_details'),
    path('cast/create', views.CastCreateView.as_view(), name='cast_create'),
]
