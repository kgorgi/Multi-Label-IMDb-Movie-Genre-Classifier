import json

import movie_synopsis

def classify_movies(movies, genre):
    movies_in_genre = dict()
    movies_in_genre[movie_synopsis.is_genre_class] = list()
    movies_in_genre[movie_synopsis.is_not_genre_class] = list()

    for movie in movies:
        if movie.has_genre(genre):
            movies_in_genre[movie_synopsis.is_genre_class].append(movie)
        else:
            movies_in_genre[movie_synopsis.is_not_genre_class].append(movie)
  
    return movies_in_genre

def get_words(movies):
    words = set()
    for movie in movies:
        for word in movie.text_arr:
            if not word in words:
                    words.add(word)
    return words

def count_unique_words(movies):
    unique_term_counts = dict()
    for movie in movies:
        for term in movie.text_arr:
            if term in unique_term_counts:
                unique_term_counts[term] += 1
            else:
                unique_term_counts[term] = 1
    return unique_term_counts

def count_words(movies):
    count = 0
    for movie in movies:
        count += len(movie.text_arr)
       
    return count

def train_model(movies, genre):
    condProb = dict()
    priorProb = dict()

    movies_in_genre = classify_movies(movies, genre)
    unique_words = get_words(movies)
    classification_count = len(movies_in_genre.keys())

    for classification in movie_synopsis.classifications:
        # Append the ratio between documents in classification and all documents
        priorProb[classification] = len(movies_in_genre[classification])/len(movies)
        unique_word_counts = count_unique_words(movies_in_genre[classification])
        word_count = count_words(movies_in_genre[classification])

        for term in unique_words:
            # If not within classification assign an initial probability of 0
            if term in unique_word_counts:
                term_count = unique_word_counts[term]
            else:
                term_count = 0    
            
            probability = (term_count + 1) / (len(unique_words) + word_count)
            
            # If no probability already recorded, add dict to list
            if not term in condProb:
                condProb[term] = dict()
            condProb[term][classification] = probability
    
    model = dict()
    model["priorProb"] = priorProb
    model["condProb"] = condProb
    return model

def main():   
    movies, genres = movie_synopsis.read_file('../data/training_movies.txt')   
   
    models = dict()
    for genre in genres:
        models[genre] = train_model(movies, genre)
        print(genre + " Model Trained")

    encoded_model = json.dumps(models, indent=4, separators=(',', ': '))
    with open('models.json', 'w') as model_file:
        model_file.write(encoded_model)
    
if __name__ =="__main__":
    main()