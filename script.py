import argparse
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path
import logging
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger()


def create_parser():
    parser = argparse.ArgumentParser(description='Download books text and info by id')
    parser.add_argument('--start_id', help='Start_id', default=1, type=int)
    parser.add_argument('--end_id', help='End_id', default=10, type=int)

    return parser


def check_for_redirect(response):
    response.raise_for_status()
    if response.status_code == 302:
        raise requests.HTTPError


def download_txt(url, filename, book_id, folder='books/'):
    payload = {"id": f"{book_id}"}
    response = requests.get(url, verify=False, allow_redirects=False, params=payload)
    check_for_redirect(response)

    valid_filename = sanitize_filename(filename)
    filename = os.path.join(folder, valid_filename)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_image(url, filename, folder='images/'):
    response = requests.get(url, verify=False)
    response.raise_for_status()

    valid_filename = sanitize_filename(filename)
    filename = os.path.join(folder, valid_filename)
    with open(filename, 'wb') as file:
        file.write(response.content)

def parse_img_name(file_url):
    path = urlsplit(file_url).path
    encoding_path = unquote(path)
    filename = os.path.split(encoding_path)[-1]
    return filename


def parse_book_page(soup):
    title_tag = soup.find('h1')
    title_text = title_tag.text.split('::')
    book_title, book_author = title_text

    book_genres = soup.find('span', class_='d_book').find_all('a')
    book_comments = soup.find_all('div', class_='texts')

    book_img = soup.find('div', class_='bookimage').find('img')['src']

    return book_title, book_author, book_genres, book_comments, book_img


def get_book(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url, verify=False, allow_redirects=False)
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')
    book_title, book_author, book_genres, book_comments, book_img = parse_book_page(soup)

    logger.info(f'Заголовок: {book_title.strip()}')
    logger.info(f'Автор: {book_author.strip()}')
    logger.info('Жанр:')
    for book_genre in book_genres:
        logger.info(f'{book_genre.text}')
    if len(book_comments) > 1:
        logger.info('Комментарии:')
    for comment in book_comments:
        comment_text = comment.find('span').text
        logger.info(f'{comment_text}')

    book_text_link = 'https://tululu.org/txt.php'
    book_filename = f'{book_id}. {book_title}'
    download_txt(book_text_link, book_filename, book_id)

    img_filename = parse_img_name(book_img)
    book_img_link = urljoin('https://tululu.org/', book_img)
    download_image(book_img_link, img_filename)


def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    Path("images").mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format="%(asctime)s - [%(levelname)s] - %(message)s",
    )
    logger.setLevel(logging.INFO)

    parser = create_parser()
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id):
        try:
            get_book(book_id)
        except requests.HTTPError:
            logger.exception(f'Страница с id {book_id} была переадресована. Информация не получена.')


if __name__ == '__main__':
    main()