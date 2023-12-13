from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField, DateField, \
    DecimalField, validators, FloatField, BooleanField
from wtforms.validators import DataRequired, Optional
from models import Vehicle, Section, Employee, EmployeeVehicleAction, ExternalCompany, \
    Preparation, ExternalService, Transaction, CarMake, CarModel, Purchase

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
        ('Electric', 'Electric'),
        ('Plug-in Hybrid', 'Plug-in Hybrid')
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
    Purchase_Price = DecimalField('Purchase Price ($)', validators=[DataRequired()])
    Notes = StringField('Notes', validators=[Optional()])
    optical_preparation = FloatField('Optical Preparation', validators=[DataRequired()])
    mechanical_preparation = FloatField('Mechanical Preparation', validators=[DataRequired()])
    other_preparation_costs = FloatField('Other Preparation Costs', validators=[DataRequired()])
    tax = SelectField('Tax', choices=[('0', '0%'), ('0.02', '2%')], validators=[DataRequired()])
    excise_tax_checkbox = BooleanField('Excise Tax?')

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
            Sale_Price=form.sales_price.data,
            optical_preparation=form.optical_preparation.data,
            mechanical_preparation=form.mechanical_preparation.data,
            other_preparation_costs=form.other_preparation_costs.data,
        )

        db.session.add(new_vehicle)
        db.session.commit()

        new_transaction = Transaction(
            Vehicle_ID=new_vehicle.Vehicle_ID,
            Transaction_Date=transaction_date,
            Purchase_Price=form.Purchase_Price.data,
            Notes=form.Notes.data
        )

        db.session.add(new_transaction)
        db.session.commit()

        new_purchase = Purchase(
            tax=form.tax.data,
            excise_tax=form.excise_tax.data,
            sales_price=form.sales_price.data,
            margin=form.margin.data,
        )

        db.session.add(new_purchase)
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
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if request.method == 'POST':

        vehicle.VIN = request.form['vin']
        vehicle.Registration_Number = request.form['registration_number']
        vehicle.Make = request.form['make']
        vehicle.Model = request.form['model']
        vehicle.First_Registration_Date = request.form['first_registration_date']
        vehicle.Fuel_Type = request.form['fuel_type']
        vehicle.Engine_Capacity = request.form['engine_capacity']
        vehicle.Engine_Power = request.form['engine_power']
        vehicle.Gearbox_Type = request.form['gearbox_type']
        vehicle.Mileage = request.form['mileage']
        #vehicle.Equipment_Version = request.form['equipment_version']
        vehicle.Number_Of_Doors = request.form['door_count']
        vehicle.Drive_Type = request.form['drive_type']

        try:
            db.session.commit()
            flash('Vehicle details updated successfully!', 'success')
            return redirect(url_for('manage_vehicles'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')

    return render_template('edit_vehicle.html', vehicle=vehicle)


@app.route('/')
def home():
    return render_template('home.html')




if __name__ == '__main__':
    app.run(debug=True)
