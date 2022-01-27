import psycopg2
import requests
import psycopg2
import json
from init import *



active_ingredients_table = ("""
CREATE TABLE active_ingredients
(
  id SERIAL
    CONSTRAINT active_ingredients_pk
      PRIMARY KEY, active_ingredient TEXT
);
""")

age_table = ("""
create table age
(
unique_aer_id_number varchar(100),
min numeric(10,2),
unit varchar(100)
);
""")

animals_table = ("""
create table animals
(
unique_aer_id_number varchar(100),
species varchar(100),
gender varchar(100),
breed varchar(2000),
reproductive_status varchar(100)
);
""")

dog_table = ("""
create table dog
(
id int,
name varchar(100),
life_span int,
weight varchar(100),
height varchar(100),
temperament varchar(500),
breed_group varchar(100),
bred_for varchar(500)
);
""")

drugs_table = ("""
create table drugs
(
unique_aer_id_number varchar(100),
used_according_to_label varchar(100),
previous_exposure_to_drug varchar(100),
dosage_form varchar(100),
atc_vet_code varchar(100)
);
""")

duration_table = ("""
create table duration
(
unique_aer_id_number varchar(100),
value int,
unit varchar(100)
);

""")

health_assessment_prior_to_exposure_table = ("""
create table health_assessment_prior_to_exposure
(
unique_aer_id_number varchar(100),
condition_of_animal varchar(100)
);

""")

incident_ai_table = ("""
create table incident_ai
(
unique_aer_id_number varchar(100),
ai_id int,
numerator numeric(10,2),
numerator_unit varchar(100),
denominator numeric(10,2),
denominator_unit varchar(100)
);

""")

reactions_table = ("""
create table reactions
(
unique_aer_id_number varchar(100),
veddra_version varchar(100),
veddra_term_code int,
veddra_term_name varchar(100)
);
""")

results_table = ("""
create table results
(
unique_aer_id_number varchar(100),
original_receive_date varchar(100),
primary_reporter varchar(100),
onset_date varchar(100),
report_id varchar(100)
);

""")

weight_table = ("""
create table weight
(
unique_aer_id_number varchar(100),
min numeric(10,2),
unit varchar(100)
);

""")

temperament_table = ("""
create table temperament
(
id int,
char1 varchar(100),
char2 varchar(100),
char3 varchar(100),
char4 varchar(100),
char5 varchar(100),
char6 varchar(100)
);
""")

table_list = [active_ingredients_table, age_table, animals_table, dog_table,drugs_table, duration_table,
              health_assessment_prior_to_exposure_table,incident_ai_table, reactions_table,
              results_table, weight_table, temperament_table]


def table_creation():
    try:
        connection = psycopg2.connect(connection_name)
        connection.autocommit = True
        crs = connection.cursor()

        for command in table_list:
            crs.execute(command)
            # close communication with the PostgreSQL database server
            # crs.close()
            # commit the changes
            connection.commit()
        crs.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def active_ingredients():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    # Active Ingredients
    active_ingredients_to_insert = []
    for record in records:
        for drugs_data in record[1].get('drug'):
            for active_ingredients in drugs_data.get('active_ingredients'):
                active_ingredients_to_insert.append(active_ingredients.get('name', 'Unknown'))

    insert_q = """
        INSERT INTO active_ingredients (active_ingredient)
        VALUES (%s)
        ON CONFLICT DO NOTHING
        """

    for active_ingredient_to_insert in active_ingredients_to_insert:
        crs.execute(insert_q, (active_ingredient_to_insert,))


def incident_ai():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    for record in records:
        try:
            for drugs_data in record[1].get('drug'):
                for active_ingredient in drugs_data.get('active_ingredients'):

                    crs.execute(f"""
                    SELECT id FROM active_ingredients
                    WHERE active_ingredient = '{active_ingredient.get('name', 'Unknown')}'
                    """)

                    ai_to_insert = crs.fetchone()

                    crs.execute("""
                    INSERT INTO incident_ai (unique_aer_id_number,ai_id,numerator,numerator_unit,denominator,denominator_unit)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    ON CONFLICT DO NOTHING 
                    """, (record[0], ai_to_insert[0], active_ingredient.get('dose').get('numerator'),
                          active_ingredient.get('dose').get('numerator'), active_ingredient.get('dose').get('denominator'),
                          active_ingredient.get('dose').get('denominator_unit')))
        except Exception as E:
            print("Error: {}".format(E))




def animals():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    for record in records:
        try:

            # for animal_data in record[1].get('animal'):
                animal_data = record[1].get("animal")
                print(animal_data['breed']['breed_component'])
                print(animal_data['species'])
                crs.execute(f"""
                INSERT INTO animals(unique_aer_id_number, species, gender, breed, reproductive_status)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """, (record[0], animal_data.get('species'), animal_data.get('gender'), animal_data['breed']['breed_component'],
                      animal_data.get('reproductive_status')))

        except Exception as E:
            print("Error: {}".format(E))


