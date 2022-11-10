
CREATE OR REPLACE FUNCTION setCustomersBalance(IN initialBalance bigint) RETURNS void AS $$
BEGIN
    UPDATE customers SET balance = floor(random()*initialBalance); 
END;
$$ LANGUAGE plpgsql;
