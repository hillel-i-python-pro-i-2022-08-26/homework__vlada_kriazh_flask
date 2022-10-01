import sqlite3
from flask import Flask, Response
from pathlib import Path
from webargs import fields
from webargs.flaskparser import use_args

from applications.application import reading_file, generate_list_users
from applications.application import get_numbers_of_astronauts, mean_data_metrical
from applications.create_table import create_table
from applications import connection_db
from applications.settings_path import DB_PATH

app = Flask(__name__)
path_to_txt_file = Path('applications/Example.txt')


# hw Flask


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


# hw SQL

create_table()


@app.route('/phones/create_row')
@use_args({'contact_name': fields.Str(required=True), 'phone_value': fields.Str(required=True)}, location='query')
def create_row(args):
    if args['phone_value'].isdigit():
        try:
            with connection_db.DBConnection(DB_PATH) as conn:
                with conn:
                    conn.execute('''
                            INSERT INTO phones (contact_name, phone_value)
                            VALUES (:contact_name, :phone_value);''',
                                 {'contact_name': args['contact_name'], 'phone_value': args['phone_value']})
            return 'Row added'
        except sqlite3.IntegrityError:
            return f"<p>Incorrect phone number.<p> <p>Phone number length 10 symbols, get {len(args['phone_value'])}<p>"
    else:
        return f'<p>Incorrect phone number.<p> <p>Enter numbers.<p>'


@app.route('/phones/read/<int:key>')
def read_row(key: int):
    key = key
    try:
        with connection_db.DBConnection(DB_PATH) as conn:
            result = conn.execute('''
                    SELECT *
                    FROM phones
                    WHERE phone_ID = :key''', {'key': key}).fetchone()
        return f'{result[0]} {result[1]} {result[2]}'
    except TypeError:
        return 'Incorrect key'


@app.route('/phones/update/<int:key>')
@use_args({'contact_name': fields.Str(), 'phone_value': fields.Str()}, location='query')
def updating_row(args, key: int):
    key = key
    name = args.get('contact_name')
    phone = args.get('phone_value')
    if name is None and phone is None:
        return Response(
                    'Need to provide at least one argument',
                    status=400,
                )

    if phone is not None:
        if not phone.isdigit():
            return Response(
                    "<p>Incorrect phone number.<p> <p>Enter numbers.<p>",
                    status=400,
                )
    column = []
    if name:
        column.append('contact_name = :name')
    if phone:
        column.append('phone_value = :phone')

    try:
        with connection_db.DBConnection(DB_PATH) as conn:
            with conn:
                conn.execute(f'''
                UPDATE phones
                SET {', '.join(column)}
                WHERE phone_ID = :key''', {'key': key, 'name': name, 'phone': phone})

                result = conn.execute('''
                            SELECT *
                            FROM phones
                            WHERE phone_ID = :key''', {'key': key}).fetchone()
        return f'{result[0]} {result[1]} {result[2]}'
    except sqlite3.IntegrityError:
        return f"<p>Incorrect phone number.<p> <p>Phone number length 10 symbols, get {len(args['phone_value'])}<p>"


@app.route('/phones/delete/<int:key>')
def delete_row(key: int):
    key = key
    with connection_db.DBConnection(DB_PATH) as conn:
        with conn:
            conn.execute('''
            DELETE FROM phones
            WHERE phone_ID = :key''', {'key': key})
    return f'Row №{key} deleted'


@app.route('/phones/read_all')
def read_all():
    with connection_db.DBConnection(DB_PATH) as conn:
        result = conn.execute('''
        SELECT * FROM phones
        ''').fetchall()
    return ''.join([f'<p>{i[0]} {i[1]} {i[2]}<p>' for i in result])


if __name__ == "__main__":
    app.run(debug=True)
