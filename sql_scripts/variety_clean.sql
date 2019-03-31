update wines set variety = 'other' where variety in (select distinct (variety) from wines group by(variety) having count(variety) < 3);


update wines set variety = 'other' where variety in (
    select distinct (variety) from (select * from wines) as w group by(variety) having count(variety) < 3
    );


 SELECT DISTINCT (variety), count(variety) FROM (select * from wines) AS w GROUP BY(variety) HAVING count(variety) > 500;   

 select wine_name, count(wine_name) from reviews group by wine_name


 select winery, count(winery) from reviews, wines where reviews.wine_name = wines.wine_name group by winery having count(winery) > 100;


 SELECT winery, COUNT(winery) FROM reviews, wines WHERE reviews.wine_name = wines.wine_name GROUP BY winery ORDER BY count(winery) DESC LIMIT 20;


