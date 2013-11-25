from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SelectField
from wtforms.validators import Required
from models import User_location, Item_location

try:
    user_locations = map(lambda x: (x.id, x), User_location.query.all())
except:
    user_locations = [(1, "")]

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    location  = SelectField('location', choices=user_locations, coerce=int, validators = [Required()])
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)



try:
    item_locations = map(lambda x: (x.id, x), Item_location.query.all())
except:
    item_locations = [(1, "")]

class ItemForm(Form):
    name = TextField('name', validators = [Required()])
    price = TextField('email', validators = [Required()])
    location  = SelectField('location', choices=item_locations, coerce=int, validators = [Required()])
    description = TextField('description', validators = [Required()])

