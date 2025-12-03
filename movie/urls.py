from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_movies, name="get_movies"),

    path("post/", views.post_all_movie, name="post_all_movie"),

    path("recommend/", views.recommendations, name="recommend"),
    path("recommend2/", views.recommendations2, name="recommend2"),

    path("like/<int:movie_id>/", views.like_movie, name="like_movie"),
    path("unlike/<int:movie_id>/", views.unlike_movie, name="unlike_movie"),
]
