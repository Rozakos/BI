import psycopg2
from init import *



#dogs

dog_commands = ("""
UPDATE dog SET bred_for = 'Unkown' WHERE bred_for ='';
UPDATE dog SET bred_for = 'Unkown' WHERE bred_for IS NULL;
UPDATE dog SET breed_group = 'Unkown' WHERE breed_group ='';
UPDATE dog SET breed_group = 'Unkown' WHERE breed_group IS NULL;
UPDATE dog SET temperament = 'Unkown' WHERE temperament IS NULL;
UPDATE dog SET temperament = 'Unkown' WHERE temperament ='';
""")


#animals
animals_commands = ("""
UPDATE animals SET reproductive_status = 'Unkown' WHERE reproductive_status IS NULL;
UPDATE animals SET gender = 'Unkown' WHERE gender is NULL;
DELETE FROM animals WHERE species != 'Dog';

""")


#drugs
drugs_commands = ("""
UPDATE drugs SET used_according_to_label = 'true' WHERE used_according_to_label ='True';
UPDATE drugs SET used_according_to_label = 'false' WHERE used_according_to_label ='False';
UPDATE drugs SET used_according_to_label = 'true' WHERE used_according_to_label ='True';
UPDATE drugs SET used_according_to_label = 'Unkown' WHERE used_according_to_label IS NULL;
UPDATE drugs SET previous_exposure_to_drug = 'Unkown' WHERE previous_exposure_to_drug IS NULL;
UPDATE drugs SET dosage_form = 'Unkown' WHERE dosage_form IS NULL;
""")


#reactions
reaction_commands = ("""
UPDATE reactions SET veddra_version = 'Unknown' WHERE veddra_version = '';
UPDATE reactions SET veddra_term_name = 'Unknown' WHERE veddra_term_name = '';
""")


#weight

weight_commands = ("""
DELETE FROM weight WHERE min IS NULL;
ALTER TABLE weight DROP COLUMN unit;
""")


#duration
duration_commands = ("""
DELETE FROM duration WHERE unit IS NULL;
DELETE FROM duration WHERE unit = 'Year';
DELETE FROM duration WHERE unit = 'Hour';
DELETE FROM duration WHERE unit = 'Minute';
DELETE FROM duration WHERE unit = 'Second';
DELETE FROM duration WHERE unit = '';
ALTER TABLE duration DROP COLUMN unit;
""")


#age
age_commands = ("""
DELETE FROM age WHERE unit !='Year';
DELETE FROM age WHERE unit IS NULL;
ALTER TABLE age DROP COLUMN unit;
""")


health_assessment_prior_to_exposure_commands = ("""
UPDATE health_assessment_prior_to_exposure SET condition_of_animal = 'Unknown' WHERE condition_of_animal='';
DELETE FROM health_assessment_prior_to_exposure WHERE condition_of_animal IS NULL;
""")

#results
results_commands = ("""
UPDATE results SET onset_date = 'Unkown' WHERE onset_date IS NULL;
UPDATE results SET onset_date = 'Unkown' WHERE onset_date = '';
UPDATE results SET primary_reporter = 'Unkown' WHERE primary_reporter IS NULL;
UPDATE results SET primary_reporter = 'Unkown' WHERE primary_reporter = '';
UPDATE results SET original_receive_date = 'Unkown' WHERE original_receive_date IS NULL;
UPDATE results SET original_receive_date = 'Unkown' WHERE original_receive_date = '';
""")


commands_list = [dog_commands, animals_commands, drugs_commands, reaction_commands, weight_commands, duration_commands,
                 age_commands, health_assessment_prior_to_exposure_commands, results_commands]


def clean_tables():
    try:
        connection = psycopg2.connect(connection_name)
        connection.autocommit = True
        crs = connection.cursor()

        for command in commands_list:
            crs.execute(command)
            # close communication with the PostgreSQL database server
            # crs.close()
            # commit the changes
            connection.commit()
        crs.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# clean_tables()
