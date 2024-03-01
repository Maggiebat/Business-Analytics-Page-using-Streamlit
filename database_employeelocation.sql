create table employeelocation (
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    lon double,
	lat double,
    countryindex int,
    isocode varchar(255),
    city varchar(255)
)

insert into employeelocation (department) 
select distinct customers.Department
from customers

insert into employeelocation (city) 
select distinct customers.City
from customers