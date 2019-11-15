import threading
import queue
from crawler import get_page, process_page

def crawler_thread(page_queue, result_queue):
    while not page_queue.empty():
        page_number = page_queue.get()
        print("Processing Page: " + str(page_number))
        page_queue.task_done()
        html = get_page(page_number)
        if html is None:
            print("Failed to request page: " + str(page_number))
            continue
       
        movies = process_page(html)
        for movie in movies:
            result_queue.put(movie)

def main():
    number_of_crawler_threads = 15

    page_queue = queue.Queue()
    result_queue = queue.Queue()

    for i in range(1, 100):
        page_queue.put(i)

    crawler_threads = list()
    crawler_thread_args = (page_queue, result_queue)
    for i in range(0, number_of_crawler_threads):
        thread = threading.Thread(target = crawler_thread, args = crawler_thread_args)
        thread.setDaemon(True)
        thread.start()
        crawler_threads.append(thread)

    for thread in crawler_threads:
        thread.join()
    
if __name__ == '__main__':
    main()
