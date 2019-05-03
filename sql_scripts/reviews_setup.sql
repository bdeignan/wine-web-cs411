--File to set up the reviews table from csv

-- Need to remove all columns from description field and replace with ; or other character

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
    review_id MEDIUMINT NOT NULL AUTO_INCREMENT, 
    taster_name VARCHAR(255) NOT NULL,
    wine_name VARCHAR(255) NOT NULL, 
    description VARCHAR(1056), 
    rating INT DEFAULT 0, 
    PRIMARY KEY(review_id)
);

LOAD DATA LOCAL INFILE '/home/server/csv_files/reviews.csv' INTO TABLE reviews FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;




SELECT country, avg(points) FROM winery, wines, reviews where winery.winery = wines.winery  AND reviews.wine_name = wines.wine_name GROUP BY country;