import nltk
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

import string
import re
import os

import json


# Too lazy to use the smart string building with only ten files
data_files = ["pages_1-10.txt", "pages_11-20.txt",
    "pages_21-30.txt", "pages_31-40.txt", "pages_41-50.txt",
    "pages_51-60.txt", "pages_61-70.txt", "pages_71-80.txt",
    "pages_81-90.txt", "pages_91-100.txt"]

NUM_TESTS_PER_GENRE = 100

# Make a genre files that consists of ones and zeros
#   to conform to input from code lifted from Thomo
# Creates all the genres into their own files and stores,
#   them into a genres subfolder
def genre_generator(bad_genres):
    unique_genres = find_unique_genres()
    genres = get_genres()
    for current_genre in unique_genres:
        try:
            os.remove("../genres/train_%s.txt" % (current_genre))
        except IOError:
            pass

    # Want to sort all the train data into ints values where it says
    #   which movies are of which genre 1 = True, 0 = False.
    starter = True
    for movie_genres in genres:
        for current_genre in unique_genres:
            if current_genre in bad_genres:
                continue
            if starter:
                with open("../genres/train_%s.txt" % (current_genre), "w") as cg:
                    if current_genre in movie_genres:
                        cg.write("1\n")
                    else:
                        cg.write("0\n")
                starter = False
            else:
                with open("../genres/train_%s.txt" % (current_genre), "a") as cg:
                    if current_genre in movie_genres:
                        cg.write("1\n")
                    else:
                        cg.write("0\n")

# Helper method for genre_generator()
def get_genres():
    genres = []
    with open("../data/train_genre.txt", "r") as tg:
        for line in tg:
            genres.append(line.strip('\n'))
    return genres

# Helper method for genre_generator()
def find_unique_genres():
    unique_genres = []
    with open("../data/genre_cheater.txt", "r") as tg:
        for line in tg:
            words = line.split(",")
            for word in words:
                word = word.strip('\n')
                if word not in unique_genres:
                    unique_genres.append(word)
    unique_genres.sort()
    return unique_genres


"""Method takes all of the 'pages_xxx-xxx.txt'
then converts them into six text files:
      - train_synopsis.txt
      - train_ids.txt
      - train_genre.txt
      - test_synopsis.txt
      - test_ids.txt
      - test_genre.txt
Additionally, for the synopsis it strips any punctuation,
  removes stops words, makes all strings lower, and
  replaces all words with their stem versions."""
def process(bad_genres, genre_counter):
    file_headers = ['ids', 'genre', 'synopsis']

    for file_header in file_headers:
        try:
            os.remove("../data/train_%s.txt" % (file_header))
        except OSError:
            pass
    for file_header in file_headers:
        try:
            os.remove("../data/test_%s.txt" % (file_header))
        except:
            pass

    unique_genres = find_unique_genres()
    genre_filler = dict()
    for genre in unique_genres:
        if genre in genre_counter.keys():
            genre_filler[genre] = 0
    
    op = 0
    train_ids = []
    train_genres = []
    train_synopsis = []
    test_ids = []
    test_genres = []
    test_synopsis = []

    ps = PorterStemmer()
    genres = []
    train_with_movie = True
    usable_movie = False

    for file_name in data_files:
        with open("../data/" + file_name) as open_file_object:
            for line in open_file_object:
                # op = 0 means its a identifier so op = 1
                if op == 0:
                    op = 1
                    tmp_id = line
                # op = 1 means comma seperated movie genre so store in genre array and op = 2
                elif op == 1:
                    op = 2
                    genres = line.lower().split(',')
                    usable_movie = False
                    for genre in genres:
                        genre = genre.strip('\n')
                        if genre in bad_genres:
                            continue
                        elif genre_filler[genre] < min(genre_counter[genre] / 2, NUM_TESTS_PER_GENRE):
                            train_with_movie = False
                            usable_movie = True
                            test_ids.append(tmp_id)
                            test_genres.append(line.lower())
                            break
                        else:
                            train_with_movie = True
                            usable_movie = True
                            train_ids.append(tmp_id)
                            train_genres.append(line.lower())
                            break
                    if train_with_movie == False and usable_movie == True:
                        for genre in genres:
                            genre = genre.strip('\n')

                            if genre in bad_genres:
                                continue
                            genre_filler[genre] += 1
                # op = 2 means synopsis so store in . and op = 0
                else:
                    op = 0
                    if usable_movie:
                        fresh_line = ""
                        words = line.split()
                        for word in words:
                            word = word.lower()
                            new_word = re.sub(r'[^\w\s]', '', word)
                            if new_word not in stop_words and new_word != '':
                                new_word = ps.stem(new_word)
                                fresh_line = fresh_line + " " + new_word
                        fresh_line = fresh_line + "\n"
                        if train_with_movie:
                            train_synopsis.append(fresh_line)
                        else:
                            test_synopsis.append(fresh_line)
                        
    with open("../data/train_genre.txt", "w") as tg:
        tg.writelines(train_genres)
    with open("../data/train_synopsis.txt", "w") as ts:
        ts.writelines(train_synopsis)
    with open("../data/train_ids.txt", "w") as ti:
        ti.writelines(train_ids)
    with open("../data/test_genre.txt", "w") as tg:
        tg.writelines(test_genres)
    with open("../data/test_synopsis.txt", "w") as ts:
        ts.writelines(test_synopsis)
    with open("../data/test_ids.txt", "w") as ti:
        ti.writelines(test_ids)

def find_bad_genres():
    unique_genres = find_unique_genres()
    genre_counter = dict()
    # Create a dictionary to count all of genres
    for genre in unique_genres:
        genre_counter[genre] = 0

    bad_genres = []
    op = 0
    for file_name in data_files:
        with open("../data/" + file_name) as open_file_object:
            for line in open_file_object:
                # op = 0 means its a identifier so op = 1
                if op == 0:
                    op = 1
                # op = 1 means comma seperated movie genre so store in genre array and op = 2
                elif op == 1:
                    op = 2
                    genres = line.lower().split(',')
                    for genre in genres:

                        genre_counter[genre.strip('\n')] += 1
                # op = 2 means synopsis so store in . and op = 0
                else:
                    op = 0
    for genre in unique_genres:
        if genre_counter[genre] < 100:
            bad_genres.append(genre)
            del genre_counter[genre]
    print(json.dumps(genre_counter, indent=1))
    print(json.dumps(bad_genres, indent=1))
    return bad_genres, genre_counter        

def main():

    bad_genres, genre_counter = find_bad_genres()
    # process(bad_genres, genre_counter)
    # genre_generator(bad_genres)
    # Should only need to run the above two once
    print()
            
if __name__ == '__main__':
    main()