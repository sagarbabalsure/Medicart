from flask import *
from medicart.form import *
import hashlib
from medicart.models import *
from medicart import app
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
		data = BuyerRegister.query.filter_by(username=username,password=password).first()
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
		data = BuyerRegister.query.filter_by(username=username).first()
		if data:
			flash("Username is already taken")
		else:
			query = BuyerRegister(name=name,username=username,email=email,password=password)
			db.session.add(query)
			db.session.commit()
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
		data = SellerRegister.query.filter_by(username=username,password=password).first()
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
		data = SellerRegister.query.filter_by(username=username).first()
		if data:
			flash("Username is already taken")
		else:
			query = SellerRegister(name=name,username=username,email=email,password=password)
			db.session.add(query)
			db.session.commit()
			flash("Congragulation you have registered successfully")
			return redirect(url_for('seller_login'))

	return render_template("register.html",form=form,title='Seller')

@app.route('/profile')
def profile():
	if 'username' in session:
		username = session['username']
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			data = BuyerRegister.query.filter_by(username=username).first()
			print(data.username)
			return render_template("profile.html",data=data,mode='Buyer')
		else:
			data = SellerRegister.query.filter_by(username=username).first()
			return render_template("profile.html",data=data)
	else:
		return render_template('index.html')

@app.route('/homepage')
def homepage():
	if 'username' in session:
		username = session['username']
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			data = Items.query.all()
			return render_template('homepage_data.html',homepage_data=data)
		else:
			return redirect(url_for('add_medicine'))
	else:
		return render_template('index.html')


@app.route('/logout')
def logout():
	if 'username' in session:
		username = session['username']
		print(username)
		mode = BuyerRegister.query.filter_by(username=username).first()
		print(mode)
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
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			form = EditBuyerProfile()
			data = BuyerRegister.query.filter_by(username=username).first()
			if request.method == 'POST' and form.validate_on_submit():
				data = BuyerRegister.query.filter_by(username=username).first()
				print(data)
				data.email=form.email.data
				data.mobile_no = form.mobile_no.data
				data.address = form.address.data
				data.about_me = form.about_me.data
				db.session.commit()
				flash("Your profile is updated")
				return redirect(url_for('profile'))
			return render_template("edit_profile.html",form=form,data=data,mode="Buyer")
		else:
			form = EditSellerProfile()
			data = SellerRegister.query.filter_by(username=username).first()
			print("first: ",data)
			if request.method == 'POST' and form.validate_on_submit():
				data = SellerRegister.query.filter_by(username=username).first()
				print("second: ",data)
				data.email=form.email.data
				data.mobile_no = form.mobile_no.data
				data.company = form.company.data
				data.about_me = form.about_me.data
				db.session.commit()
				flash("Your profile is updated")
				return redirect(url_for('profile'))
			return render_template("edit_profile.html",form=form,data=data)
	return render_template('index.html')





@app.route('/view-orders')
def view_orders():
	if 'username' in session:
		username = session['username']
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			buyer_id = mode.Buyer_id
			P_ids = ConfirmedOrder.query.filter_by(buyer_id=buyer_id).all()
			list1 = []
			for P_id in P_ids:
				data = Items.query.filter_by(product_id=P_id.product_id).first()
				list1.append(data)	
			return render_template('view_orders.html',data=list1)
		return redirect(url_for('buyer_login'))

@app.route('/search-by-name',methods=['GET','POST'])
def search():
	if 'username' in session:
		username = session['username']
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			if request.method == 'POST':
				search_key = request.form['search']
				data = Items.query.filter_by(medicine_name=search_key).all()
				return render_template('homepage_data.html',searched_data=data)
			return render_template('buyer_homepage.html')
		return redirect(url_for('buyer_login'))



@app.route('/add_medicine',methods=['GET','POST'])
def add_medicine():
	form = AddMedicine()
	if 'username' in session:
		username = session['username']
		mode = SellerRegister.query.filter_by(username=username).first()
		if mode:
			Seller_id = mode.Seller_id
			if request.method == "POST" and form.validate_on_submit():
				medicine_name = form.medicine_name.data
				manufacturer = form.manufacturer.data
				price = form.price.data
				stock = form.stock.data
				composition = form.composition.data
				precaution = form.precaution.data
				description = form.medicine_description.data
				query = Items(medicine_name=medicine_name,manufacturer=manufacturer,price=price,stock=stock,description=description,composition=composition,precaution=precaution,Seller_id=Seller_id)
				db.session.add(query)
				db.session.commit()
				flash("Medicine information added")
				return redirect(url_for('homepage'))
			return render_template('add_medicine.html',form=form)
		return redirect(url_for('seller_login'))


