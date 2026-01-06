import os
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from MovieAPIML import settings
from movie.models import Movie
from movie.serializer import MovieSerializer
from movie.utils.recommed import get_recommendations_from_liked


def get_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return render(request, "movie/index.html", {"movies": serializer.data})




def post_all_movie(request):
    excel_path = os.path.join(settings.BASE_DIR, "real_movies_sample1.xlsx")

    if not os.path.exists(excel_path):
        return HttpResponse("Excel file not found.", status=404)

    df = pd.read_excel(excel_path)

    for _, row in df.iterrows():
        Movie.objects.get_or_create(
            title=row["Title"],
            description=row["Description"],
            image_url=row["ImageUrl"]
        )

    return HttpResponse("Movies imported successfully!")


def recommendations(request):
    recs = get_recommendations_from_liked(request.user)
    return render(request, "movie/recommendationspages.html", {"movies": recs})



from django.http import JsonResponse
from movie.models import Movie
from movie.serializer import MovieSerializer


def like_movie(request, movie_id):
    liked = request.session.get("liked_movies", [])

    if movie_id not in liked:
        liked.append(movie_id)

    request.session["liked_movies"] = liked
    return JsonResponse({"message": "Movie liked!", "liked_movies": liked})


def unlike_movie(request, movie_id):
    liked = request.session.get("liked_movies", [])

    if movie_id in liked:
        liked.remove(movie_id)

    request.session["liked_movies"] = liked
    return JsonResponse({"message": "Movie unliked!", "liked_movies": liked})


def recommendations2(request):
    liked_ids = request.session.get("liked_movies", [])

    recs = get_recommendations_from_liked(liked_ids)

    serializer = MovieSerializer(recs, many=True)
    return render(request, "movie/recommendations.html", {"movies": serializer.data})



def clear_liked_movies(request):
    liked_ids = request.session.get("liked_movies", [])
    if liked_ids:
        del request.session["liked_movies"]

    return HttpResponse("Successfully cleared liked movies!")


def movie_details(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    serializer = MovieSerializer(movie)
    return render(request, "movie/detail.html", {"movie": serializer.data})