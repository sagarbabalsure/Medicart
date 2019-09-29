from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,FloatField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo


class BuyerLoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Sign In')


class SellerLoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Sign In')


class BuyerRegisterForm(FlaskForm):
	name = StringField('Name',validators=[DataRequired()])
	username = StringField('Username',validators=[DataRequired(),Length(max=10)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired(),Length(min=4,max=10)])
	password2 = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')


class SellerRegisterForm(FlaskForm):
	name = StringField('Name',validators=[DataRequired()])
	username = StringField('Username',validators=[DataRequired(),Length(max=10)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired(),Length(min=4,max=10)])
	password2 = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')


class EditBuyerProfile(FlaskForm):
	name = StringField('Name',validators=[DataRequired()])
	username = StringField('Username',validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired(),Email()])
	mobile_no = StringField('mobile no',validators=[DataRequired(),Length(max=10)])
	address = TextAreaField('address',validators=[DataRequired()])
	about_me = StringField("About Me")
	submit = SubmitField('Edit Profile')

class EditSellerProfile(FlaskForm):
	name = StringField('Name',validators=[DataRequired()])
	username = StringField('Username',validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired(),Email()])
	mobile_no = StringField('mobile no',validators=[DataRequired(),Length(max=10)])
	company = StringField('company',validators=[DataRequired()])
	about_me = StringField("About Me")
	submit = SubmitField('Submit')

class AddMedicine(FlaskForm):
	medicine_name = StringField('Medicine Name',validators=[DataRequired()])
	manufacturer = StringField('Manufactured By',validators=[DataRequired()])
	price = FloatField("Price",validators=[DataRequired()])
	stock = IntegerField("stock",validators=[DataRequired()])
	medicine_description = TextAreaField("Description")
	composition = TextAreaField("composition")
	precaution = TextAreaField("precaution")
	submit = SubmitField("Add Medicine")

class UpdateMedicineData(FlaskForm):
	medicine_name = StringField('Medicine Name',validators=[DataRequired()])
	price = FloatField("Price",validators=[DataRequired()])
	stock = IntegerField("stock",validators=[DataRequired()])
	submit = SubmitField("update")