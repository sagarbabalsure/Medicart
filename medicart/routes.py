from flask import *
from medicart.form import *
import hashlib
from medicart import app,cur,db
from werkzeug import url_encode



@app.route('/')
def index():
	return render_template('index.html')


@app.route('/buyer_login',methods=['GET','POST'])
def buyer_login():
	error=""
	form = LoginForm()
	if request.method =='POST' and form.validate_on_submit():
		username = form.username.data
		password = hashlib.sha256(form.password.data.encode()).hexdigest()
		data = cur.execute("SELECT username,password from buyer_register where username=%s and password=%s",(username,password))
		data = cur.fetchone()
		if data:
			session["logged_in"] = True
			session["username"] = form.username.data
			flash("Now you are logged in")
			return redirect(url_for('homepage'))
		else:
			error="Invalid username or password"
	return render_template("login.html",error=error,form=form,title='Buyer')


@app.route('/buyer_register',methods=['GET','POST'])
def buyer_register():
	form = RegisterForm()
	if request.method == 'POST' and form.validate_on_submit():
		name = form.name.data
		username = form.username.data
		email = form.email.data
		password = hashlib.sha256(form.password.data.encode()).hexdigest()
		data = cur.execute("SELECT * from buyer_register where username=%s",(username))
		if data > 0:
			flash("Username is already taken")
		else:
			query = "INSERT INTO buyer_register (name,username,email,password) values (%s,%s,%s,%s)"
			cur.execute(query,(name,username,email,password))
			db.commit()
			flash("Congragulation you have registered successfully")
			return redirect(url_for('buyer_login'))

	return render_template("register.html",form=form,title='Buyer')


@app.route('/seller_login',methods=['GET','POST'])
def seller_login():
	error=""
	form = LoginForm()
	if request.method == 'POST' and form.validate_on_submit():
		username = form.username.data
		password = hashlib.sha256(form.password.data.encode()).hexdigest()
		data = cur.execute("SELECT username,password from seller_register where username=%s and password=%s",(username,password))
		data = cur.fetchone()
		if data:
			session["logged_in"] = True
			session["username"] = form.username.data
			flash("Now you are logged in")
			return redirect(url_for('homepage'))
		else:
			error="invalid username or password"
	return render_template("login.html",error=error,form=form,title='Seller')


@app.route('/seller_register',methods=['GET','POST'])
def seller_register():
	form = RegisterForm()
	if request.method == 'POST' and form.validate_on_submit():
		name = form.name.data
		username = form.username.data
		email = form.email.data
		password = hashlib.sha256(form.password.data.encode()).hexdigest()
		data = cur.execute("SELECT * from seller_register where username=%s",(username))
		if data > 0:
			flash("Username is already taken")
		else:
			query = "INSERT INTO seller_register (name,username,email,password) values (%s,%s,%s,%s)"
			cur.execute(query,(name,username,email,password))
			db.commit()
			flash("Congragulation you have registered successfully")
			return redirect(url_for('seller_login'))

	return render_template("register.html",form=form,title='Seller')

@app.route('/profile')
def profile():
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		# print(mode['mode'])
		if mode:
			data = cur.execute("SELECT * from buyer_register where username=%s",(username))
			data = cur.fetchone()
			return render_template("profile.html",data=data,mode='Buyer')
		else:
			data = cur.execute("SELECT * from seller_register where username=%s",(username))
			data = cur.fetchone()
			return render_template("profile.html",data=data)
	else:
		return render_template('index.html')

@app.route('/homepage')
def homepage():
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			cur.execute("SELECT * FROM Items")
			data = cur.fetchall()
			return render_template('homepage_data.html',homepage_data=data)
		else:
			return redirect(url_for('add_medicine'))
	else:
		return render_template('index.html')


@app.route('/logout')
def logout():
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			session.clear()
			flash("you have been loggod out")
			return redirect(url_for('buyer_login'))
		else:
			session.clear()
			flash("you have been loggod out")
			return redirect(url_for('seller_login'))
	else:
		return render_template('index.html')


