CREATE OR REPLACE FUNCTION setOrderAmount() 
    RETURNS VOID
    AS $$   
    BEGIN 
        update orders
        set netamount = aux.precio from (
        
        with total as (select orderid, price * sum(quantity) as totalAmount from orderdetail 
            group by orderid, price)
        select orderid, sum(totalAmount) as precio from total
            group by total.orderid) as aux
        where orders.orderid = aux.orderid;

        update orders
        set totalAmount = netamount*(100 + tax)/100;
    END;
    $$
LANGUAGE 'plpgsql';
