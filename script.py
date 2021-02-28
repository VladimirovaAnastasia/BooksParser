import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path
import logging

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)

Path("books").mkdir(parents=True, exist_ok=True)


def check_for_redirect(response):
    if response.status_code == 302:
        raise requests.HTTPError


def get_book_text(book_id):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url, verify=False, allow_redirects=False)
    check_for_redirect(response)
    filename = f'books/book_{book_id}.txt'
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    for book_id in range(10):
        try:
            get_book_text(book_id+1)
        except requests.HTTPError:
            logging.error(f'The page with id {book_id+1} was redirected')


if __name__ == '__main__':
    main()