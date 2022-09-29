from statistics import mean
from faker import Faker
import requests
import pathlib

fake = Faker()

API_ASTROS = 'http://api.open-notify.org/astros.json'
LINK_DOWNLOAD_CSV = requests.get('https://drive.google.com/uc?export=download&id=1yM0a4CSf0iuAGOGEljdb7qcWyz82RBxl')

# Reading csv file


def reading_file(path_to_file: pathlib.Path) -> list:
    with open(path_to_file, 'r') as file:
        return list(file)


# Generating users


def generate_user() -> str:
    return fake.name()


def generate_list_users(count: int) -> list:
    list_users = []
    num = 1
    for i in range(count):
        name = generate_user()
        users_name = name.split()
        list_users.append(f"{num}. {users_name[0]} {users_name[0].lower()}_{users_name[1].lower()}.mail.com")
        num += 1
    return list_users


# Getting data from json


def get_json(link: str) -> dict:
    page = requests.get(link)
    return page.json()


def get_numbers_of_astronauts() -> int:
    data = get_json(API_ASTROS)
    return data['number']


# Processing data from scv file


def download_csv(page: requests.models.Response):
    with open('data.csv', 'wb') as file:
        file.write(page.content)


def mean_data(csv_file: str) -> list:
    height = []
    weight = []
    with open(csv_file, 'r') as file:
        for line in list(file)[1:-1]:
            row = line.split(',')
            height.append(float(row[1].strip()))
            weight.append(float(row[2].strip()))
    return [mean(height), mean(weight)]


def inches_to_sm(height: float) -> float:
    sm = height * 2.54
    return sm


def pounds_to_kg(weight: float) -> float:
    kg = weight * 0.45
    return kg


def mean_data_metrical() -> list:
    download_csv(LINK_DOWNLOAD_CSV)
    mean_data_list = mean_data('data.csv')
    mean_sm = inches_to_sm(mean_data_list[0])
    mean_kg = pounds_to_kg(mean_data_list[1])
    return [mean_sm, mean_kg]
