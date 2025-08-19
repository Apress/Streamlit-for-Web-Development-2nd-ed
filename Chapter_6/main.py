from flask import Flask, request
from DataBase import Employees
from DataBase.Connection import session_manager

app = Flask(__name__)


@app.route('/employees')
def get_all_employees():
    with session_manager() as session:
        employees = session.query(Employees).all()
        employees = [employee.to_dict() for employee in employees]
        return {"data": employees}


@app.route('/employee', methods=["POST"])
def add_employee():
    body = request.json
    with session_manager() as session:
        session.add(Employees(**body))
        session.commit()
    return {"message": "New employee added successfully"}

app.run()
