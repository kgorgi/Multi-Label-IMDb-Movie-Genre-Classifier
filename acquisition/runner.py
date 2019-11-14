import threading
from . import crawler

def threaded_crawler(page_queue, result_queue):
    while not page_queue.empty():
        page_number = page_queue.get()
        page_queue.task_done()
        html = crawler.get_page(page_number)
        movies = crawler.process_page(html)

        for movie in movies:
            result_queue.add(movie)


def main():
    pass

if __name__ == '__main__':
    main()
