

drop table if exists lotr_words cascade;
CREATE TABLE lotr_words(
	id serial, 
	film TEXT, 
	chapter TEXT, 
	character TEXT, 
	race TEXT, 
	words TEXT);
-- copies from a file in the same directory. Wierd syntax for the Flowers db.
\copy lotr_words(film, chapter, character, race, words) FROM 'lotr_wordsSpoken.tsv';

