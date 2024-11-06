from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import serial
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Настройка базы данных
engine = create_engine('mysql+pymysql://root:1qaz@WSX12@localhost/db_info_users')
Base = declarative_base()

# Настройка Arduino
arduino = serial.Serial('COM8', 9600)


# Модели таблиц
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255))
    patronymic = Column(String(255))
    position = Column(String(255))
    department = Column(String(255))
    card_id = Column(String(20), unique=True, nullable=False)
    hire_date = Column(DateTime)
    salary = Column(DECIMAL(10, 2))
    phone = Column(String(20))
    email = Column(String(255))


class Qualification(Base):
    __tablename__ = 'qualifications'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    qualification = Column(String(255))
    level = Column(String(255))
    certificate_number = Column(String(255))
    expiry_date = Column(DateTime)


class Vacation(Base):
    __tablename__ = 'vacations'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    type = Column(String(255))


class SickLeave(Base):
    __tablename__ = 'sick_leaves'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    reason = Column(Text)


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    description = Column(Text)
    status = Column(String(255))
    deadline = Column(DateTime)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Эндпоинт для получения информации о сотруднике
@app.route('/employee/<int:employee_id>')
def get_employee(employee_id):
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        return jsonify({
            'id': employee.id,
            'name': employee.name,
            'surname': employee.surname,
            'patronymic': employee.patronymic,
            'position': employee.position,
            'department': employee.department,
            'card_id': employee.card_id,
            'hire_date': employee.hire_date.isoformat(),
            'salary': employee.salary,
            'phone': employee.phone,
            'email': employee.email
        })
    else:
        return jsonify({'message': 'Сотрудник не найден'}), 404


# Эндпоинт для получения квалификаций сотрудника
@app.route('/employee/<int:employee_id>/qualifications')
def get_employee_qualifications(employee_id):
    qualifications = session.query(Qualification).filter_by(employee_id=employee_id).all()
    if qualifications:
        qualification_list = []
        for qualification in qualifications:
            qualification_list.append({
                'id': qualification.id,
                'qualification': qualification.qualification,
                'level': qualification.level,
                'certificate_number': qualification.certificate_number,
                'expiry_date': qualification.expiry_date.isoformat()
            })
        return jsonify({'qualifications': qualification_list})
    else:
        return jsonify({'message': 'Данные о квалификациях сотрудника не найдены'}), 404


# Эндпоинт для получения отпусков сотрудника
@app.route('/employee/<int:employee_id>/vacations')
def get_employee_vacations(employee_id):
    vacations = session.query(Vacation).filter_by(employee_id=employee_id).all()
    if vacations:
        vacation_list = []
        for vacation in vacations:
            vacation_list.append({
                'id': vacation.id,
                'start_date': vacation.start_date.isoformat(),
                'end_date': vacation.end_date.isoformat(),
                'type': vacation.type
            })
        return jsonify({'vacations': vacation_list})
    else:
        return jsonify({'message': 'Данные об отпусках сотрудника не найдены'}), 404


# Эндпоинт для получения больничных сотрудника
@app.route('/employee/<int:employee_id>/sick_leaves')
def get_employee_sick_leaves(employee_id):
    sick_leaves = session.query(SickLeave).filter_by(employee_id=employee_id).all()
    if sick_leaves:
        sick_leave_list = []
        for sick_leave in sick_leaves:
            sick_leave_list.append({
                'id': sick_leave.id,
                'start_date': sick_leave.start_date.isoformat(),
                'end_date': sick_leave.end_date.isoformat(),
                'reason': sick_leave.reason
            })
        return jsonify({'sick_leaves': sick_leave_list})
    else:
        return jsonify({'message': 'Данные о больничных сотрудника не найдены'}), 404


# Эндпоинт для получения задач сотрудника
@app.route('/employee/<int:employee_id>/tasks')
def get_employee_tasks(employee_id):
    tasks = session.query(Task).filter_by(employee_id=employee_id).all()
    if tasks:
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'description': task.description,
                'status': task.status,
                'deadline': task.deadline.isoformat()
            })
        return jsonify({'tasks': task_list})
    else:
        return jsonify({'message': 'Данные о задачах сотрудника не найдены'}), 404


# ... (Другие эндпоинты для работы с данными пока под вопросом)

if __name__ == '__main__':
    app.run(debug=True)
