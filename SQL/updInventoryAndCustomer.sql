CREATE OR REPLACE FUNCTION updInventory() RETURNS TRIGGER AS $$
DECLARE
    prod record;
BEGIN
    FOR prod IN
        -- Iteramos por todos los productos del orderid que
        -- hace ejecutar el trigger al finalizar una compra
        SELECT
            orderdetail.prod_id, sales, quantity, stock
        FROM
            orderdetail,
            inventory
        WHERE
            OLD.orderid = orderdetail.orderid AND
            inventory.prod_id = orderdetail.prod_id

    -- Actualizamos el inventorio de cada producto del order
    LOOP
        UPDATE inventory
        SET
            stock = prod.stock - prod.quantity,
            sales = prod.sales + prod.quantity
        WHERE
            inventory.prod_id = prod.prod_id;
        /*
        -- En caso de que no haya stock, añadimos una alerta
        IF (prod.quantity >= prod.stock) THEN
            INSERT INTO alertas
            VALUES (prod.prod_id, NOW(), prod.stock - prod.quantity);
        END IF;
        */
    END LOOP;
    --Quitamos del saldo del cliente el precio del pedido 
    UPDATE customers set
        balance = balance - old.totalamount;

    -- Actualizamos el orderdate de la tabla orders
    NEW.orderdate = 'NOW()';

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Creamos el trigger que actualiza las tablas inventory y orders cuando
-- se finalice la compra (status = Paid). También crea una alerta en la
-- tabla alertas cuando el stock de alguna película a comprar llega a cero
CREATE OR REPLACE TRIGGER updInventory
BEFORE UPDATE OF STATUS ON orders
FOR EACH ROW
    WHEN (NEW.status = 'Paid')
    EXECUTE PROCEDURE updInventory();

/* PARA PROBAR COSAS
select * from customers where customerid = 9557;
UPDATE public.orders SET customerid=9557,  status='Paid' WHERE orderid=123456;
select * from orders where orderid=123456;
*/