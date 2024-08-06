from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    serialize_rules = ('-password',)  # Exclude password from serialization

class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    employees = db.relationship('Employee', backref='department', lazy=True)

class Employee(db.Model, SerializerMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    job_title = db.Column(db.String(80), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    date_hired = db.Column(db.DateTime, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    leave_records = db.Column(db.String(200), nullable=True)

    leave_allocations = db.relationship('LeaveAllocation', backref='employee', lazy=True)
    leave_requests = db.relationship('LeaveRequest', backref='employee', lazy=True)

class LeaveAllocation(db.Model, SerializerMixin):
    __tablename__ = 'leave_allocations'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_days_allocated = db.Column(db.Integer, nullable=False)
    days_used = db.Column(db.Integer, default=0)
    days_remaining = db.Column(db.Integer, nullable=False)

class LeaveRequest(db.Model, SerializerMixin):
    __tablename__ = 'leave_requests'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    approver_name = db.Column(db.String(80), nullable=True)
    status = db.Column(db.String(20), default='Pending')