@app.route('/edit_profile',methods=['GET','POST'])
def edit_profile():
	
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			form = EditBuyerProfile()
			cur.execute("SELECT * from buyer_register where username=%s",(username))
			data = cur.fetchone()
			if request.method == 'POST' and form.validate_on_submit():
				email = form.email.data
				mobile_no = form.mobile_no.data
				print(mobile_no)
				address = form.address.data
				print(address)
				about_me = form.about_me.data
				print(about_me)
				query = "UPDATE buyer_register SET email=%s,mobile_no=%s,address=%s,about_me=%s where username=%s"
				cur.execute(query,(email,mobile_no,address,about_me,username))
				db.commit()
				flash("Your profile is updated")
				return redirect(url_for('profile'))
			return render_template("edit_profile.html",form=form,data=data,mode="Buyer")
		else:
			form = EditSellerProfile()
			cur.execute("SELECT * from seller_register where username=%s",(username))
			data = cur.fetchone()
			if request.method == 'POST' and form.validate_on_submit():
				email = form.email.data
				mobile_no = form.mobile_no.data
				company = form.company.data
				about_me = form.about_me.data
				query = "UPDATE seller_register SET email=%s,mobile_no=%s,company_name=%s,about_me=%s where username=%s"
				cur.execute(query,(email,mobile_no,company,about_me,username))
				db.commit()
				flash("Your profile is updated")
				return redirect(url_for('profile'))
			return render_template("edit_profile.html",form=form,data=data)
	return render_template('index.html')





@app.route('/view-orders')
def view_orders():
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			cur.execute("SELECT Buyer_id from buyer_register where username=%s",(username))
			buyer_id = cur.fetchone()
			cur.execute("SELECT product_id from confirmed_order where buyer_id=%s",(buyer_id['Buyer_id']))
			product_ids = cur.fetchall()
			list1 = []
			for i in range(0,len(product_ids)):
				cur.execute("SELECT  * from Items where product_id=%s",(product_ids[i]['product_id']))
				data = cur.fetchall()
				list1.append(data)	
			return render_template('view_orders.html',data=list1)
		return redirect(url_for('buyer_login'))

@app.route('/search-by-name',methods=['GET','POST'])
def search():
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			if request.method == 'POST':
				search_key = request.form['search']
				cur.execute("SELECT * from Items where medicine_name=%s",(search_key))
				data = cur.fetchall()
				return render_template('homepage_data.html',searched_data=data)
			return render_template('buyer_homepage.html')
		return redirect(url_for('buyer_login'))



@app.route('/add_medicine',methods=['GET','POST'])
def add_medicine():
	form = AddMedicine()
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from seller_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			cur.execute("SELECT Seller_id from seller_register where username=%s",(username))
			S_id = cur.fetchone()
			if request.method == "POST" and form.validate_on_submit():
				medicine_name = form.medicine_name.data
				manufacturer = form.manufacturer.data
				price = form.price.data
				stock = form.stock.data
				composition = form.composition.data
				precaution = form.precaution.data
				description = form.medicine_description.data
				query = "INSERT INTO Items (medicine_name,manufacturer,price,stock,description,composition,precaution,seller_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
				cur.execute(query,(medicine_name,manufacturer,price,stock,description,composition,precaution,S_id['Seller_id']))
				db.commit()
				flash("Medicine information added")
				return redirect(url_for('homepage'))
			return render_template('add_medicine.html',form=form)
		return redirect(url_for('seller_login'))


@app.route('/seller-added-products')
def added_products():
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from seller_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			cur.execute("SELECT Seller_id from seller_register where username=%s",(username))
			S_id = cur.fetchone()
			cur.execute("SELECT * from Items where seller_id=%s",(S_id['Seller_id']))
			data = cur.fetchall()
			return render_template('seller_added_products.html',data=data)
		return redirect(url_for('seller_login'))


@app.route('/update-medicine-data/<int:product_id>',methods=['GET','POST'])
def update_medicine(product_id):
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from seller_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			form=UpdateMedicineData()
			cur.execute("SELECT * from Items where product_id=%s",(product_id))
			data = cur.fetchone()
			if request.method == 'POST' and form.validate_on_submit():
				medicine_name = form.medicine_name.data
				price = form.price.data
				stock = form.stock.data
				query = "UPDATE Items SET medicine_name=%s,price=%s,stock=%s where product_id=%s"
				cur.execute(query,(medicine_name,price,stock,product_id))
				db.commit()
				return redirect(url_for('added_products'))
			return render_template('update_medicine_data.html',form=form,data=data)
		return redirect(url_for('seller_login'))

