from datetime import date

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField, DateField, DecimalField
from wtforms.validators import DataRequired, Optional
from makes import MAKES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://[root]:[password]@localhost/car_company'
db = SQLAlchemy(app)

class VehiclePurchaseForm(FlaskForm):
    VIN = StringField('VIN', validators=[DataRequired()])
    Registration_Number = StringField('Registration Number', validators=[DataRequired()])
    Make = SelectField('Make', choices=MAKES, validators=[DataRequired()])
    Model = StringField('Model', validators=[DataRequired()])
    First_Registration_Date = DateField('First Registration Date', format = '%d-%m-%Y', validators=[DataRequired()])
    Fuel_Type = SelectField('Fuel Type', choices=[
        ('Gas', 'Gas'),
        ('Diesel', 'Diesel'),
        ('Hybrid', 'Hybrid'),
        ('Electric', 'Electric')
    ])
    Engine_Capacity = IntegerField('Engine Capacity (cc)', validators=[DataRequired()])
    Engine_Power = IntegerField('Engine Power (HP)', validators=[DataRequired()])
    Gearbox_Type = SelectField('Gearbox Type', choices=[
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic')
    ])
    Mileage = IntegerField('Mileage (km)', validators=[DataRequired()])
    Number_Of_Doors = SelectField('Number of Doors', choices=[
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ])
    Drive_Type = SelectField('Drive Type', choices=[
        ('FWD', 'Front-Wheel Drive'),
        ('RWD', 'Rear-Wheel Drive'),
        ('AWD', 'All-Wheel Drive')
    ])
    Prod_Year = IntegerField('Production Year', validators=[DataRequired()])
    Sales_Price = DecimalField('Price ($)', validators=[DataRequired()])
    Transaction_Date = DateField('Transaction Date', format='%d-%m-%Y', validators=[DataRequired()], default=date.today())
    Price = DecimalField('Price ($)', validators=[DataRequired()])
    Notes = StringField('Notes', validators=[Optional()])

    Submit = SubmitField('Submit')
