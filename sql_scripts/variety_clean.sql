update wines set variety = 'other' where variety in (select distinct (variety) from wines group by(variety) having count(variety) < 3);


update wines set variety = 'other' where variety in (
    select distinct (variety) from (select * from wines) as w group by(variety) having count(variety) < 3
    );


 SELECT DISTINCT (variety), count(variety) FROM (select * from wines) AS w GROUP BY(variety) HAVING count(variety) > 500;   

 