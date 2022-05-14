from flask_wtf import FlaskForm
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from jinja2.utils import markupsafe
from ...models import User


class LoginForm(FlaskForm):
    #field name = DatatypeField('LABEL', validators=[LIST OF validators])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name =  StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
            validators=[DataRequired(), EqualTo('password', message='Password Must Match')])
    submit = SubmitField('Register')

    r1= 1
    r2= 2
    r3= 3

    c1 = markupsafe.Markup(f'<img src= "https://res.cloudinary.com/dipcloqy3/image/upload/v1651867932/character3_eqvcd2.png" height= "150px">')
    c2 = markupsafe.Markup(f'<img src= "https://res.cloudinary.com/dipcloqy3/image/upload/v1651869917/character4_hcdgai.png" height= "150px">')
    c3 = markupsafe.Markup(f'<img src= "https://res.cloudinary.com/dipcloqy3/image/upload/v1651867932/character1_rn81i8.webp" height= "150px">')

    icon = RadioField('Choose Trainer', validators =[DataRequired()],
        choices= [(r1,c1),(r2,c2),(r3,c3)]
    )

    ## MUST BE LIKE THIS!!  VALIDATE_FIELDNAME
    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
                        # SELECT * FROM user WHERE email = ???
        if same_email_user:
            raise ValidationError('Email is Already in Use')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name =  StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
            validators=[DataRequired(), EqualTo('password', message='Password Must Match')])
    submit = SubmitField('Change Profile')

    r1= 1
    r2= 2
    r3= 3

    c1 = markupsafe.Markup(f'<img src= "https://res.cloudinary.com/dipcloqy3/image/upload/v1651867932/character3_eqvcd2.png" height= "150px">')
    c2 = markupsafe.Markup(f'<img src= "https://res.cloudinary.com/dipcloqy3/image/upload/v1651869917/character4_hcdgai.png" height= "150px">')
    c3 = markupsafe.Markup(f'<img src= "https://res.cloudinary.com/dipcloqy3/image/upload/v1651867932/character1_rn81i8.webp" height= "150px">')

    icon = RadioField('Choose Trainer', validators =[Optional()],
        choices= [(r1,c1),(r2,c2),(r3,c3)]
    )