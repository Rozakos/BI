import psycopg2
from init import *


dim_weight = ("""
CREATE TABLE dim_weight
(
weight_ID SERIAL primary key,
min numeric(10,2)
);
""")


dim_age = ("""
CREATE TABLE dim_age
(
age_ID SERIAL primary key,
min numeric(10,2)
);
""")


dim_animals = ("""
CREATE TABLE dim_animals
(
unique_aer_id_number varchar(100) primary key,
species varchar(100),
gender varchar(100),
breed varchar(2000),
reproductive_status varchar(100),
weight_ID int,
age_ID int,
FOREIGN KEY (weight_ID) REFERENCES dim_weight(weight_ID),
FOREIGN KEY (age_ID) REFERENCES dim_age(age_ID)
);
""")


dim_dog = ("""
CREATE TABLE dim_dog
(
dog_id int primary key,
name varchar(100),
life_span int,
weight varchar(100),
height varchar(100),
breed_group varchar(100),
bred_for varchar(500)
);
""")


dim_duration = ("""
create table dim_duration
(
duration_id serial primary key,
value int
);
""")


dim_incident_ai = ("""
create table dim_incident_ai
(
id serial primary key,
ai_id int,
numerator numeric(10,2),
numerator_unit varchar(100),
denominator numeric(10,2),
denominator_unit varchar(100)
);
""")


dim_drugs = ("""
create table dim_drugs
(
drug_id serial primary key,
used_according_to_label varchar(100),
previous_exposure_to_drug varchar(100),
dosage_form varchar(100),
atc_vet_code varchar(100),
incident_ai_ID int,
FOREIGN KEY (incident_ai_ID) REFERENCES dim_incident_ai(id)
)
""")


dim_reactions = ("""
create table dim_reactions
(
reaction_id serial primary key,
veddra_version varchar(100),
veddra_term_code int,
veddra_term_name varchar(100)
);
""")


dim_health_assessment_prior_to_exposure = ("""
create table dim_health_assessment_prior_to_exposure
(
health_assessment_id serial primary key,
condition_of_animal varchar(100)
);

""")

dim_temperament = ("""
create table dim_temperament
(
temperament_id serial primary key,
dog_id int,
char1 varchar(100),
char2 varchar(100),
char3 varchar(100),
char4 varchar(100),
char5 varchar(100),
char6 varchar(100),
FOREIGN KEY (dog_id) REFERENCES dim_dog(dog_id)
);
""")


fact_results = ("""
create table fact_results
(
unique_aer_id_number varchar(100),
health_assessment_id int,
drug_id int,
reaction_id int,
duration_id int,
original_receive_date varchar(100),
primary_reporter varchar(100),
onset_date varchar(100),
report_id varchar(100),
FOREIGN KEY (unique_aer_id_number) REFERENCES dim_animals(unique_aer_id_number),
FOREIGN KEY (health_assessment_id) REFERENCES dim_health_assessment_prior_to_exposure(health_assessment_id),
FOREIGN KEY (drug_id) REFERENCES dim_drugs(drug_id),
FOREIGN KEY (reaction_id) REFERENCES dim_reactions(reaction_id),
FOREIGN KEY (duration_id) REFERENCES dim_duration(duration_id)
);
""")



table_list = [dim_weight, dim_age, dim_animals, dim_dog,
                 dim_duration, dim_incident_ai,
                 dim_drugs, dim_reactions, dim_health_assessment_prior_to_exposure,
                 dim_temperament, fact_results]


def data_warehouse():
    try:
        connection = psycopg2.connect(connection_name)
        connection.autocommit = True
        crs = connection.cursor()

        for command in table_list:
            crs.execute(command)
            connection.commit()
        crs.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)




# data_warehouse()
