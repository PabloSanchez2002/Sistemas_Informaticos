
            WITH anno as (
                select(values (date_part('year',(SELECT current_timestamp)))) as ann),
            calc as(
                select movieid, year, (anno.ann - CAST( year AS INT)) as age 
                from imdb_movies, anno)
            
            select age from calc;


            /*
            UPDATE orderdetail ord
                SET price = precios.price
                from (select orderdetail.orderid, orderdetail.prod_id, products.price, from orderdetail
                    orderdetail join products on orderdetail.prod_id = products.prod_id) as precios
            
                WHERE ord.orderid = precios.orderid; */

    
