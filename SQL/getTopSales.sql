CREATE OR REPLACE function getTopSales(year1 INT, year2 INT)
RETURNS TABLE(
    year INT,
    movietitle varchar(255),
    num bigint
)
AS $$
BEGIN
return query

with a(movietitle, sells, year)
as (
select im.movietitle, sum(o.quantity)::bigint as sells, extract(year from orderdate) as new_year 
from orders os join orderdetail o on os.orderid = o.orderid join products p on o.prod_id = p.prod_id join imdb_movies im on im.movieid = p.movieid 
where extract(year from orderdate) >= year1 and extract(year from orderdate) <= year2  group by im.movietitle, new_year order by im.movietitle
),
b (year, sells) as(
select a.year, max(sells) from a group by a.year
)
select b.year::int, a.movietitle, b.sells from a join b on a.sells = b.sells and a.year = b.year order by b.sells desc;

END;
$$
LANGUAGE 'plpgsql'