@app.route('/product_page/<int:product_id>')
def product_page(product_id):
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			cur.execute("SELECT * from Items where product_id=%s",(product_id))
			data = cur.fetchall()
			return render_template('product_page.html',data=data)
	return redirect(url_for('buyer_login'))


@app.route('/AddToCart<int:product_id>')
def add_to_cart(product_id):
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			cur.execute("SELECT Buyer_id from buyer_register where username=%s",(username))
			buyer_id = cur.fetchone()
			query = "INSERT INTO cart values(%s,%s)"
			cur.execute(query,(product_id,buyer_id['Buyer_id']))
			db.commit()
			flash("product added to cart")
			return redirect(url_for('product_page',product_id=product_id))
		return redirect(url_for('buyer_login'))

@app.route('/show_cart')
def show_cart():
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT Buyer_id from buyer_register where username=%s",(username))
		buyer_id = cur.fetchone()
		cur.execute("SELECT product_id from cart where buyer_id=%s",(buyer_id['Buyer_id']))
		product_ids = cur.fetchall()
		list1 = []
		for i in range(0,len(product_ids)):
			cur.execute("SELECT  * from Items where product_id=%s",(product_ids[i]['product_id']))
			data = cur.fetchall()
			list1.append(data)	
		return render_template('show_cart.html',data=list1,product_ids=product_ids)

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			cur.execute("DELETE FROM cart where product_id=%s",(product_id))
			db.commit()
			return redirect(url_for('homepage'))
		return redirect(url_for('buyer_login'))


@app.route('/buy/<int:product_id>')
def buy(product_id):
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			cur.execute("SELECT * from Items where product_id=%s",(product_id))
			data = cur.fetchall()
			return render_template('order_page.html',data=data)
		return redirect(url_for('buyer_login'))

@app.route('/confirm-order/<int:product_id>/<int:seller_id>',methods=['GET','POST'])
def confirm_order(product_id,seller_id):
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from buyer_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			username = session['username']
			if request.method == 'POST':
				quantity = request.form['quantity']

			cur.execute("SELECT Buyer_id from buyer_register where username = %s",(username))
			buyer_id = cur.fetchone()
			query = "INSERT INTO confirmed_order values(%s,%s,%s,%s)"
			cur.execute(query,(buyer_id['Buyer_id'],product_id,quantity,seller_id))
			db.commit()
			cur.execute("SELECT stock from Items where product_id=%s",(product_id))
			stock = cur.fetchone()
			new_stock = (stock['stock'] - int(quantity))
			query = "UPDATE Items SET stock=%s where product_id=%s"
			cur.execute(query,(new_stock,product_id))
			db.commit()
			return render_template("last.html")
		return redirect(url_for('buyer_login'))
	return render_template('index.html')

@app.route('/manage-orders')	
def manage_orders():
	if 'username' in session:
		username = session['username']
		cur.execute("SELECT mode from seller_register where username=%s",(username))
		mode = cur.fetchone()
		if mode:
			cur.execute("SELECT Seller_id from seller_register where username=%s",(username))
			seller_id = cur.fetchone()
			cur.execute("SELECT * from confirmed_order where seller_id=%s",(seller_id['Seller_id']))
			ids = cur.fetchall()
			finallist = list()
			for i in range(0,len(ids)):
				templist = []
				cur.execute("SELECT medicine_name from Items where product_id=%s", (ids[i]['product_id']))
				med_name = cur.fetchone()
				templist.append(med_name)
				cur.execute("SELECT name, address from buyer_register where buyer_id=%s", (ids[i]['buyer_id']))
				buyer_data = cur.fetchone()
				templist.append(buyer_data)
				finallist.append(templist)
			return render_template("manage_orders.html",ids=med_name,data=finallist)
		return redirect(url_for('seller_login'))

if __name__=='__main__':
	app.run(debug=True)