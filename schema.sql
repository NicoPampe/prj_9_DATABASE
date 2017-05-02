

DROP TABLE IF EXISTS lotr_words cascade;
CREATE TABLE lotr_words(
	id serial, 
	film TEXT, 
	chapter TEXT, 
	character TEXT, 
	race TEXT, 
	words TEXT);
-- copies from a file in the same directory. Wierd syntax for the Flowers db.
\copy lotr_words(film, chapter, character, race, words) FROM 'lotr_wordsSpoken.tsv';

DROP TABLE IF EXISTS factorio_recipe cascade;
CREATE TABLE factorio_recipe(
	id serial, 
	recipe TEXT, 
	resources TEXT, 
	amount TEXT); 
-- copies from a file in the same directory. Wierd syntax for the Flowers db.
\copy factorio_recipe(recipe, resources, amount) FROM 'factorio_recipe.csv' WITH (DELIMITER ',');

DROP TABLE IF EXISTS war_of_five_kings cascade;
CREATE TABLE war_of_five_kings(
	id serial, 
	name TEXT,
	year TEXT,
	battle_number TEXT,
	attacker_king TEXT,
	defender_king TEXT,
	attacker_1 TEXT,
	attacker_2 TEXT,
	attacker_3 TEXT,
	attacker_4 TEXT,
	defender_1 TEXT,
	defender_2 TEXT,
	defender_3 TEXT,
	defender_4 TEXT,
	attacker_outcome TEXT,
	battle_type TEXT,
	major_death TEXT,
	major_capture TEXT,
	attacker_size TEXT,
	defender_size TEXT,
	attacker_commander TEXT,
	defender_commander TEXT,
	summer TEXT,
	location TEXT,
	region TEXT,
	note TEXT);
\copy war_of_five_kings(name,year,battle_number,attacker_king,defender_king,attacker_1,attacker_2,attacker_3,attacker_4,defender_1,defender_2,defender_3,defender_4,attacker_outcome,battle_type,major_death,major_capture,attacker_size,defender_size,attacker_commander,defender_commander,summer,location,region,note) FROM 'war_of_the_five_kings_dataset.csv' WITH (DELIMITER ',');

