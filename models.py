from sqlalchemy import DECIMAL
from database import db


class Vehicle(db.Model):
    __tablename__ = 'Vehicles'

    Vehicle_ID = db.Column(db.Integer, primary_key=True)
    VIN = db.Column(db.String(17), unique=True, nullable=False)
    Registration_Number = db.Column(db.String(10))
    make_id = db.Column(db.Integer, db.ForeignKey('CarMake.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('CarModel.id'))
    First_Registration_Date = db.Column(db.Date)
    Fuel_Type = db.Column(db.String(10))
    Engine_Capacity = db.Column(db.Integer)
    Engine_Power = db.Column(db.Integer)
    Gearbox_Type = db.Column(db.String(10))
    Mileage = db.Column(db.Integer)
    Number_Of_Doors = db.Column(db.Integer)
    Drive_Type = db.Column(db.String(10))
    Prod_Year = db.Column(db.Integer)
    Sale_Price = db.Column(DECIMAL(precision=10, scale=2))
    optical_preparation = db.Column(db.DECIMAL(10, 2))
    mechanical_preparation = db.Column(db.DECIMAL(10, 2))
    other_preparation_costs = db.Column(db.DECIMAL(10, 2))
    margin = db.Column(db.DECIMAL(10, 2))

    vehicle_actions = db.relationship('EmployeeVehicleAction', back_populates='vehicle')
    preparations = db.relationship('Preparation', back_populates='vehicle')
    external_services = db.relationship('ExternalService', back_populates='vehicle')
    transactions = db.relationship('Transaction', back_populates='vehicle')

    make = db.relationship('CarMake', backref='related_vehicles')
    model = db.relationship('CarModel', backref='model_vehicles')


class Section(db.Model):
    __tablename__ = 'Sections'

    Section_ID = db.Column(db.Integer, primary_key=True)
    Section_Name = db.Column(db.String(100), nullable=False)

    employees = db.relationship('Employee', back_populates='section')


class Employee(db.Model):
    __tablename__ = 'Employees'

    Employee_ID = db.Column(db.Integer, primary_key=True)
    Full_Name = db.Column(db.String(50), nullable=False)
    Role = db.Column(db.String(20))
    Section_ID = db.Column(db.Integer, db.ForeignKey('Sections.Section_ID'))

    section = db.relationship('Section', back_populates='employees')
    employee_actions = db.relationship('EmployeeVehicleAction', back_populates='employee')
    transactions = db.relationship('Transaction', back_populates='employee')


class EmployeeVehicleAction(db.Model):
    __tablename__ = 'Employee_Vehicle_Action'

    Employee_ID = db.Column(db.Integer, db.ForeignKey('Employees.Employee_ID'), primary_key=True)
    Vehicle_ID = db.Column(db.Integer, db.ForeignKey('Vehicles.Vehicle_ID'), primary_key=True)
    Action = db.Column(db.String(100), primary_key=True)
    Start_Date = db.Column(db.Date)
    End_Date = db.Column(db.Date)

    vehicle = db.relationship('Vehicle', back_populates='vehicle_actions')
    employee = db.relationship('Employee', back_populates='employee_actions')


class ExternalCompany(db.Model):
    __tablename__ = "External_Companies"

    Company_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)

    external_services = db.relationship('ExternalService', back_populates='company')


class Preparation(db.Model):
    __tablename__ = 'Preparation'

    Preparation_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vehicle_ID = db.Column(db.Integer, db.ForeignKey('Vehicles.Vehicle_ID'))
    Preparation_Costs = db.Column(DECIMAL(precision=10, scale=2))
    Start_Date = db.Column(db.Date)
    End_Date = db.Column(db.Date)

    vehicle = db.relationship('Vehicle', back_populates='preparations')


class ExternalService(db.Model):
    __tablename__ = 'External_Services'

    Service_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vehicle_ID = db.Column(db.Integer, db.ForeignKey('Vehicles.Vehicle_ID'))
    Company_ID = db.Column(db.Integer, db.ForeignKey('External_Companies.Company_ID'))
    Service_Description = db.Column(db.String(255))
    Service_Date = db.Column(db.DateTime)

    vehicle = db.relationship('Vehicle', back_populates='external_services')
    company = db.relationship('ExternalCompany', back_populates='external_services')


class Transaction(db.Model):
    __tablename__ = 'Transactions'

    Transaction_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vehicle_ID = db.Column(db.Integer, db.ForeignKey('Vehicles.Vehicle_ID'))
    Employee_ID = db.Column(db.Integer, db.ForeignKey('Employees.Employee_ID'))
    Transaction_Type = db.Column(db.Enum('Purchase', 'Sale'))
    Transaction_Date = db.Column(db.Date)
    Purchase_Price = db.Column(DECIMAL(precision=10, scale=2))
    Notes = db.Column(db.String(255))

    vehicle = db.relationship('Vehicle', back_populates='transactions')
    employee = db.relationship('Employee', back_populates='transactions')


class CarMake(db.Model):
    __tablename__ = 'CarMake'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    vehicles = db.relationship('Vehicle', back_populates='make')

    models = db.relationship('CarModel', back_populates='make')


class CarModel(db.Model):
    __tablename__ = 'CarModel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    make_id = db.Column(db.Integer, db.ForeignKey('CarMake.id'), nullable=False)

    make = db.relationship('CarMake', back_populates='models')

    vehicles = db.relationship('Vehicle', back_populates='model')


class Purchase(db.Model):
    __tablename__ = 'Purchase'

    Purchase_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vehicle_ID = db.Column(db.Integer, db.ForeignKey('Vehicles.Vehicle_ID'))
    Purchase_Price = db.Column(db.DECIMAL(10, 2))
    Purchase_Date = db.Column(db.Date)
    tax = db.Column(db.DECIMAL(5, 3))
    excise_tax = db.Column(db.DECIMAL(10, 2))
    sales_price = db.Column(db.DECIMAL(10, 2))

    vehicle = db.relationship('Vehicle', backref='purchases')