import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

Path("books").mkdir(parents=True, exist_ok=True)


def get_book_text(book_id):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url, verify=False)
    response.raise_for_status()
    filename = f'books/book_{book_id}.txt'
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    for book_id in range(10):
        get_book_text(book_id)


if __name__ == '__main__':
    main()