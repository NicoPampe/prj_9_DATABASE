

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
\copy factorio_recipe(recipe, resources, amount) FROM 'factorio_recipe.csv' WITH (DELIMITER ',');
