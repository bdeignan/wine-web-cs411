delimiter //
CREATE TRIGGER insert_review_count
    AFTER INSERT ON reviews
    FOR EACH ROW
BEGIN
    UPDATE users
    SET num_reviews =
        ( select count(description) from reviews where reviews.username = NEW.username)
    WHERE users.username = NEW.username;

    UPDATE users
    SET avg_rating =
        ( select AVG(points) from reviews where reviews.username = NEW.username)
    WHERE users.username = NEW.username;

END; //
delimiter ;

delimiter //
CREATE TRIGGER delete_review_count
    AFTER DELETE ON reviews
    FOR EACH ROW
BEGIN
    UPDATE users
    SET num_reviews =
        ( select count(description) from reviews where reviews.username = OLD.username)
    WHERE users.username = OLD.username;

    UPDATE users
    SET avg_rating =
        ( select AVG(points) from reviews where reviews.username = NEW.username)
    WHERE users.username = NEW.username;
END; //
delimiter ;







select trigger_name from information_schema.triggers;


UPDATE users
SET num_reviews =
    ( select count(description) from reviews where reviews.username = users.username)

UPDATE users
SET avg_rating =
    ( select avg(points) from reviews where reviews.username = users.username)
