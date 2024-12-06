from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
