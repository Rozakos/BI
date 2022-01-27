import psycopg2

connection_name = "postgres://postgres:banana_2@localhost:5432/postgres"


load_weight = ("""
    insert into dim_weight(min)
    select distinct min from weight
    where not exists(select * from dim_weight);
    commit;
""")


load_age = ("""
	insert into dim_age(min)
	select distinct min from age
	where not exists(select * from dim_age);
    commit;
""")


load_animals = ("""
insert into dim_animals(unique_aer_id_number,species,gender,breed,
							reproductive_status,weight_ID,age_ID)
	select distinct a.unique_aer_id_number,a.species,a.gender
						,a.breed,a.reproductive_status
						,dw.weight_id,da.age_id
						from animals a
						left join weight w
						on w.unique_aer_id_number=a.unique_aer_id_number
						left join age ag
						on ag.unique_aer_id_number=a.unique_aer_id_number
						left join dim_weight dw
						on dw.min=w.min
						left join dim_age da
						on da.min=ag.min
					where not exists(select * from dim_animals);
commit;
""")


load_dog = ("""
	insert into dim_dog(dog_id,name,life_span,weight,height,breed_group,bred_for)
	select distinct id,name,life_span,weight,height,breed_group,bred_for
	from dog
	where not exists(select * from dim_dog);
    commit;
""")


load_duration = ("""
	insert into dim_duration(value)
	select distinct value from duration
	where not exists(select * from dim_duration);
    commit;
""")

load_incident_ai = ("""
	insert into dim_incident_ai(ai_id,numerator,numerator_unit,denominator,denominator_unit)
	select distinct ai_id,numerator,numerator_unit,denominator,denominator_unit from incident_ai
	where not exists(select * from dim_incident_ai);
    commit;
""")

load_drugs = ("""
    insert into dim_drugs(used_according_to_label,previous_exposure_to_drug,dosage_form,atc_vet_code,incident_ai_ID)
	select distinct d.used_according_to_label,d.previous_exposure_to_drug,d.dosage_form,d.atc_vet_code,di.id
	from drugs d
	left join incident_ai i
	on d.unique_aer_id_number=i.unique_aer_id_number
	left join dim_incident_ai di
	on di.ai_id=i.ai_id
	where not exists(select * from dim_drugs);
    commit;
""")


load_reactions = ("""
	insert into dim_reactions(veddra_version,veddra_term_code,veddra_term_name)
	select distinct veddra_version,veddra_term_code,veddra_term_name
	from reactions
	where not exists(select * from dim_reactions);
commit;
""")


load_health_assessment_prior_to_exposure = ("""
	insert into dim_health_assessment_prior_to_exposure(condition_of_animal)
	select distinct condition_of_animal from health_assessment_prior_to_exposure
	where not exists(select * from dim_health_assessment_prior_to_exposure);
    commit;
""")


load_temperament = ("""
insert into dim_temperament(dog_id,char1,char2,char3,char4,char5,char6)
select distinct d.id,t.char1,t.char2,t.char3,t.char4,t.char5,t.char6 
from temperament t
right join dog d
on d.id=t.id
where not exists(select * from dim_temperament);
commit;
""")


load_fact_result = ("""
	insert into fact_results(unique_aer_id_number,health_assessment_id,
							 drug_id,reaction_id,duration_id,
							 original_receive_date,primary_reporter,onset_date,
							 report_id)
	select distinct da.unique_aer_id_number,dh.health_assessment_id,
					dd.drug_id,drc.reaction_id,ddt.duration_id,
					r.original_receive_date,r.primary_reporter,r.onset_date,
					r.report_id
					from results r
					right join animals an
					on r.unique_aer_id_number=an.unique_aer_id_number
					inner join dim_animals da
					on da.unique_aer_id_number=an.unique_aer_id_number
					left join health_assessment_prior_to_exposure h
					on h.unique_aer_id_number=an.unique_aer_id_number
					left join dim_health_assessment_prior_to_exposure dh
					on h.condition_of_animal=dh.condition_of_animal
					left join drugs dr
					on dr.unique_aer_id_number=an.unique_aer_id_number
					left join dim_drugs dd
					on dd.atc_vet_code=dr.atc_vet_code
					left join reactions rc
					on rc.unique_aer_id_number=an.unique_aer_id_number
					left join dim_reactions drc
					on drc.veddra_version=rc.veddra_version
					and drc.veddra_term_code=rc.veddra_term_code
					left join duration dt
					on dt.unique_aer_id_number=an.unique_aer_id_number
					left join dim_duration ddt 
					on dt.value=ddt.value
					where not exists(select * from fact_results);
commit;
""")


command_list = [load_fact_result]


def create_dimensions():
    try:
        connection = psycopg2.connect(connection_name)
        connection.autocommit = True
        crs = connection.cursor()

        for command in command_list:
            crs.execute(command)
            # close communication with the PostgreSQL database server
            # crs.close()
            # commit the changes
            connection.commit()
        crs.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        # connection = psycopg2.connect(connection_name)
        # connection.autocommit = True
        # crs = connection.cursor()


# create_dimensions()