@app.route('/seller-added-products')
def added_products():
	if 'username' in session:
		username = session['username']
		mode = SellerRegister.query.filter_by(username=username).first()
		if mode:
			data = Items.query.filter_by(Seller_id=mode.Seller_id).all()
			print(type(data))
			for d in data:
				print(type(d))
			return render_template('seller_added_products.html',data=data)
		return redirect(url_for('seller_login'))


@app.route('/update-medicine-data/<int:product_id>',methods=['GET','POST'])
def update_medicine(product_id):
	if 'username' in session:
		username = session['username']
		mode = SellerRegister.query.filter_by(username=username).first()
		if mode:
			form=UpdateMedicineData()
			data = Items.query.filter_by(product_id=product_id).first()
			if request.method == 'POST' and form.validate_on_submit():
				data.medicine_name = form.medicine_name.data
				data.price = form.price.data
				data.stock = form.stock.data
				db.session.commit()
				return redirect(url_for('added_products'))
			return render_template('update_medicine_data.html',form=form,data=data)
		return redirect(url_for('seller_login'))

@app.route('/product_page/<int:product_id>')
def product_page(product_id):
	if 'username' in session:
		username = session['username']
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			data = Items.query.filter_by(product_id=product_id).first()
			print(data)
			return render_template('product_page.html',data=data)
	return redirect(url_for('buyer_login'))


@app.route('/AddToCart<int:product_id>')
def add_to_cart(product_id):
	if 'username' in session:
		username = session['username']
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			B_id = BuyerRegister.query.filter_by(username=username).first()
			query = Cart(product_id=product_id,buyer_id=B_id.Buyer_id)
			db.session.add(query)
			db.session.commit()
			flash("product added to cart")
			return redirect(url_for('product_page',product_id=product_id))
		return redirect(url_for('buyer_login'))

@app.route('/show_cart')
def show_cart():
	if 'username' in session:
		username = session['username']
		B_id = BuyerRegister.query.filter_by(username=username).first()
		P_ids = Cart.query.filter_by(buyer_id=B_id.Buyer_id).all()
		print(P_ids)
		list1 = []
		for P_id in P_ids:
			data = Items.query.filter_by(product_id=P_id.product_id).first()
			print(P_id)
			list1.append(data)	
		return render_template('show_cart.html',data=list1,product_ids=P_ids)
	
@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
	if 'username' in session:
		username = session['username']
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			query = Cart.query.filter_by(product_id=product_id).first()
			db.session.delete(query)
			db.session.commit()
			return redirect(url_for('homepage'))
		return redirect(url_for('buyer_login'))


@app.route('/buy/<int:product_id>')
def buy(product_id):
	if 'username' in session:
		username = session['username']
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			data = Items.query.filter_by(product_id=product_id).first()
			return render_template('order_page.html',data=data)
		return redirect(url_for('buyer_login'))

@app.route('/confirm-order/<int:product_id>/<int:seller_id>',methods=['GET','POST'])
def confirm_order(product_id,seller_id):
	if 'username' in session:
		username = session['username']
		mode = BuyerRegister.query.filter_by(username=username).first()
		if mode:
			username = session['username']
			if request.method == 'POST':
				quantity = request.form['quantity']
			query = ConfirmedOrder(buyer_id=mode.Buyer_id,product_id=product_id,Quantity=quantity,seller_id=seller_id)
			db.session.add(query)
			db.session.commit()
			Stock = Items.query.filter_by(product_id=product_id).first()
			new_stock = (Stock.stock - int(quantity))
			Stock.stock = new_stock
			db.session.commit() 
			return render_template("last.html")
		return redirect(url_for('buyer_login'))
	return render_template('index.html')

@app.route('/manage-orders')	
def manage_orders():
	if 'username' in session:
		username = session['username']
		mode = SellerRegister.query.filter_by(username=username).first()
		if mode:
			seller_id = mode.Seller_id
			ids = ConfirmedOrder.query.filter_by(seller_id=seller_id).all()
			finallist = list()
			for _id in ids:
				templist = []
				med_name = Items.query.filter_by(product_id=_id.product_id).first()
				templist.append(med_name.medicine_name)
				buyer_data = BuyerRegister.query.filter_by(Buyer_id=_id.buyer_id).first()
				templist.append(buyer_data.name)
				templist.append(buyer_data.address)
				finallist.append(templist)
			print(finallist)
			return render_template("manage_orders.html",data=finallist)
		return redirect(url_for('seller_login'))
		