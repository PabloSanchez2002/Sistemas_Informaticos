CREATE OR REPLACE FUNCTION updordersfunc() 
RETURNS TRIGGER as $$
DECLARE
    extra int4;
BEGIN
    IF (TG_OP = 'INSERT') THEN
        extra := (select o.netamount from orders o where o.orderid = new.orderid);
        UPDATE orders set netamount = extra + (new.price*new.quantity) where orders.orderid = new.orderid;
        UPDATE orders set totalamount = (netamount + (netamount*tax/100)) where orders.orderid = new.orderid;
    ELSEIF (TG_OP = 'DELETE') THEN
        extra := (select o.netamount from orders o where o.orderid = old.orderid);
        UPDATE orders set netamount = extra - (old.price*old.quantity) where orders.orderid = old.orderid;
        UPDATE orders set totalamount = (netamount + (netamount*tax/100)) where orders.orderid = old.orderid;
    ELSEIF (TG_OP = 'UPDATE') THEN
        extra := (select o.netamount from orders o where o.orderid = old.orderid);
        extra := extra - (old.price*old.quantity);
        UPDATE orders set netamount = extra + (new.price*new.quantity) where orders.orderid = new.orderid;
        UPDATE orders set totalamount = (netamount + (netamount*tax/100)) where orders.orderid = new.orderid;


        
    END IF;
    RETURN NULL;
END;
    $$ 
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER updOrders
AFTER DELETE OR INSERT OR UPDATE ON orderdetail
FOR EACH ROW
EXECUTE PROCEDURE updordersfunc();

--181790,3796,,1