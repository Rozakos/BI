import psycopg2
import json
import requests
from psycopg2.extras import Json



def etl():
    connection = psycopg2.connect("postgres://postgres:banana_2@localhost:5432/postgres")
    connection.autocommit = True
    crs = connection.cursor()

    insert_q = """    INSERT INTO raw (unique_aer_id_number, raw_data) VALUES(%s, %s)
    """
    for page in fetch_data():
        for result in page:
            crs.execute(insert_q, (result.get("unique_aer_id_number"), json.dumps(result)))


def fetch_data():
    url = 'https://api.fda.gov/animalandveterinary/event.json?limit=1000'
    response = requests.get(url)
    print(url)
    yield response.json().get("results")

    while response.links.get("next") is not None:
        url = response.links.get('next').get("url")
        response = requests.get(url)
        yield response.json().get("results")



def etl_dog_api():
    connection = psycopg2.connect("postgres://postgres:banana_2@localhost:5432/postgres")
    connection.autocommit = True
    crs = connection.cursor()

    insert_q = """
     INSERT INTO raw_dog (raw_data)
       SELECT j FROM jsonb_array_elements((%s)::jsonb) AS j;
    """

    crs.execute(insert_q, fetch_data_dog_api())


def fetch_data_dog_api():
    url = 'https://api.thedogapi.com/v1/breeds/'
    response = requests.get(url)
    response = response.text
    print(response)

    return [response]


if __name__ == '__main__':
        etl_dog_api()

    # def fetch_data():
    #     url = 'https://api.fda.gov/animalandveterinary/event.json?limit=1000'
    #     response = requests.get(url)
    #     print(url)
    #     yield response.json().get("results")
    #
    #     while response.links.get("next") is not None:
    #         url = response.links.get('next').get("url")
    #         response = requests.get(url)
    #         yield response.json().get("results")
