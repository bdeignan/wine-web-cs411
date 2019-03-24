SET SQL_SAFE_UPDATES = 0;
SET GLOBAL local_infile = 1;
CREATE database if not exists wine_web_2;
USE wine_web_2;

CREATE TABLE IF NOT EXISTS users ( 
    username VARCHAR(255) NOT NULL, 
    taster_name VARCHAR(255) NOT NULL,
    twitter VARCHAR(255), 
    email VARCHAR(255) NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    num_reviews INT DEFAULT 0, 
    avg_rating INT DEFAULT 0, 
    user_id BIGINT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (user_id),
    constraint UNIQUE(username),
    INDEX(username),
    INDEX(user_id)
);

LOAD DATA 
LOCAL INFILE '/Users/bmd/mcs-illinois/cs411-db-sys/data/tasters3.csv' 
INTO TABLE users 
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n' IGNORE 1 ROWS;

CREATE TABLE IF NOT EXISTS wines ( 
    wine_name VARCHAR(255) NOT NULL,  # need to normalize these better
    winery VARCHAR(255), # make this not null in the R script then add
    designation VARCHAR(255), 
    variety VARCHAR(255), 
    year SMALLINT,
    avg_price DECIMAL(5,2),
    wine_id BIGINT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (wine_name), 
    INDEX(wine_name),
    INDEX(wine_id),
    INDEX(winery)
);

LOAD DATA 
    LOCAL INFILE '/Users/bmd/mcs-illinois/cs411-db-sys/data/wines3.csv' 
    INTO TABLE wines 
    FIELDS TERMINATED BY ';' 
    -- OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n' IGNORE 1 ROWS;

CREATE TABLE IF NOT EXISTS reviews ( 
    username VARCHAR(255) NOT NULL,
    wine_name VARCHAR(255) NOT NULL,
    description MEDIUMTEXT,
    points SMALLINT,
    user_id BIGINT NOT NULL,
    PRIMARY KEY (user_id, wine_name),
    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
      ON UPDATE CASCADE
      ON DELETE CASCADE
)
;

LOAD DATA 
    LOCAL INFILE '/Users/bmd/mcs-illinois/cs411-db-sys/data/reviews3.csv' 
    INTO TABLE reviews
    FIELDS TERMINATED BY ';' 
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n' IGNORE 1 ROWS
    (@username, @wine_name, @description, @points)
    SET username = @username,
        wine_name =  @wine_name,
        description = @description,
        points = @points,
        user_id = 
        (
            SELECT user_id
            FROM users
            WHERE username = @username
            LIMIT 1
        )
;


CREATE TABLE IF NOT EXISTS winery ( # could add numeric winery_id
    winery VARCHAR(255), # need to clean these names of weird punct
    country VARCHAR(255), 
    region_1 VARCHAR(255), 
    PRIMARY KEY (winery)
);

LOAD DATA 
LOCAL INFILE '/Users/bmd/mcs-illinois/cs411-db-sys/data/winery3.csv' 
INTO TABLE winery 
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n' IGNORE 1 ROWS;