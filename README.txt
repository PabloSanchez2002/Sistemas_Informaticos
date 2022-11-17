Para el correcto funcionamiento de la pagina web desplegada sobre el servidor de apache es posible que sea necersario ejecutarel siguiente comando en el directorio /public_html:
~$ sudo chmod 777 -R *

En caso de no ejecutarse la funcion getTopSales en la plataforma, ejecutar este script de sql:

update imdb_movies set movietitle = replace(movietitle,'''', '`');

Este esta incluido tambien en actualiza.sql pero a veces no funciona correctamete.