def age():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    for record in records:
        try:
            animal_data = record[1].get("animal")
            age = animal_data["age"]
            print(age)
            min = age.get("min")
            print(min)
            crs.execute(f"""
            INSERT INTO age(unique_aer_id_number, min, unit)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (record[0], age.get("min"), age.get("unit")))
        except Exception as E:
            print("Error: {}".format(E))


def results():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    for record in records:
        try:
            results = record[1]
            original_receive_date = results.get("original_receive_date")
            primary_reporter = results.get("primary_reporter")
            onset_date = results.get("onset_date")
            report_id = results.get("report_id")
            crs.execute(f"""
            INSERT INTO results(unique_aer_id_number, original_receive_date, primary_reporter, onset_date, report_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (record[0], original_receive_date, primary_reporter, onset_date, report_id))
            # print(report_id)
            # print(onset_date)
            # print(number_of_animals_affected)
            # print(number_of_animals_treated)
            # print(onset_date)
            # print(primary_reporter)
            # print(report_id)
        except Exception as E:
            print("Error: {}".format(E))


def dog():

    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw_dog LIMIT 1000")

    records = crs.fetchall()
    for record in records:
        try:
            id  = record[0].get("id")
            name = record[0].get("name")
            life_span = record[0].get("life_span")[:2]
            weight = record[0].get("weight")["metric"][:2]
            height = record[0].get("height")["metric"][:2]
            temperament = record[0].get("temperament")
            breed_group = record[0].get("breed_group")
            bred_for = record[0].get("bred_for")
            # print(id)
            # print(weight)
            # print(height)
            print(temperament)
            crs.execute("""
            INSERT INTO dog(id, name, life_span, weight, height, temperament, breed_group, bred_for)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (id, name, life_span, weight, height, temperament, breed_group, bred_for))
        except Exception as E:
            print("Error: {}".format(E))


def reactions():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    for record in records:
        try:
            results = record[1]
            reaction = results.get("reaction")
            veddra_version = reaction[0].get("veddra_version")
            veddra_term_code = reaction[0].get("veddra_term_code")
            veddra_term_name = reaction[0].get("veddra_term_name")
            crs.execute(f"""
            INSERT INTO reactions(unique_aer_id_number, veddra_version, veddra_term_code, veddra_term_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (record[0], veddra_version, veddra_term_code, veddra_term_name))
            # print(veddra_version)
            # print(veddra_term_code)
            # print(veddra_term_name)
        except Exception as E:
            print("Error: {}".format(E))


def weight():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    for record in records:
        try:
            animal_data = record[1].get("animal")
            weight = animal_data["weight"]
            print(age)
            min = weight.get("min")
            print(min)
            crs.execute(f"""
            INSERT INTO weight(unique_aer_id_number, min, unit)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (record[0], weight.get("min"), weight.get("unit")))
        except Exception as E:
            print("Error: {}".format(E))


def drugs():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    for record in records:
        try:
            drugs = record[1].get("drug")
            used_according_to_label = drugs[0].get("used_according_to_label")
            print(used_according_to_label)
            previous_exposure_to_drug = drugs[0].get("previous_exposure_to_drug")
            # brand_name = drugs[0].get("brand_name")
            dosage_form = drugs[0].get("dosage_form")
            atc_vet_code = drugs[0].get("atc_vet_code")
            crs.execute(f"""
            INSERT INTO drugs(unique_aer_id_number, used_according_to_label, previous_exposure_to_drug, dosage_form, atc_vet_code)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (record[0], used_according_to_label, previous_exposure_to_drug,
                   dosage_form, atc_vet_code))
        except Exception as E:
            print("Error: {}".format(E))


def health_assessment_prior_to_exposure():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    for record in records:
        try:
            health_assessment_prior_to_exposure = record[1].get("health_assessment_prior_to_exposure")
            condition = health_assessment_prior_to_exposure.get("condition")
            # assessed_by = health_assessment_prior_to_exposure.get("assessed_by")
            # print(assessed_by)
            crs.execute(f"""
            INSERT INTO health_assessment_prior_to_exposure(unique_aer_id_number, condition_of_animal)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """, (record[0], condition))
        except Exception as E:
            print("Error: {}".format(E))


def duration():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw LIMIT 1000000")

    records = crs.fetchall()

    for record in records:
        try:
            duration = record[1].get("duration")
            value = duration.get("value")
            unit = duration.get("unit")
            if unit == "Week":
                value = str(int(value) * 7)
            elif unit == "Month":
                value = str(int(value) * 30)
            print(unit)
            crs.execute(f"""
            INSERT INTO duration(unique_aer_id_number, value, unit)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (record[0], value, unit))
        except Exception as E:
            print("Error: {}".format(E))

def temperament():
    connection = psycopg2.connect(connection_name)
    connection.autocommit = True

    crs = connection.cursor()

    crs.execute("SELECT * FROM raw_dog LIMIT 1000")

    crs.execute(f"""
    INSERT INTO temperament (id, char1, char2, char3, char4, char5, char6)
    SELECT id
            ,split_part(temperament, ',', 1) AS col1
            ,split_part(temperament, ',', 2) AS col2
            ,split_part(temperament, ',', 3) AS col3
            ,split_part(temperament, ',', 4) AS col4
            ,split_part(temperament, ',', 5) AS col5
            ,split_part(temperament, ',', 6) AS col6
    FROM dog;
    """)


def normalize_tables():
    table_creation()
    health_assessment_prior_to_exposure()
    duration()
    results()
    animals()
    dog()
    age()
    weight()
    drugs()
    active_ingredients()
    reactions()
    temperament()
    incident_ai()


# normalize_tables()
