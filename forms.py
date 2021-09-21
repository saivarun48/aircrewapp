from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Email, Length


class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=-1, max=80, message='Field should not have more than 80 characters.')])
    surname = StringField('Surname', validators=[Length(min=-1, max=100, message='Field should not have more than 100 characters.')])
    email = StringField('E-Mail', validators=[Email(), Length(min=-1, max=200, message='Field should not have more than 200 characters.')])
    phone = StringField('Phone', validators=[Length(min=-1, max=20, message='Field should not have more than 20 characters.')])
    role = SelectField('Role', choices=[('Captain', 'Captain'), ('First officer', 'First officer'), ('Flight attendant', 'Flight attendant')])
    attachment = FileField('Passport')
    
