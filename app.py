from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField, DateField, \
    DecimalField, validators
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
    VIN = StringField('VIN', [
        validators.Length(max=17, message="VIN must be 17 characters"),
        validators.Regexp(r'^[A-Z0-9]{17}$', message="VIN must only contain uppercase letters and numbers")
    ])
    Registration_Number = StringField('Registration Number', validators=[DataRequired()])
    Make = SelectField('Make', choices=[], validators=[DataRequired()])
    Model = SelectField('Model', choices=[], validators=[DataRequired()])
    First_Registration_Date = DateField('First Registration Date', format='%Y-%m-%d', validators=[DataRequired()])
    Fuel_Type = SelectField('Fuel Type', choices=[
        ('Gas', 'Gas'),
        ('Petrol', 'Petrol'),
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
    Transaction_Date = DateField('Transaction Date', format='%Y-%m-%d', validators=[DataRequired()])
    Price = DecimalField('Price ($)', validators=[DataRequired()])
    Notes = StringField('Notes', validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(VehiclePurchaseForm, self).__init__(*args, **kwargs)
        self.Make.choices = [(make.id, make.name) for make in CarMake.query.all()]
        self.Model.choices = [(model.id, model.name) for model in CarModel.query.all()]

    Submit = SubmitField('Submit')


@app.route('/get-models/<make_id>', methods=['GET'])
def get_models(make_id):
    models = CarModel.query.filter_by(make_id=make_id).all()
    model_list = [{"id": m.id, "name": m.name} for m in models]
    return jsonify(model_list)

@app.route('/buyer', methods=['GET', 'POST'])
def buyer_interface():
    form = VehiclePurchaseForm()

    form.Make.choices = [(make.id, make.name) for make in CarMake.query.all()]
    form.Model.choices = [(model.id, model.name) for model in CarModel.query.all()]

    if form.validate_on_submit():
        first_registration_date = form.First_Registration_Date.data
        transaction_date = form.Transaction_Date.data

        new_vehicle = Vehicle(
            VIN=form.VIN.data,
            Registration_Number=form.Registration_Number.data,
            make_id=form.Make.data,
            model_id=form.Model.data,
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

@app.route('/manage-vehicles', methods=['GET'])
def manage_vehicles():
    related_vehicles = Vehicle.query.all()
    return render_template('manage_vehicles.html', related_vehicles=related_vehicles)

@app.route('/edit-vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if request.method == 'POST':

        update_mileage = request.form['mileage']

        vehicle.Mileage = update_mileage

        db.session.commit()
        return redirect(url_for('manage_vehicles'))
    return render_template('edit_vehicle.html', vehicle=vehicle)



if __name__ == '__main__':
    app.run(debug=True)
