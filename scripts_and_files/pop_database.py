import pandas as pd
from ..web import connection

# Loading datas
xls = pd.ExcelFile('scripts_and_files/my_shop_data.xlsx')
df_customers = pd.read_excel(xls, 'customers')
df_orders = pd.read_excel(xls, 'order')
df_employees = pd.read_excel(xls, 'employee')
df_products = pd.read_excel(xls, 'products')
df_geodata = pd.read_csv('scripts_and_files/iso_alpha_dataset.csv')

# Normalizing data
df_customers['country'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_geodata = df_geodata[['Country', 'Latitude (average)', 'Longitude (average)']].replace('"', '', regex=True)
df_geodata = df_geodata.rename(columns={'Country': 'country', 'Latitude (average)': 'lat', 'Longitude (average)':'lon'})
df_geodata['country'] = df_geodata['country'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Sending Data to database at Azure and setting primary key:
conn = connection.conn()

df_customers.to_sql('customers', conn, if_exists='replace', index=False)
with conn.connect() as con:
    con.execute('''ALTER TABLE customers ADD PRIMARY KEY (customer_id);''')
df_orders.to_sql('orders', conn, if_exists='replace', index=True)
with conn.connect() as con:
    con.execute('''ALTER TABLE orders ADD PRIMARY KEY (index);''')
df_employees.to_sql('employees', conn, if_exists='replace', index=False)
with conn.connect() as con:
    con.execute('''ALTER TABLE employees ADD PRIMARY KEY (employee_id);''')
df_products.to_sql('products', conn, if_exists='replace', index=False)
with conn.connect() as con:
    con.execute('''ALTER TABLE products ADD PRIMARY KEY (product_id);''')
df_geodata.to_sql('geodata', conn, if_exists='replace', index=True)
with conn.connect() as con:
    con.execute('''ALTER TABLE geodata ADD PRIMARY KEY (index);''')


# To read the files directly from database:
df_customers = pd.read_sql("select * from \"customers\"", conn)
df_orders = pd.read_sql("select * from \"orders\"", conn)
df_employee = pd.read_sql("select * from \"employees\"", conn)
df_products = pd.read_sql("select * from \"products\"", conn)
