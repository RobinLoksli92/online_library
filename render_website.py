from email.encoders import encode_noop
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape

from livereload import Server, shell


def on_reload():
    env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
   
    for i, books_group in enumerate(books_per_page, 1):
        grouped_books = list(chunked(books_group,2))
        rendered_page = template.render(books=grouped_books)
        with open(f'pages/index{i}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)
    print('site reloaded')


books = []

with open('book_discription.json', 'r', encoding='utf-8') as file:
    for book in json.load(file):
        books.append(book)

books_per_page = list(chunked(books,20))

for i, book in enumerate(books_per_page, 1):
    grouped_books = list(chunked(books_per_page[0],2))
    print(grouped_books)

on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
