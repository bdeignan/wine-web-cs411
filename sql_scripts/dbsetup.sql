
USE wine_web;


CREATE TABLE users ( 
    taster_name VARCHAR(255) NOT NULL,
    twitter VARCHAR(255), 
    email VARCHAR(255) NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    username VARCHAR(255) NOT NULL, 
    num_reviews INT DEFAULT 0, 
    avg_rating INT DEFAULT 0, 
    PRIMARY KEY(taster_name)
);



CREATE TABLE wines ( 
    wine_name VARCHAR(255) NOT NULL, 
    winery VARCHAR(255), 
    designation VARCHAR(255), 
    avg_price DECIMAL(5,2), 
    variety VARCHAR(255), 
    year SMALLINT, 
    PRIMARY KEY (wine_name) 
);

LOAD DATA LOCAL INFILE '~/tasters.csv' INTO TABLE users FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

SELECT * FROM users;