from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField, DateField, DecimalField
from wtforms.validators import DataRequired, Optional
from models import Vehicle, Section, Employee, EmployeeVehicleAction, ExternalCompany, \
    Preparation, ExternalService, Transaction, CarMake, CarModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/car_company'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)


class VehiclePurchaseForm(FlaskForm):
    VIN = StringField('VIN', validators=[DataRequired()])
    Registration_Number = StringField('Registration Number', validators=[DataRequired()])
    Make = SelectField('Make', choices=[], validators=[DataRequired()])
    Model = SelectField('Model', choices=[], validators=[DataRequired()])
    First_Registration_Date = StringField('First Registration Date', validators=[DataRequired()])
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
    Sale_Price = DecimalField('Price ($)', validators=[DataRequired()])
    Transaction_Date = StringField('Transaction Date', validators=[DataRequired()])
    Price = DecimalField('Price ($)', validators=[DataRequired()])
    Notes = StringField('Notes', validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(VehiclePurchaseForm, self).__init__(*args, **kwargs)
        self.Make.choices = [(make.id, make.name) for make in CarMake.query.all()]
        self.Model.choices = [(model.id, model.name) for model in CarModel.query.all()]

    Submit = SubmitField('Submit')


@app.route('/buyer', methods=['GET', 'POST'])
def buyer_interface():
    form = VehiclePurchaseForm()

    form.Make.choices = [(make.id, make.name) for make in CarMake.query.all()]
    form.Model.choices = [(model.id, model.name) for model in CarModel.query.all()]

    if form.validate_on_submit():
        first_registration_date = datetime.strptime(form.First_Registration_Date.data, '%d.%m.%Y').date()
        transaction_date = datetime.strptime(form.Transaction_Date.data, '%d.%m.%Y').date()

        new_vehicle = Vehicle(
            VIN=form.VIN.data,
            Registration_Number=form.Registration_Number.data,
            Make=form.Make.data,
            Model=form.Model.data,
            First_Registration_Date=first_registration_date,
            Fuel_Type=form.Fuel_Type.data,
            Engine_Capacity=form.Engine_Capacity.data,
            Engine_Power=form.Engine_Power.data,
            Gearbox_Type=form.Gearbox_Type.data,
            Mileage=form.Mileage.data,
            Number_Of_Doors=form.Number_Of_Doors.data,
            Drive_Type=form.Drive_Type.data,
            Prod_Year=form.Prod_Year.data,
            Sale_Price=form.Sale_Price.data,
        )

        db.session.add(new_vehicle)
        db.session.commit()

        new_transaction = Transaction(
            Vehicle_ID=new_vehicle.Vehicle_ID,
            Transaction_Date=transaction_date,
            Price=form.Price.data,
            Notes=form.Notes.data
        )

        db.session.add(new_transaction)
        db.session.commit()

        flash('Vehicle and Purchase details saved successfully!', 'success')
        return redirect(url_for('buyer_interface'))

    return render_template('buyer_form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
