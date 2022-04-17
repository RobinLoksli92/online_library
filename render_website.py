import json
import math
import os
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


BOOKS_PER_PAGE = 20

COL_NUMBER = 2


def get_img_name(books):
    for book in books:
        img_path = urlparse(book['Картинка']).path
        img_name = os.path.basename(img_path)
        book['img_name'] = img_name


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    with open('media/book_discription.json', 'r', encoding='utf-8') as file:
        books = json.load(file)

    books_per_page = list(chunked(books, BOOKS_PER_PAGE))
    get_img_name(books)
    page_count = math.ceil(len(books)/BOOKS_PER_PAGE)

    for current_page, books_group in enumerate(books_per_page, 1):
        grouped_books = list(chunked(books_group, COL_NUMBER))
        rendered_page = template.render(
            books=grouped_books,
            current_page=current_page,
            page_count=page_count)
        with open(
                f'pages/index{current_page}.html',
                'w',
                encoding="utf8"
                ) as file:
            file.write(rendered_page)

    print('site reloaded')


def main():
    server = Server()
    on_reload()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
