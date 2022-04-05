import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

from livereload import Server, shell



def on_reload():
    template = env.get_template('template.html')
    rendered_page = template.render(books=books)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print('site reloaded')

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
    )

books = []

with open('book_discription.json', 'r', encoding='utf-8') as file:
    for book in json.load(file):
        books.append(book)

on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
