from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,PasswordField, IntegerField, FloatField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class SearchForm(FlaskForm):
    winename = StringField('Wine Name')
    wineyear = SelectField('Year', choices=[],default='')
    winevar = SelectField('Variety',choices=[],default='')
    submit = SubmitField('Find')

class LoginForm(FlaskForm):
    username = StringField('User Name', )
    password = PasswordField('Password')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_ver = PasswordField('Password Verify', validators=[DataRequired()])
    email = StringField('E-mail Address', validators=[DataRequired()])
    submit = SubmitField('Enter')
	
	
class ProfileForm(FlaskForm):
    username = StringField('User Name')
	
class NewReviewForm(FlaskForm):
    winery = StringField('Winery', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    designation = StringField('Designation', default='')
    variety = StringField('Variety', default = '')
    points = IntegerField('Rating Points', validators=[DataRequired()])
    description = StringField('Write your review:', widget=TextArea(), default = '')
    submit = SubmitField('Add')
	
class NewLogForm(FlaskForm):
    username = StringField('User Name')
    winename = StringField('Wine Name')
    winevar = StringField('Variety')
    wineyear = StringField('Year')
    rating = IntegerField('Rating')
    price = FloatField('Price')
    purchasepoint = StringField('Purchased from')
    logcontent = StringField('Log')
    submit = SubmitField('Enter')
	
