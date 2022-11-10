ALTER TABLE customers ADD COLUMN balance int;
CREATE TABLE ratings (
    customerid  int not null REFERENCES customers(customerid),
    movieid int not null REFERENCES imdb_movies(movieid),
    rated int not null check(rated >= 0 and rated <= 5),
    PRIMARY KEY(customerid, movieid)
);
ALTER TABLE imdb_movies ADD COLUMN ratingmean int DEFAULT 0;
ALTER TABLE imdb_movies ADD COLUMN ratingcount int DEFAULT 0;
ALTER TABLE customers ALTER COLUMN password TYPE character varying(96);
SELECT setCustomersBalance(100);

CREATE OR REPLACE TRIGGER updateratingsADD
AFTER INSERT ON ratings
FOR EACH ROW
EXECUTE PROCEDURE updateratingsfuncADD();

CREATE OR REPLACE TRIGGER updateratingsDEL
AFTER DELETE ON ratings
FOR EACH ROW
EXECUTE PROCEDURE updateratingsfuncDEL();

    


