import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path
import logging
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)

Path("books").mkdir(parents=True, exist_ok=True)


def check_for_redirect(response):
    if response.status_code == 302:
        raise requests.HTTPError


def download_txt(url, filename, folder='books/'):
    response = requests.get(url, verify=False, allow_redirects=False)
    check_for_redirect(response)

    valid_filename = sanitize_filename(filename)
    filename = os.path.join(folder, valid_filename)
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_book(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url, verify=False, allow_redirects=False)
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text.split('::')
    [book_title, book_author] = title_text

    book_text_link = f'https://tululu.org/txt.php?id={book_id}'
    book_filename = f'{book_id}. {book_title}'

    download_txt(book_text_link, book_filename)


def main():
    for book_id in range(1, 11):
        try:
            get_book(book_id)
        except requests.HTTPError:
            logging.error(f'The page with id {book_id} was redirected')


if __name__ == '__main__':
    main()