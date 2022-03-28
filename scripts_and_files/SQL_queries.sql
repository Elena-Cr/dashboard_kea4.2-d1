DROP VIEW IF EXISTS prod_order CASCADE;
CREATE VIEW prod_order as
select orders.*, products.productname, 
products.stock, products.type 
from products join orders 
on products.product_id = orders.product_id 
order by products.stock asc;

DROP VIEW IF EXISTS prod_order_cust CASCADE;
CREATE VIEW prod_order_cust as
select prod_order.*, 
customers.first_name, customers.last_name,
customers.country,
(prod_order.unitprice * prod_order.quantity) as sale,
CONCAT(prod_order.customer_id, ' - ', customers.first_name, 
 ' ', customers.last_name) as id_and_name,
geodata.lon, geodata.lat
from prod_order join customers
on customers.customer_id = prod_order.customer_id
join geodata on customers.country = geodata.country;

DROP VIEW IF EXISTS scatter_sales CASCADE;
create view scatter_sales as
select country, lon, lat, id_and_name,
/*unitprice, quantity, sale,*/
SUM(sale) as total_sale
from prod_order_cust
group by country, lon, lat, id_and_name 
order by country asc;

DROP VIEW IF EXISTS order_emp_best CASCADE;
create view order_emp_best as
select  employees.employee_id, 
CONCAT(employees.firstname, ' ', employees.lastname) as fullname,
SUM(tbl2.total_sale) as total_sale
from 
(select orders.employee_id,
(orders.quantity * orders.unitprice) as total_sale 
 from orders) tbl2
join employees on 
tbl2.employee_id = employees.employee_id
group by employees.employee_id
order by total_sale desc;


DROP VIEW IF EXISTS prod_order_cust_emp CASCADE;
create view prod_order_cust_emp as
select  tbl2.order_id, tbl2.employee_id,
tbl2.productname, tbl2.orderdate,
employees.firstname, employees.lastname,
tbl2.sale, tbl2.type,
tbl2.quantity, tbl2.country,
tbl2.first_name, tbl2.last_name 
 from (select prod_order_cust.* from prod_order_cust) as tbl2
join employees on 
tbl2.employee_id = employees.employee_id
group by tbl2.order_id, tbl2.productname, tbl2.orderdate,
employees.firstname, employees.lastname,
tbl2.sale, tbl2.type, tbl2.employee_id,
tbl2.quantity, tbl2.country,
tbl2.first_name, tbl2.last_name 
order by tbl2.orderdate desc;

