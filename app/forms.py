from flask_wtf import FlaskForm
from wtforms import (StringField, DateField, TimeField,
                     TextAreaField, BooleanField, SubmitField)
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime


def validate_end_date(form, field):
    if not form.start_date.data or not form.start_time.data or not field.data or not form.end_time.data:
        return  # Skip if any required fields are missing

    start = datetime.combine(form.start_date.data, form.start_time.data)
    end = datetime.combine(field.data, form.end_time.data)
    if form.start_date.data != field.data:
        raise ValidationError("Start and end date must be on the same day")
    # 'raise' ends the function. so at most one error will show (for formatting notes)
    if start >= end:
        raise ValidationError("End date/time must come after start date/time")



class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired(), validate_end_date])
    end_time = TimeField('End Time', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    private = BooleanField('Private')   #data required on booleans forces the checkbox to be checked
    submit = SubmitField('Save')
