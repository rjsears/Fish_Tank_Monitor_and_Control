from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, StringField, TextAreaField
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms.validators import (DataRequired,Email,EqualTo,Length,URL)

class ParameterForm(FlaskForm):
    kh = FloatField('KH Reading', [InputRequired()])
    gh = FloatField('GH Reading', [InputRequired()])
    po4 = FloatField('Phosphate Reading', [InputRequired()])
    submit = SubmitField('Submit')


