import math
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import numpy as np
import operator
import os
import re
stop_words = set(stopwords.words('english'))

data_files = ["pages_1-10.txt", "pages_11-20.txt",
    "pages_21-30.txt", "pages_31-40.txt", "pages_41-50.txt",
    "pages_51-60.txt", "pages_61-70.txt", "pages_71-80.txt",
    "pages_81-90.txt", "pages_91-100.txt"]

def count_genres(full_text):
    genre_count = dict()
    genres_per_movie = full_text[1::3]
    for genre_list in genres_per_movie:
        for genre in genre_list.strip().split(','):
            if genre in genre_count:
                genre_count[genre] += 1
            else:
                genre_count[genre] = 1
    
    return genre_count    

def get_genres(filename):
    with open(filename)as fh:
        return fh.readlines()

def get_pages_text():
    full_text = list()
    for data in data_files:
        file_loc = "pages/" + data
        with open(file_loc) as fh:
            full_text.extend(fh.readlines())
    return full_text

def plot_genre_count(genre_data, x_increment):
    labels = genre_data.keys()
    sizes = genre_data.values()
    percentages = list()
    sum = 0

    for size in sizes:
        sum+=size

    for size in sizes:
        percentages.append((size/sum)*100)

    figure, axis = plt.subplots()
    y_pos = np.arange(len(labels))

    for i, v in enumerate(sizes):
        axis.text(v + 3, i + .25, str(v), color='black', fontweight='bold')
    axis.barh(np.arange(len(labels)), sizes, align='center')
    plt.xticks(np.arange(0, max(sizes)+x_increment, x_increment))
    axis.set_yticks(np.arange(len(labels)))
    axis.set_yticklabels(labels)

    axis.invert_yaxis() 
    axis.set_xlabel('Number of Movies')
    axis.set_ylabel('Genre')
    axis.set_title('Number of Movies per Genre')
    plt.show()

def count_words(full_text):
    word_count = dict()
    words_in_synopsis = full_text[1::2]
    
    for word_chunk in words_in_synopsis:
        for word in word_chunk.strip().split(" "):
            new_word = re.sub(r'[^\w\s]', '', word.lower())
            if new_word in stop_words:
                continue
            if new_word in word_count:
                word_count[new_word] += 1
            else:
                word_count[new_word] = 1
    word_count_sorted = sorted(word_count.items(), key=operator.itemgetter(1))
    return word_count_sorted

def get_average_synopsis_length(full_text):
    synopsis_count = 0
    synopsis_total_count = 0
    words_in_synopsis = full_text[1::2]

    for word_chunk in words_in_synopsis:
        synopsis_total_count += len(word_chunk.split(" "))
        synopsis_count +=1
    return synopsis_total_count / synopsis_count

def main():
    genre_data_test = count_genres(get_genres('test_movies.txt'))
    plot_genre_count(genre_data_test, 10)
    genre_data_train = count_genres(get_genres('train_movies.txt'))
    plot_genre_count(genre_data_train, 200)
    genre_data_pages = count_genres(get_pages_text())
    plot_genre_count(genre_data_pages, 200)
    word_count_sorted = count_words(get_pages_text())
    get_average_synopsis_length(get_pages_text())

if __name__ == '__main__':
    main()