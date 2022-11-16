CREATE OR REPLACE function getTopActors(generoINPUT varchar(32))
RETURNS TABLE(
    actorname varchar(128),
    num bigint,
    debut text,
    movietitle varchar(255),
    director varchar(128)
)
AS $$
BEGIN
return query
with c(
    movieid, actorname, movietitle, directorname,year 
) as (
        select m.movieid, a.actorname, m.movietitle, d.directorname, m.year
        from imdb_catalogogenres cg join imdb_moviegenres mg on cg.id = mg.genre 
        join imdb_movies m on m.movieid = mg.movieid join imdb_actormovies am on am.movieid = m.movieid join imdb_actors a on a.actorid = am.actorid 
        join imdb_directormovies dm on dm.movieid = m.movieid join imdb_directors d on d.directorid = dm.directorid 
        where cg.genres = generoINPUT
),

d(
    movieid, actorname, movietitle, directorname,year
) as (
    select distinct on (c.actorname, c.movietitle) c.movieid, c.actorname, c.movietitle, c.directorname, c.year 
    from c
),

b(
    actorname, num
) as (
    select distinct d.actorname, count(*) over (partition by d.actorname) as num 
    from d
),

a(
    actorname, debut
) as (
    select a.actorname, min(m.year) as debut 
    from imdb_movies m join imdb_actormovies am on am.movieid = m.movieid
    join imdb_actors a on a.actorid = am.actorid join imdb_moviegenres mg on mg.movieid = m.movieid join imdb_catalogogenres cg on cg.id = mg.genre 
    where cg.genres = generoINPUT 
    group by a.actorname) 

select c.actorname, b.num, a.debut, c.movietitle, c.directorname 
from c join b on c.actorname = b.actorname join a on a.actorname = c.actorname and a.debut = c.year 
where b.num > 4 
order by num desc, actorname;

END;
$$
LANGUAGE 'plpgsql';

