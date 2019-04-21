CREATE VIEW country_prices AS
    SELECT AVG(avg_price) as price,country FROM wines, winery WHERE wines.winery = winery.winery AND winery.country != '' GROUP BY winery.country;