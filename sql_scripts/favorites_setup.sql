--File to set up the favorites table

DROP TABLE IF EXISTS favorites;

CREATE TABLE favorites (
	taster_name VARCHAR(255) NOT NULL,
	wine_name VARCHAR(255) NOT NULL,
	PRIMARY KEY(taster_name, wine_name)
);