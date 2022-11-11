--Añadimos valor balance a customer
ALTER TABLE customers ADD COLUMN balance int;

--Creamos tabla ratings
CREATE TABLE ratings (
    customerid  int not null REFERENCES customers(customerid),
    movieid int not null REFERENCES imdb_movies(movieid),
    rated int not null check(rated >= 0 and rated <= 5),
    PRIMARY KEY(customerid, movieid)
);

--Añadimos columnas a tabla imdb_movies
ALTER TABLE imdb_movies ADD COLUMN ratingmean int DEFAULT 0;
ALTER TABLE imdb_movies ADD COLUMN ratingcount int DEFAULT 0;

--Cambiamos el tipo de password a 96 caracteres
ALTER TABLE customers ALTER COLUMN password TYPE character varying(96);




--
CREATE OR REPLACE FUNCTION setCustomersBalance(IN initialBalance bigint) RETURNS void AS $$
BEGIN
    UPDATE customers SET balance = floor(random()*initialBalance); 
END;
$$ LANGUAGE plpgsql;

--setCustomersBalance()
SELECT setCustomersBalance(100);



--Añadimos las claves primarias y las dependencias entre claves
ALTER TABLE foo_table ADD CONSTRAINT fk_e52ffdeea76ed395 FOREIGN KEY (user_id) REFERENCES users (another_id) ON DELETE CASCADE;


--
CREATE OR REPLACE TRIGGER updateratingsADD
AFTER INSERT ON ratings
FOR EACH ROW
EXECUTE PROCEDURE updateratingsfuncADD();




CREATE OR REPLACE TRIGGER updateratingsDEL
AFTER DELETE ON ratings
FOR EACH ROW
EXECUTE PROCEDURE updateratingsfuncDEL();

    


