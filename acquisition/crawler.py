from bs4 import BeautifulSoup
from utilities import safe_get

list_id = "ls057823854"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
}

def get_page(page_number):
    """Returns the HTML of a specific list page or None if response failed"""
    url = "https://www.imdb.com/list/" + list_id + "/?sort=list_order,asc&st_dt=&mode=detail&page=" + str(page_number)
    
    response = safe_get(url)

    if response is None:
        return None
    else:
        return response.text

def process_page(html):
    """Processes HTML and returns an array of array [movie_id, array of genres]"""
    soup = BeautifulSoup(html, features="html.parser")
    html_list = soup.findAll("div", {"class": "lister-item-content"})

    movies_list = []
    for html in html_list:

        try:
            movie_url = html.h3.a['href']
            movie_id = movie_url.split('/')[2]
            genre_html = html.p.find("span", {"class": "genre"})
            genre_text = genre_html.getText()
            genre_array = [text.strip() for text in genre_text.split(", ")] 
            movies_list.append([movie_id, genre_array])
        except:
            # Invalid Movie...Skip
            pass 

    return movies_list

def crawl_imdb(max_page):
    """Returns an array of arrays [movie_id, array of genres]"""
    movies = []

    for i in range(1, max_page):
        print("Processing page: " + str(i))
        html = get_page(i)
        if html is not None:
            movies.extend(process_page(html))
    
    return movies

def main():
    movies = crawl_imdb(2)

    for movie in movies:
        print(movie)

if __name__ == '__main__':
    main()
