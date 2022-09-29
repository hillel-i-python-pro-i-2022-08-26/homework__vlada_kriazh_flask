from flask import Flask
from applications.applications import reading_file, generate_list_users
from applications.applications import get_numbers_of_astronauts, mean_data_metrical
from pathlib import Path


app = Flask(__name__)
path_to_txt_file = Path('applications/Example.txt')


@app.route('/')
def index():
    return '<h1>Homework Flask<h1>'


@app.route('/requirements/')
def print_file():
    return ''.join(f'<p>{i}<p>' for i in reading_file(path_to_txt_file))


@app.route('/generate-users/')
@app.route('/generate-users/<int:count>')
def users(count=100):
    users_count = count
    return ''.join(f'<p>{i}<p>' for i in generate_list_users(users_count))


@app.route('/space/')
def output_count_of_astronauts():
    return f'<p>number of astronauts - {get_numbers_of_astronauts()}<p>'


@app.route('/mean/')
def mean():
    data = mean_data_metrical()
    return f'<p>Mean height (sm) = {round(data[0], 2)}<p><p>Mean weight (kg) = {round(data[1], 2)}'


if __name__ == "__main__":
    app.run()
