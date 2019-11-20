from scraper import add_movie_synopsis
from crawler import get_page, process_page
import threading
import time
import queue

def crawler_thread(page_queue, movie_id_queue):
    while not page_queue.empty():
        page_number = page_queue.get()
        
        page_queue.task_done()
        html = get_page(page_number)
        if html is None:
            print("Failed to request page: " + str(page_number))
            continue
       
        movies = process_page(html)
        for movie in movies:
            movie_id_queue.put(movie)

def scraping_thread(movie_id_queue, result_list, finished_crawling):
    while not (finished_crawling.is_set() and movie_id_queue.empty()):
        while not movie_id_queue.empty():
            movie = movie_id_queue.get()
            successful = add_movie_synopsis(movie)

            if successful:
                result_list.append(movie)

            movie_id_queue.task_done()
    
        time.sleep(0.010)

def acquire_data(start_page_num, end_page_num):
    number_of_crawler_threads = 5
    number_of_scraping_threads = 50

    page_queue = queue.Queue()
    movie_id_queue = queue.Queue()
    result_list = list()
    finished_crawling = threading.Event()

    for i in range(start_page_num, end_page_num + 1):
        page_queue.put(i)

    crawler_threads = list()
    crawler_thread_args = (page_queue, movie_id_queue)
    scraping_threads = list()
    scraping_thread_args = (movie_id_queue, result_list, finished_crawling)

    for i in range(0, number_of_crawler_threads):
        thread = threading.Thread(target = crawler_thread, args = crawler_thread_args)
        thread.setDaemon(True)
        thread.start()
        crawler_threads.append(thread)

    for i in range(0, number_of_scraping_threads):
        thread = threading.Thread(target = scraping_thread, args = scraping_thread_args)
        thread.setDaemon(True)
        thread.start()
        scraping_threads.append(thread)

    for thread in crawler_threads:
        while thread.isAlive():
            print("Remaining Pages To Crawl:" + str(page_queue.qsize()) + "\t" + \
                  "Movie Ids In Queue: " + str(movie_id_queue.qsize()) + "\t" + \
                  "Scraped Movies: " + str(len(result_list)))
            time.sleep(0.5)
    
    finished_crawling.set()

    for thread in scraping_threads:
       while thread.isAlive():
            print("Remaining Pages To Crawl:" + str(page_queue.qsize()) + "\t" + \
                  "Movie Ids In Queue: " + str(movie_id_queue.qsize()) + "\t" + \
                  "Scraped Movies: " + str(len(result_list)))
            time.sleep(0.5)

    with open('pages_' + str(start_page_num) + '-' + str(end_page_num) + '.txt', 'w') as fh:
        for movie in result_list:
            if len(movie) < 3:
                print('WEIRD: ' + ' '.join(movie) + ' Length: ' + str(len(movie)))
            fh.writelines([movie[0] + '\n', ','.join(movie[1]) + '\n', movie[2] + '\n'])

def main():
    for i in range(8, 10):
        start = 1 + 10 * i
        end = 10 + 10 * i
        print('Processing Pages ' + str(start) + ' to ' + str(end))

        acquire_data(start, end)
        time.sleep(10)

if __name__ == '__main__':
    main()
