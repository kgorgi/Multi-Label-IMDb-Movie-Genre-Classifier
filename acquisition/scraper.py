from bs4 import BeautifulSoup
import re
from html.parser import HTMLParser
from utilities import safe_get

def remove_spaces(synopsis):
    all_br = synopsis.find_all('br')
    for br in all_br:
        br.string = ' '

    text = synopsis.get_text()
    return " ".join(text.split())

def get_movie_synopsis(movie_id):
    movie_page_html = BeautifulSoup(safe_get('https://www.imdb.com/title/' + movie_id + '/plotsummary').content, 'html.parser')
    if movie_page_html.select('#no-synopsis-content'):
        return None
    else:
        synopsis_html = movie_page_html.findAll('li', id=lambda x: x and x.startswith('synopsis-'))[0]
        return remove_spaces(synopsis_html)

def add_movie_synopsis(movie_info):
    synopsis = get_movie_synopsis(movie_info[0])
    if not synopsis is None:
        movie_info.append(synopsis.strip())
        return True
    return False