--Hacemos las llamadas necsarias para los procedimientos almacenados
\i updOrders.sql
\i updRatings.sql
\i setOrderAmount.sql

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


--Funcion de crear balances aleatorios
CREATE OR REPLACE FUNCTION setCustomersBalance(IN initialBalance bigint) RETURNS void AS $$
BEGIN
    UPDATE customers SET balance = floor(random()*initialBalance); 
END;
$$ LANGUAGE plpgsql;

--Llamada a funcion setCustomersBalance
SELECT setCustomersBalance(100);

--Modificamos las FK existentes para que cumplasn ON DELETE CASCADE
ALTER TABLE public.imdb_directormovies DROP CONSTRAINT imdb_directormovies_movieid_fkey;
ALTER TABLE public.imdb_directormovies ADD CONSTRAINT imdb_directormovies_movieid_fkey FOREIGN KEY (movieid) REFERENCES public.imdb_movies(movieid) ON DELETE CASCADE;
ALTER TABLE public.imdb_moviecountries DROP CONSTRAINT imdb_moviecountries_movieid_fkey;
ALTER TABLE public.imdb_moviecountries ADD CONSTRAINT imdb_moviecountries_movieid_fkey FOREIGN KEY (movieid) REFERENCES public.imdb_movies(movieid) ON DELETE CASCADE;
ALTER TABLE public.imdb_moviegenres DROP CONSTRAINT imdb_moviegenres_movieid_fkey;
ALTER TABLE public.imdb_moviegenres ADD CONSTRAINT imdb_moviegenres_movieid_fkey FOREIGN KEY (movieid) REFERENCES public.imdb_movies(movieid) ON DELETE CASCADE;
ALTER TABLE public.imdb_movielanguages DROP CONSTRAINT imdb_movielanguages_movieid_fkey;
ALTER TABLE public.imdb_movielanguages ADD CONSTRAINT imdb_movielanguages_movieid_fkey FOREIGN KEY (movieid) REFERENCES public.imdb_movies(movieid) ON DELETE CASCADE;
ALTER TABLE public.ratings DROP CONSTRAINT ratings_movieid_fkey;
ALTER TABLE public.ratings ADD CONSTRAINT ratings_movieid_fkey FOREIGN KEY (movieid) REFERENCES public.imdb_movies(movieid) ON DELETE CASCADE;
ALTER TABLE public.products  DROP CONSTRAINT products_movieid_fkey;   
ALTER TABLE public.ratings DROP CONSTRAINT ratings_customerid_fkey;
ALTER TABLE public.ratings ADD CONSTRAINT ratings_customerid_fkey FOREIGN KEY (customerid) REFERENCES public.customers(customerid) ON DELETE CASCADE;


--Añadimos las claves primarias y las dependencias entre claves
ALTER TABLE imdb_actormovies ADD CONSTRAINT FK_actorid FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid);
ALTER TABLE imdb_actormovies ADD CONSTRAINT FK_movieid FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid) ON DELETE CASCADE;
ALTER TABLE products ADD CONSTRAINT FK_movieid FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid) ON DELETE CASCADE;
ALTER TABLE inventory ADD CONSTRAINT FK_prod_id FOREIGN KEY (prod_id) REFERENCES products(prod_id) ON DELETE CASCADE;
ALTER TABLE orderdetail ADD CONSTRAINT FK_prod_id FOREIGN KEY (prod_id) REFERENCES products(prod_id) ON DELETE CASCADE;
ALTER TABLE orders ADD CONSTRAINT FK_customerid FOREIGN KEY (customerid) REFERENCES customers(customerid) ON DELETE CASCADE;
ALTER TABLE orderdetail ADD CONSTRAINT FK_orderid FOREIGN KEY (orderid) REFERENCES orders(orderid) ON DELETE CASCADE;
ALTER TABLE imdb_actormovies ADD CONSTRAINT PK_imdb_actormivies PRIMARY KEY (actorid,movieid);
--Hay tuplas duplicadas por lo que debemos eliminar una de ellas para poder crear la Primary Key (orderid, prod_id)
delete from orderdetail where (orderid, prod_id) in (
    SELECT orderid, prod_id
    FROM orderdetail
    GROUP BY orderid, prod_id
    HAVING COUNT(orderid) > 1);
delete from orderdetail where prod_id not in (select prod_id from inventory); --> Eliminamos pedidos que pudieran referenciar a un producto que no esta en inventario
ALTER TABLE orderdetail ADD CONSTRAINT PK_orderdetail Primary Key (orderid, prod_id); --> error por duplicadas

--Eliminamos las peliculas varios años de produccion (complican calculso en la base de datos)
DELETE FROM imdb_movies WHERE LENGTH(YEAR)>4;

--Trigger para cuando se mete o elimina una valoracion
CREATE OR REPLACE TRIGGER updateratings
AFTER DELETE OR INSERT ON ratings
FOR EACH ROW
EXECUTE PROCEDURE updateratingsfunc();

--Query setPrice.sql 
\i setPrice.sql


--Llamada a setOrderAmount()
select setOrderAmount();

--Tablas del catalogos para la informacion de las peliculas
CREATE TABLE imdb_catalogolanguage (
    id SERIAL PRIMARY KEY,
    language character varying(32) NOT NULL UNIQUE
);

INSERT INTO imdb_catalogolanguage (language) select DISTINCT language from imdb_movielanguages;
UPDATE imdb_movielanguages SET language = cm.id from imdb_catalogolanguage cm where cm.language = imdb_movielanguages.language;
ALTER TABLE imdb_movielanguages ALTER COLUMN language TYPE int USING language::integer;
ALTER TABLE imdb_movielanguages ADD CONSTRAINT foreign_key FOREIGN KEY(language) REFERENCES imdb_catalogolanguage(id);

CREATE TABLE imdb_catalogocountries (
    id SERIAL PRIMARY KEY, 
    countries character varying(32) NOT NULL UNIQUE
);
INSERT INTO imdb_catalogocountries(countries) select DISTINCT country from imdb_moviecountries;
UPDATE imdb_moviecountries SET country = cm.id from imdb_catalogocountries cm where cm.countries = imdb_moviecountries.country;
ALTER TABLE imdb_moviecountries ALTER COLUMN country TYPE int USING country::integer;
ALTER TABLE imdb_moviecountries ADD CONSTRAINT foreign_key FOREIGN KEY(country) REFERENCES imdb_catalogocountries(id);

CREATE TABLE imdb_catalogogenres(
    id SERIAL PRIMARY KEY,
    genres character varying(32) NOT NULL UNIQUE
);
INSERT INTO imdb_catalogogenres(genres) select DISTINCT genre from imdb_moviegenres;
UPDATE imdb_moviegenres SET genre = cm.id from imdb_catalogogenres cm where cm.genres = imdb_moviegenres.genre;
ALTER TABLE imdb_moviegenres ALTER COLUMN genre TYPE int USING genre::integer;
ALTER TABLE imdb_moviegenres ADD CONSTRAINT foreign_key FOREIGN KEY(genre) REFERENCES imdb_catalogogenres(id);




    


