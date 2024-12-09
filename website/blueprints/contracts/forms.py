from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ContractForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    server_id = SelectField('Server', coerce=int, validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    type = SelectField(
        'Type',
        choices=[('hourly', 'Hourly'), ('lump_sum', 'Lump Sum')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Create Contract')
