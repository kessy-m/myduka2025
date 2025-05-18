# import flask to use it to build a flask applications
from flask import Flask, render_template,request, redirect,url_for,flash,session
from flask_bcrypt import Bcrypt
from database import fetch_products,fetch_sales,insert_products,insert_sales,confirm_user,insert_users,profit_per_product,profit_per_day,sales_per_product,sales_per_day,insert_stock,fetch_stock,available_stock,edit_product
from functools import wraps
# initiate our application - initialize our app
# flask instance

app = Flask(__name__)

app.secret_key='abcdefgh'

bcrypt = Bcrypt(app)



 
@app.route('/')
def home(): 
    name = "LOVELY PEOPLE" 
    return render_template('index.html', data=name)


def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected


@app.route('/trial')
def trial():
    flash('This is a test message')
    return render_template('test.html','danger')
    


@app.route('/products')
@login_required
def products():
    products = fetch_products()
    return render_template('products.html', products=products)


@app.route('/add_products',methods=['GET','POST'])
def add_products():
    if request.method == 'POST':
        product_name = request.form['p_name']
        buying_price = request.form['by_price']
        selling_price = request.form['s_price']

        new_product = (product_name,buying_price,selling_price)
        insert_products(new_product)

        return redirect(url_for('products'))


@app.route('/update_products' ,methods=['GET','POST'])
def update_products():
    if request.method =='POST':
        pid = request.form['pid']
        name = request.form['product_name']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']
        edited_product =(name,buying_price,selling_price,pid)
        edit_product(edited_product)
        flash('product eddited succesfully','success')
        return redirect(url_for('products'))




@app.route('/sales')
@login_required
def sales():
    sales = fetch_sales()
    products = fetch_products()
    return render_template('sales.html', mysales=sales , products=products)




@app.route('/add_sales',methods=['POST'])   
def add_sales():
   product_id = request.form['pid']
   quantity = request.form['quantity']
   new_sale = (product_id,quantity)
   stock_available = available_stock(product_id)
#    if stock_available is None:
#        flash('Invalid product id or no stock information available', 'danger')
#        return redirect(url_for('sales'))
    
   if stock_available < float(quantity):
       flash('insufficient stock', 'info')
       return redirect(url_for('sales'))
   

   insert_sales(new_sale)
   flash('sale made', 'success')

   return redirect(url_for('sales'))





@app.route('/dashboard')
@login_required
def dashboard():

    profit_product = profit_per_product()
    day_profit = profit_per_day()

    sales_product = sales_per_product()
    day_sales = sales_per_day()

# list comprehension to get individual data points
    product_name = [i[0] for i in profit_product]
    pr_profit = [float( i[1]) for i in profit_product]
    pr_sales = [float( i[1] )for i in sales_product]

#day metrics data
    date = [str(i[1]) for i in day_sales]
    d_sales = [float(i[1]) for i in day_sales]
    d_profit =[float(i[1]) for i in day_profit]


    return render_template('dashboard.html', 
    product_name=product_name,pr_profit=pr_profit,pr_sales=pr_sales,date=date,d_sales=d_sales,d_profit=d_profit)





@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone']
        password = request.form['password']
        

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
     
        user = confirm_user(email)
        if  not user:
            new_user =(full_name,email,phone_number,hashed_password)
            insert_users(new_user)
            return redirect(url_for('login'))
        else:
            print('already rgistered')
    return render_template('register.html')



@app.route('/login',methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':

       email = request.form['email']
       password = request.form['password']
       

       user= confirm_user(email)
       if not user:
           flash('user not found,please register','danger')
           return redirect(url_for('register'))
       else:
           if bcrypt.check_password_hash(user[-1], password):
            session['email'] = email
            return redirect(url_for('dashboard'))
           else:
               flash('wrong password','danger')
    return render_template('login.html')           





@app.route('/stock')
def stock():
    products=fetch_products()
    stock=fetch_stock()
    return render_template('stock.html',products=products,stock=stock)




@app.route('/add_stock',methods=['GET','POST'])
def add_stock():
    if request.method== 'POST':
        product_id=request.form['pid']
        stock_quantity=request.form['quantity']
        new_stock =(product_id,stock_quantity)
        insert_stock(new_stock)
        flash('stock added succesfully', 'success')

        return redirect(url_for('stock'))





@app.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    flash('you have been logged out','info')
    return redirect(url_for('login'))










    # new_users =(full_name,email,password)
    # insert_users(new_users)
# insert = f"insert into users(full_name, email, password){values}"



# run your application
# (debug=True--detects errors and chages)

app.run(debug=True)

