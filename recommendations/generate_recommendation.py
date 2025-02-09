import cosine_similarity_recommendations, pearson_correlation_recommendations
from items_ratings_treated import items, ratings
from user_rating_matrix import rating_matrix
from thefuzz import fuzz, process

types_of_algorithms = ["Pearson Correlation Coefficient", "Cosine Similarity"]

if __name__ == "__main__":
    print("Options: ", end="")
    for type in types_of_algorithms:
        print(type, end=" ")
    print()
    option = input("Choose the algo that will be used to generate recommendations: ")
    result = process.extractOne(option, types_of_algorithms)[0]

    movie = process.extractOne(input("What's the movie you want to generate recommendations for?\n"), items["title"])[0]

    print(f"Generating recommendations using {result} for the movie {movie}...")

    movieId = items[items['title'] == movie]['movieId'].iloc[0]

    if result == "Pearson Correlation Coefficient":
        recommendations = pearson_correlation_recommendations.generate_recommendation(rating_matrix=rating_matrix, movieId=movieId)
    elif result == "Cosine Similarity":
        recommendations = cosine_similarity_recommendations.generate_recommendations(rating_matrix=rating_matrix, movieId=movieId)

    for recommendation in recommendations:
        print(recommendation)