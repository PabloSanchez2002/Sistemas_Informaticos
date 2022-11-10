DELETE FROM ratings
WHERE customerid = 31 or customerid = 32 or customerid = 33 or customerid = 34;

--Comenatar las lineas de abajo para comporbar el delete
--INSERT INTO ratings VALUES (31, 172724, 4);
--INSERT INTO ratings VALUES (32, 172724, 5);
--INSERT INTO ratings VALUES (33, 172724, 3);
--INSERT INTO ratings VALUES (34, 172724, 4);

select * from imdb_movies where movieid = 172724 or movieid = 103;
select * from ratings