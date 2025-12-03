import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from movie.models import Movie

def get_recommendations_from_liked(liked_ids):
    if not liked_ids:
        return []

    all_movies = Movie.objects.all()
    df = pd.DataFrame(list(all_movies.values("id", "title", "description")))

    df["description"] = df["description"].fillna("")

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(df["description"])

    sim_matrix = cosine_similarity(tfidf)

    rec_movies = set()

    for liked_id in liked_ids:
        idx = df.index[df["id"] == liked_id][0]
        similarity_scores = list(enumerate(sim_matrix[idx]))

        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        for movie_idx, score in similarity_scores[1:6]:
            rec_movies.add(df.iloc[movie_idx]["id"])

    rec_movies = rec_movies - set(liked_ids)

    return Movie.objects.filter(id__in=rec_movies)
