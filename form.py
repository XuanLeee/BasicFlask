## python file interact with user input
from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField## submitbutton
from wtforms.validators import DataRequired, Email, Length ##check if the user input data is empty/email address
##is good and password is secreted
##signup class ues for new users
class SignUp(Form):##inheriting from base form class
    f_name = StringField('First name',validators=[(DataRequired("first name required"))])
    l_name = StringField('Last name',validators=[(DataRequired("last name required"))])
    email = StringField('Email',validators=[(DataRequired("Invalid email address")),Email("@Address Need")])
    password = PasswordField('Password',validators=[(DataRequired("Invalid password")),Length(min=6,message="password must be 6 char or more")])
    submit = SubmitField('Sign up')

##login class is for return users
class LogIn(Form): ## inheriting from base form class
    email = StringField('Email',validators=[DataRequired("email address please"),Email("@Address Need")])
    password = PasswordField('Password',validators=[DataRequired("please enter password")])
    submit = SubmitField("Sign in")

class Address(Form):
    address = StringField('Address',validators=[DataRequired("please enter address")])
    submit = SubmitField("Search address")
