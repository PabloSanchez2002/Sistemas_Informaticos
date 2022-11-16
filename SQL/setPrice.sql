
    update orderdetail
    set price = aux.precio from (
    select orderid, ord2.prod_id, round (p.price/(1.02^((extract (year from current_date) - extract (year from orderdate)))), 2) as precio 
    from orders as ord natural join orderdetail as ord2 join products as p on p.prod_id = ord2.prod_id) as aux

    where orderdetail.prod_id = aux.prod_id and orderdetail.orderid = aux.orderid;

