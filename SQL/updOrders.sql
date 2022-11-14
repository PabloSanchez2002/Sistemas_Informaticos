CREATE OR REPLACE FUNCTION updordersfunc() 
RETURNS TRIGGER as $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        CREATE TABLE prueba_ins();

    ELSEIF (TG_OP = 'DELETE') THEN
        CREATE TABLE prueba_del();

    END IF;
    RETURN NULL;
END;
    $$ 
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER updOrders
AFTER DELETE OR INSERT ON orderdetail
FOR EACH ROW
EXECUTE PROCEDURE updordersfunc();

--181790,3796,,1