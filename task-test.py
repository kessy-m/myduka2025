# task...modify your select and insert functions to be able to select and insert data from any table
# hint-let let your function take parameters(table)

# simple example
def product_numbers(a,b):
    product = a * b
    return product

print(product_numbers(7,9))

# example 2
import psycopg2

conn = psycopg2.connect(user="postgres",password="12345",host="localhost",port="5432",database="school_db")
cur = conn.cursor()

def fetch_total_ages():
    cur.execute("select SUM(age) from students")
    total_age = cur.fetchall()
    return total_age
print(fetch_total_ages())



# <!-- jinja is a syntax wht i mean is thi {} -->
# <!-- so data is the variable so then in jinja we do passs it inside the syntax like this {data} -->


# task answer
def fetch_data(table):
    cur.execute(f"select * from {table}")
    data = cur.fetch()
    return data

students = fetch_data('students')
courses= fetch_data('courses')
print("students from fetch data func:\n",students)
print("print courses from fetch data func:\n",courses)
