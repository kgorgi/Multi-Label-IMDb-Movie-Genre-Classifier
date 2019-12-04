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
    pred_counts = list()
    for movie_genres in predicted_genres.values():
        pred_counts.append(len(movie_genres))
    
    pred_average_number_of_genres = sum(pred_counts)/len(pred_counts)
    print("Average number of genres predicted per movie: {:.2f}".format(pred_average_number_of_genres))

    actual_counts = list()
    for movie in movies:
        actual_counts.append(len(movie.genres))
    
    average_number_of_genres = sum(actual_counts)/len(actual_counts)
    print("Average number of genres per movie: {:.2f}".format(average_number_of_genres))

    print("Individual Genre Classifier Accuracies: ")
    for genre in genres:
        correct_classifications = 0

        for movie in movies:
            if movie.has_genre(genre) and genre in predicted_genres[movie.id]:
                correct_classifications += 1
            elif not movie.has_genre(genre) and genre not in predicted_genres[movie.id]:
                correct_classifications += 1

        accuracy = correct_classifications/len(movies) * 100
        print("\t{:<12}{:.2f}%".format(genre + ": ", accuracy))


def main():
    models_json = None
    with open('./model.json') as models_file:
        models_json = models_file.read()
    
    models = json.loads(models_json)    
    movies, test_genres = movie_synopsis.read_file('../data/test_movies.txt')

    genres = list(models.keys())
    genres.sort()

    # Key: movie_id, Value: List of genres
    predicted_genres = dict()
    for movie in movies:
        predicted_genres[movie.id] = apply_models(models, movie)

    prediction_correctness = list()
    incorrect_labels = 0
    for movie in movies:
        correct = 0
        for genre in genres:
            if movie.has_genre(genre) and genre in predicted_genres[movie.id]:
                correct += 1
            elif not movie.has_genre(genre) and genre not in predicted_genres[movie.id]:
                correct += 1
            else: 
                incorrect_labels += 1
        
        prediction_correctness.append(correct/len(genres))

    accuracy = sum(prediction_correctness) / len(movies) * 100
    print("Overall Accuracy: {:.2f}%".format(accuracy))
    

    hamming_loss = incorrect_labels / (len(movies) * len(genres))
    print("Hamming Loss Ratio: {:.4f}".format(hamming_loss))

    if OUTPUT_STATS:
        print_stats(movies, genres, predicted_genres)
    

if __name__ == "__main__":
    main()