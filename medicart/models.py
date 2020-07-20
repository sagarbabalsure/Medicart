from medicart import db

class BuyerRegister(db.Model):
	Buyer_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	name = db.Column(db.String(50),nullable=False)
	username = db.Column(db.String(50),unique=True,nullable=False)
	email = db.Column(db.String(50),unique=True,nullable=False)
	password = db.Column(db.String(256),unique=True,nullable=False)
	mobile_no = db.Column(db.String(50),unique=True)
	address = db.Column(db.String(50))
	mode = db.Column(db.String(50),default='Buyer')
	about_me = db.Column(db.String(50))

	def __repr__(self):
		return f"BuyerRegister('{self.name}','{self.username}','{self.email}','{self.password}','{self.mobile_no}','{self.address}','{self.mode}','{self.about_me}')"

class SellerRegister(db.Model):
	Seller_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	name = db.Column(db.String(50),nullable=False)
	username = db.Column(db.String(50),unique=True,nullable=False)
	email = db.Column(db.String(50),unique=True,nullable=False)
	password = db.Column(db.String(256),unique=True,nullable=False)
	mobile_no = db.Column(db.String(50),unique=True)
	company_name = db.Column(db.String(50))
	mode = db.Column(db.String(50),default='Seller')
	about_me = db.Column(db.String(50))
	items = db.relationship('Items', backref='seller', lazy=True)

	def __repr__(self):
		return f"SellerRegister('{self.name}','{self.username}','{self.email}','{self.password}','{self.mobile_no}','{self.company_name}','{self.mode}','{self.about_me}')"


class Items(db.Model):
	product_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	medicine_name = db.Column(db.String(100),nullable=False)
	manufacturer = db.Column(db.String(100),nullable=False)
	price = db.Column(db.Float,nullable=False)
	stock = db.Column(db.Integer,nullable=False)
	description = db.Column(db.String(200))
	composition = db.Column(db.String(200))
	precaution = db.Column(db.String(200))
	Seller_id = db.Column(db.Integer,db.ForeignKey('seller_register.Seller_id'))

	def __repr__(self):
		return f"Items('{self.medicine_name}','{self.manufacturer}','{self.price}','{self.stock}','{self.description}','{self.composition}','{self.precaution}','{self.Seller_id}')"

class Cart(db.Model):
	cart_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	product_id = db.Column(db.Integer)
	buyer_id = db.Column(db.Integer)

	def __repr__(self):
		return f"Cart('{self.product_id}','{self.buyer_id}')"

class ConfirmedOrder(db.Model):
	order_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	buyer_id = db.Column(db.Integer,nullable=False)
	product_id = db.Column(db.Integer)
	Quantity = db.Column(db.Integer,default=1)
	seller_id = db.Column(db.Integer,nullable=False)
	
	def __repr__(self):
		return f"ConfirmedOrder('{self.buyer_id}','{self.product_id}','{self.Quantity}','{self.seller_id}')"