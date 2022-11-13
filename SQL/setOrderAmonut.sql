CREATE OR REPLACE FUNCTION setOrderAmount() 
    BEGIN 

        select orderid, price, sum(quantity), price * sum(quantity) as totalAmount from orderdetail 
            group by orderid, price
            order by orderid;  

    END;