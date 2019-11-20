from bs4 import BeautifulSoup
import re
import requests
from html.parser import HTMLParser

def retrieve_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as err:
        print('None 200 status code: %s', err)
    except Exception as amb_err:
        print('Ambigious error: %s', amb_err)
    else:
        return BeautifulSoup(response.content, 'html.parser')

def remove_spaces(synopsis):
    all_br = synopsis.find_all('br')
    for br in all_br:
        br.string = ' '

    text = synopsis.get_text()
    return " ".join(text.split())

def get_movie_synopsis(movie_id):
    movie_page_html = retrieve_html('https://www.imdb.com/title/' + movie_id + '/plotsummary')
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