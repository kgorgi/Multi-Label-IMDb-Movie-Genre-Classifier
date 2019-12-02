import re
import nltk
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

NUM_TESTS_PER_GENRE = 100
GENRE_THRESHOLD = 100

def preprocess_data(lines, bad_genres, genre_counter):
    unique_genres = list(genre_counter.keys())
    genre_filler = dict()
    for genre in unique_genres:
        if genre in genre_counter.keys():
            genre_filler[genre] = 0
    
    op = 0
    train_ids = list()
    train_genres = list()
    train_synopsis = list()
    test_ids = list()
    test_genres = list()
    test_synopsis = list()

    ps = PorterStemmer()
    genres = list()
    train_with_movie = True
    usable_movie = False

    for line in lines:
        # op = 0 means its a identifier so op = 1
        if op == 0:
            op = 1
            tmp_id = line
        # op = 1 means comma seperated movie genre so store in genre array and op = 2
        elif op == 1:
            op = 2
            genres = line.lower().split(',')
            good_genres_list = list()
            for genre in genres:
                if genre not in bad_genres:
                    good_genres_list.append(genre)
            good_genres = ",".join(good_genres_list)
            usable_movie = False
            
            for genre in genres:
                genre = genre.strip('\n')
                if genre in bad_genres:
                    continue
                elif genre_filler[genre] < min(genre_counter[genre] / 2, NUM_TESTS_PER_GENRE):
                    train_with_movie = False
                    usable_movie = True
                    test_ids.append(tmp_id)
                    test_genres.append(good_genres)
                    break
                else:
                    train_with_movie = True
                    usable_movie = True
                    train_ids.append(tmp_id)
                    train_genres.append(good_genres)
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
                fresh_line = fresh_line.lstrip()        
                if train_with_movie:
                    train_synopsis.append(fresh_line)
                else:
                    test_synopsis.append(fresh_line)
                    
    return (train_ids, train_genres, train_synopsis), (test_ids,test_genres,test_synopsis)           

def find_bad_genres(lines):
    genre_counter = dict()
    bad_genres = set()
    op = 0
    for line in lines:
        # op = 0 means its a identifier so op = 1
        if op == 0:
            op = 1
        # op = 1 means comma seperated movie genre so store in genre array and op = 2
        elif op == 1:
            op = 2
            genres = line.lower().split(',')
            for genre_raw in genres:
                genre = genre_raw.strip('\n')
                if genre not in genre_counter:
                    genre_counter[genre] = 0
                genre_counter[genre] += 1
        # op = 2 means synopsis so store in . and op = 0
        else:
            op = 0

    for genre in list(genre_counter.keys()):
        if genre_counter[genre] < GENRE_THRESHOLD:
            bad_genres.add(genre)
            del genre_counter[genre]
   
    return bad_genres, genre_counter  

                   
def combine_files(start, end):
    lines = list()
    for i in range(start, end):
        start_page_num = 1 + 10 * i
        end_page_num = 10 + 10 * i
        with open('../data/raw/pages_' + str(start_page_num) \
                    + '-' + str(end_page_num) + '.txt', 'r') as fh:
            lines.extend(fh.read().splitlines())

    return lines     

def write_movies_to_file(movie_tuples, filename):
    with open(filename, "w") as output_file:
        for i in range(0, len(movie_tuples[0])):
            for j in range(0, len(movie_tuples)):
                output_file.write(movie_tuples[j][i] + "\n")
            
def main():
    lines = combine_files(0, 10)

    print("Total number of movie synopses:", int(len(lines)/3))

    bad_genres, genre_counter = find_bad_genres(lines)
    train_movies_list, test_movies_list = preprocess_data(lines, bad_genres, genre_counter)

    write_movies_to_file(train_movies_list, '../data/train_movies.txt')
    write_movies_to_file(test_movies_list, '../data/test_movies.txt')
            
if __name__ == '__main__':
    main()