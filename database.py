import psycopg2
from datetime import datetime

now = datetime.now()

#create connection to db
conn = psycopg2.connect(user="postgres",password="12345",host="localhost",port="5432",database="myduka")


#executes database operations
cur = conn.cursor()


def fetch_products():
  #query fetching products 
     cur.execute("select * from products;")

     myproducts = cur.fetchall()
     return myproducts

#looping through the products
    #  for products in myproducts:
    #     print(products)


#query fetching sales
def fetch_sales():
    cur.execute("select * from sales")
    mysales = cur.fetchall()
    return mysales


# fetch users
def fetch_users():
    cur.execute("select * from users")
    myusers = cur.fetchall()
    return myusers

# #loopin thru sales
#     for sales in mysales:
#         print(sales)



# #inserting into
def insert_products():
   cur.execute("insert into products(name,buying_price,selling_price,stock_quantity)values('mangoes',200,500,20)")
conn.commit()
fetch_products()

# insert into sales
def insert_sales():
    cur.execute(f"insert into sales(pid,quantity,created_at)values(2,5,'{now}')")
    conn.commit()     
fetch_sales()

def insert_sales(values):
    insert = "insert into sales(pid,quantity,created_at)values(%s,%s,'now()')"
    cur.execute(insert,values)
    conn.commit()





# insert into users
def insert_users(user_info):
    query = "insert into users(full_name, email, password)values(%s,%s,%s)"
    cur.execute(query,user_info)
    conn.commit()

def confirm_user(email):
    query = 'select * from users where email = %s'
    cur.execute(query,(email,))
    user = cur.fetchone()
    return user






# conn.commit ---saves operations


def profit_per_product():
    cur.execute("""select products.name, sum((products.selling_price-products.buying_price)*sales.quantity) 
        from products join sales on products.id = sales.pid group by(products.name);""")
    profit_per_product = cur.fetchall()
    return profit_per_product


def profit_per_day():
    cur.execute("""select date(sales.created_at), sum((products.selling_price-products.buying_price)*sales.quantity)
         from products join sales on products.id = sales.pid group by(sales.created_at);""")
    profit_per_day = cur.fetchall()
    return profit_per_day


def sales_per_product():
    cur.execute("""select products.name, sum(products.selling_price * sales.quantity)
       from  products join sales on products.id = sales.pid group by(products.name);""")
    sales_per_product = cur.fetchall()
    return sales_per_product


def sales_per_day():
    cur.execute("""select date(sales.created_at), sum(products.selling_price * sales.quantity)
    from sales join products on products.id = sales.pid group by(sales.created_at);""")
    sales_per_day = cur.fetchall()
    return sales_per_day

    




# task review
# function to fetch data from any tablee of your choice
def fetch_data(table):
    cur.execute(f"select * from {table}")
    data = cur.fetchall()
    return data

products = fetch_data("products")
sales = fetch_data("sales")
print("products from fetch  data func:\n",products)
print("sales from fetch data func:\n",sales)



# insert products - 
# method 1- takes values as parameters 
# use parameters---the no of parameters has to be equal the no of columns

def insert_products(values):
    insert = "insert into products(name,buying_price,selling_price,stock_quantity)values(%s,%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

product1=("grapes",200,500,20)
product2=("laptop",40000,80000,10)
insert_products(product1)
insert_products(product2)

products = fetch_data("products")
# print("fetching products from fetch data func:\n",products)


# insert methods
# method 2---still takes parameters as values but we dont use the placeholders
# instead we replace the placeholders with {values} as parameters in a formatted string

def fetch_products_method_two(values):
    insert = f"insert into products(name,buying_price,selling_price,stock_quantity){values}"
    cur.execute(insert)
    conn.commit()

product_values = ("Yoghurt",100,300,20)
fetch_products_method_two = (product_values)

products = fetch_data("products")
print("fetching products from fetch products method two func:\n",products)



# insert products 
# method 2-- insert products function tht takes values as a parameter and uses formatted string

def insert_products_method_2(values):
    insert = f"insert into products(name,buying_price,selling_price,stock_quantity)values{values}"
    cur.execute(insert)
    conn.commit()



products2 = ("Tomatoes",100,300,20)
insert_products_method_2(products2)
products = fetch_data('products')
print("fetch products from fetch data method 2 func:\n",products)

