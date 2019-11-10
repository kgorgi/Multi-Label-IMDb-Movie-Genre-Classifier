import requests 
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
}

def get_page(page_number):
    """Returns the HTML of a specific list page"""
    url = "https://www.imdb.com/list/ls000004717/?sort=list_order,asc&st_dt=&mode=detail&page=" + str(page_number)
    r = requests.get(url, headers=headers)
    return r.text

def process_page(html):
    """Processes HTML and returns an array of imdb movie ids"""
    soup = BeautifulSoup(html, features="html.parser")
    headers = soup.findAll("h3", {"class": "lister-item-header"})

    movie_ids = []
    for header in headers:
        movie_url = header.a['href']
        movie_id = movie_url.split('/')[2]
        movie_ids.append(movie_id)

    return movie_ids

def crawl_imdb():
    """Returns an array of imdb movie ids"""
    movie_ids = []

    for i in range(1, 11):
        print("Processing page: " + str(i))
        html = get_page(i)
        movie_ids.extend(process_page(html))
    
    return movie_ids

def main():
    movie_ids = crawl_imdb()
    print(movie_ids)

if __name__ == '__main__':
    main()
