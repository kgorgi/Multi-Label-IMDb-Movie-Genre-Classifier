""" These are only needed for testing """
from bs4 import BeautifulSoup
import requests


import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

import string
import re

def test_list ():
    testlist = []
    html = requests.get('https://www.imdb.com/title/tt0110912/plotsummary?ref_=tt_stry_pl#synopsis')
    html = BeautifulSoup(html.content, 'html.parser')
    testlist.append(html.find('li', id="synopsis-py3207756"))

    html = requests.get('https://www.imdb.com/title/tt7286456/plotsummary?ref_=tt_stry_pl#synopsis')
    html = BeautifulSoup(html.content, 'html.parser')
    testlist.append(html.find('li', id="synopsis-py4789503"))
    return testlist

def filter_words (synopses_list):
    """ Expects a list of li elements that were found with BeautifulSoup see test_list for example"""
    """ Returns a list of the synopses as strings without the stop words and puncuntuation """
    new_synopses_list = []
    for synopsis in synopses_list:
        fresh_list = []
        all_br = synopsis.find_all('br')
        for br in all_br:
            br.string = ' '
        words = synopsis.get_text().split()
        for word in words:
            word = word.lower()
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word not in stop_words and new_word != '':
                fresh_list.append(new_word)
        new_synopses_list.append(' '.join(fresh_list))
    return new_synopses_list

def main ():
    main()

if __name__ == '__main__':
    test = test_list()
    # print(test)
    print(filter_words(test))