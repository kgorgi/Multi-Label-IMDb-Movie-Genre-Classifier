import nltk
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

import string
import re
import os

# Too lazy to use the smart string building with only ten files
data_files = ["pages_1-10.txt", "pages_11-20.txt",
    "pages_21-30.txt", "pages_31-40.txt", "pages_41-50.txt",
    "pages_51-60.txt", "pages_61-70.txt", "pages_71-80.txt",
    "pages_81-90.txt", "pages_91-100.txt"]

# Make a genre files that consists of ones and zeros
# Creates all the genres into their own files
def genre_generator():
    unique_genres = find_unique_genres()
    genres = get_genres()

    
    for current_genre in unique_genres:
        os.remove("../genres/" + current_genre + ".txt")

    # Want to sort all the train data into ints values where it says
    #   which movies are of which genre 1 = True, 0 = False.
    starter = True
    for movie_genres in genres:
        for current_genre in unique_genres:
            if starter:
                with open("../genres/" + current_genre + ".txt", "w") as cg:
                    if current_genre in movie_genres:
                        cg.write("1\n")
                    else:
                        cg.write("0\n")
                starter = False
            else:
                with open("../genres/" + current_genre + ".txt", "a") as cg:
                    if current_genre in movie_genres:
                        cg.write("1\n")
                    else:
                        cg.write("0\n")

def get_genres():
    genres = []
    with open("../data/train_genre.txt", "r") as tg:
        for line in tg:
            genres.append(line)
    return genres

def find_unique_genres():
    unique_genres = []
    with open("../data/train_genre.txt", "r") as tg:
        for line in tg:
            words = line.split(",")
            for word in words:
                word = word.strip('\n')
                if word not in unique_genres:
                    unique_genres.append(word)
    unique_genres.sort()

    return unique_genres


# This is so fucked
# pages_$($)-$$($).txt
def process():
    op = 0
    ids = []
    genres = []
    synopsis = []
    ps = PorterStemmer() 
    for file_name in data_files:
        with open("../data/" + file_name) as open_file_object:
            for line in open_file_object:
                # op = 0 means its a identifier so op = 1
                if op == 0:
                    op = 1
                    ids.append(line)
                # op = 1 means comma seperated movie genre so store in genre array and op = 2
                elif op == 1:
                    op = 2
                    genres.append(line.lower())
                # op = 2 means synopsis so store in . and op = 0
                else:
                    fresh_line = ""
                    op = 0
                    words = line.split()
                    for word in words:
                        word = word.lower()
                        new_word = re.sub(r'[^\w\s]', '', word)
                        if new_word not in stop_words and new_word != '':
                            new_word = ps.stem(new_word)
                            fresh_line = fresh_line + " " + new_word
                    fresh_line = fresh_line + "\n"
                    synopsis.append(fresh_line)
    with open("../data/train_genre.txt", "w") as tg:
        tg.writelines(genres)
    with open("../data/train_synopsis.txt", "w") as ts:
        ts.writelines(synopsis)
    with open("../data/train_ids.txt", "w") as ti:
        ti.writelines(ids)
        
    
def main():
    process()
    # Ran genre_generator()
    # TODO need to feed all the data into the profs text classifier
    print()
            




if __name__ == '__main__':
    main()