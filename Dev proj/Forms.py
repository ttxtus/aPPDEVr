from wtforms import Form, StringField, TextAreaField, validators, ValidationError, PasswordField
from wtforms.fields import EmailField

def validate_name(form, field):
    if field.data.isalpha() ==0:
        raise ValidationError('Name must only contain alphabets')
def validate_mobile(form, field):
    if field.data.isdigit() ==0:
        raise ValidationError('Mobile number must only contain numbers')

class CreateLoginForm(Form):
    mobile_no = TextAreaField('Mobile Number', [validators.length(max=8), validators.DataRequired()])
    password = TextAreaField('Password', [validators.length(min=8, max=20), validators.DataRequired()])

class CreateSignUpForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150) , validators.DataRequired(),validate_name])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(),validate_name])
    mobile_no = StringField('Mobile Number', [validators.length(min=8,max=8), validators.DataRequired(),validate_mobile])
    password = PasswordField('Password', [validators.length(min=8, max=20), validators.DataRequired()])
    cpassword = PasswordField('Confirmed Password',[validators.length(min=8, max=20), validators.DataRequired(),validators.equal_to('password',message='Passwords must match')])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])


