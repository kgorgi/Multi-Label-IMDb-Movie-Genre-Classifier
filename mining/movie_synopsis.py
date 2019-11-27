# Constants
is_genre_class = "T"
is_not_genre_class = "F"
classifications = [is_not_genre_class, is_genre_class]

class MovieSynopsis:
    def __init__(self, movie_id, genres, text):
        self.id = movie_id
        self.text_arr = text.split(" ")
        self.genres = set()

        for genre in genres:
            self.genres.add(genre)

    def has_genre(self, genre):
        return genre in self.genres


def read_file(filename):
    movies = []
    all_genres = set()
    with open(filename) as file:
        lines = file.read().splitlines()
        for i in range(0, int(len(lines) / 3)):
            movie_index = i * 3
            movie_id = lines[movie_index]
            genres = lines[movie_index + 1].split(',')
            for genre in genres:
                all_genres.add(genre)
            text = lines[movie_index + 2]
            movie = MovieSynopsis(movie_id, genres, text)
            movies.append(movie)
    return movies, all_genres