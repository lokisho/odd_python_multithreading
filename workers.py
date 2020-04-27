import logging
import os

from redis import Redis

from rq import Queue

from download import setup_download_dir, get_links, download_link


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


def main():
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir()
    links = get_links(client_id)
    q = Queue(connection=Redis(host='localhost', port=6379))
    for link in links:
        # puts the job in a redis server that can be in other machine
        # rqworker in a terminal window and it will start a worker listening on the default queue.
        # rqworker queue_name will listen to that named queue.
        q.enqueue(download_link, download_dir, link)

if __name__ == '__main__':
    main()

