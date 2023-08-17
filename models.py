class Vehicle(db.Model):
    __tablename__ = 'Vehicles'

    Vehicle_ID = db.Column(db.Integer, primary_key=True)
    VIN = db.Column(db.String(17), unique=True, nullable=False)
    Registration_Number = db.Column(db.String(10))
    Make = db.Column(db.String(20))
    Model = db.Column(db.String(20))
    First_Registration_Date = db.Column(db.Date)
    Fuel_Type = db.Column(db.String(5))
    Engine_Capacity = db.Column(db.Integer)
    Engine_Power = db.Column(db.Integer(4))
    Gearbox_Type = db.Column(db.String(10))
    Mileage = db.Column(db.Integer)
    Number_Of_Doors = db.Column(db.Integer)
    Drive_Type = db.Column(db.String(10))
    Prod_Year = db.Column(db.Integer)

    def __init__(self, Vehicle_ID, VIN, Registration_Number, Make, Model, First_Registration_Date, Fuel_Type,
                 Engine_Capacity, Engine_Power, Gearbox_Type, Mileage,
                 Number_Of_Doors, Drive_Type, Prod_Year):
        self.Vehicle_ID = Vehicle_ID
        self.VIN = VIN
        self.Registration_Number = Registration_Number
        self.Make = Make
        self.Model = Model
        self.First_Registration_Date = First_Registration_Date
        self.Fuel_Type = Fuel_Type
        self.Engine_Capacity = Engine_Capacity
        self.Engine_Power = Engine_Power
        self.Gearbox_Type = Gearbox_Type
        self.Mileage = Mileage
        self.Number_Of_Doors = Number_Of_Doors
        self.Drive_Type = Drive_Type
        self.Prod_Year = Prod_Year


class Section(db.Model):
    __tablename__ = 'Sections'

    Section_ID = db.Column(db.Integer, primary_key=True)
    Section_Name = db.Column(db.String(100), nullable=False)

    def __init__(self, Section_ID, Section_Name):
        self.Section_ID = Section_ID
        self.Section_Name = Section_Name


class Employee(db.Model):
    __tablename__ = 'Employees'

    Employee_ID = db.Column(db.Integer, primary_key=True)
    Full_Name = db.Column(db.String(50), nullable=False)
    Role = db.Column(db.String(20))
    Section_ID = db.Column(db.Integer, db.ForeignKey('Sections.Section_ID'))

    section = db.relationship("Section", backref=db.backref("employee", lazy="dynamic"))

    def __init__(self, Employee_ID, Full_Name, Surname, Role, Section_ID):
        self.Employee_ID = Employee_ID
        self.Full_Name = Full_Name
        self.Role = Role
        self.Section_ID = Section_ID


class EmployeeVehicleAction(db.Model):
    __tablename__ = 'Employee_Vehicle_Action'

    Employee_ID = db.Column(db.Integer, db.ForeignKey('Employees.Employee_ID'), primary_key=True)
    Vehicle_ID = db.Column(db.Integer, db.ForeignKey('Vehicles.Vehicle_ID'), primary_key=True)
    Action = db.Column(db.String(100), primary_key=True)
    Start_Date = db.Column(db.Date)
    End_Date = db.Column(db.Date)

    employee = db.relationship("Employee", backref=db.backref("employee_vehicle_action", lazy="dynamic"))
    vehicle = db.relationship("Vehicle", backref=db.backref("employee_vehicle_action", lazy="dynamic"))

    def __init__(self, Employee_ID, Vehicle_ID, Action, Start_Date, End_Date):
        self.Employee_ID = Employee_ID
        self.Vehicle_ID = Vehicle_ID
        self.Action = Action
        self.Start_Date = Start_Date
        self.End_Date = End_Date

class ExternalCompany(db.Model):
    __tablename__ = "External_Companies"

    Company_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)

    def __init__(self, Company_ID, Name):
        self.Company_ID = Company_ID
        self.Name = Name

