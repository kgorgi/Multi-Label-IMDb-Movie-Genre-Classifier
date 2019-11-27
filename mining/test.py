import json
import math

import movie_synopsis

OUTPUT_STATS = True

def calculate_score(model, movie):
    priorProb = model["priorProb"]
    condProb = model["condProb"]
    
    score = dict()
    # Initialize score with log(prior)
    for classification in movie_synopsis.classifications:
        # Set initial score to ratio between documents in classification and all documents
        score[classification] = math.log(priorProb[classification])
        # Go through each term in data we want to classify
        for term in movie.text_arr:
            # Term may not have been classified yet!
            if term in condProb and classification in condProb[term]:
                score[classification] += math.log(condProb[term][classification])
    return score

def calculate_class(score):
    if score[movie_synopsis.is_genre_class] > score[movie_synopsis.is_not_genre_class]:
        return movie_synopsis.is_genre_class
    else:
        return movie_synopsis.is_not_genre_class
  
def apply_models(models, movie):
    movie_genres = set()

    for genre in models.keys():
        score = calculate_score(models[genre], movie)
        if calculate_class(score) == movie_synopsis.is_genre_class:
            movie_genres.add(genre)

    return movie_genres

def print_stats(movies, genres, predicted_genres):
    for genre in genres:
        correct_classifications = 0

        for movie in movies:
            if movie.has_genre(genre) and genre in predicted_genres[movie.id]:
                correct_classifications += 1
            elif not movie.has_genre(genre) and genre not in predicted_genres[movie.id]:
                correct_classifications += 1

        print("Accuracy for " + genre + " : " + str(correct_classifications/len(movies)) + "%")

    pred_counts = list()
    for genres in predicted_genres.values():
        pred_counts.append(len(genres))
    print("Average number of genres predicted per movie: "  + str(sum(pred_counts)/len(pred_counts)))

    actual_counts = list()
    for movie in movies:
        actual_counts.append(len(movie.genres))
    print("Average number of actual genres per movie: " + str(sum(actual_counts)/len(actual_counts)))

def main():
    models_json = None
    with open('./models.json') as models_file:
        models_json = models_file.read()
    
    models = json.loads(models_json)    
    movies, genres = movie_synopsis.read_file('../data/train_movies.txt')

    # Key: movie_id, Value: List of genres
    predicted_genres = dict()
    for movie in movies:
        predicted_genres[movie.id] = apply_models(models, movie)

    correct = 0
    total = 0
    for movie in movies:
        for genre in genres:
            if movie.has_genre(genre) and genre in predicted_genres[movie.id]:
                correct += 1
            elif not movie.has_genre(genre) and genre not in predicted_genres[movie.id]:
                correct += 1
            total += 1

    print("Overall Accuracy : " + str(correct/(total) * 100) + "%")

    if OUTPUT_STATS:
        print_stats(movies, genres, predicted_genres)
    

if __name__ == "__main__":
    main()