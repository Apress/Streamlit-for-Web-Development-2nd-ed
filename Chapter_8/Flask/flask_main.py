from flask import Flask, request
from DataBase import Employees, Admins
from DataBase.Connection import session_manager
from Services import JWTService, HashingService
from Middleware import Middleware
from werkzeug import exceptions
import yaml

app = Flask(__name__)

with open(".streamlit/secrets.toml") as f:
    yaml_dict = yaml.safe_load(f)
    sing_up_key = yaml_dict['sing_up_key']
    jwt_secret = yaml_dict['jwt_secret']

jwt_service = JWTService(jwt_secret)
middleware = Middleware(jwt_service)
hashing_service = HashingService()

app.before_request(lambda: middleware.auth(request))


@app.route('/api/employees')
def get_all_employees():
    with session_manager() as session:
        employees = session.query(Employees).all()
        employees = [employee.to_dict() for employee in employees]
        return {"data": employees}


@app.route('/api/employee', methods=["POST"])
def add_employee():
    body = request.json
    with session_manager() as session:
        session.add(Employees(**body))
        session.commit()
    return {"message": "New employee added successfully"}


@app.route('/api/auth/login', methods=["POST"])
def log_in():
    username, password = request.json['username'], request.json['password']
    with session_manager() as session:
        admin_account = session.query(Admins).filter(
            Admins.username == username).first()
        print(1)
        if admin_account is None:
            # Username doesn't exist. But don't inform the client with that as
            # they can use it to bruteforce valid usernames
            return exceptions.Unauthorized(
                description="Incorrect username/password combination")
        print(2)

        # Checking if such hash can be generated from that password
        is_password_correct = hashing_service.check_bcrypt(
            password.encode("utf8"), admin_account.password_hash.encode("utf8"))
        print(3)
        if not is_password_correct:
            return exceptions.Unauthorized(
                description="Incorrect username/password combination")
        print(4)

        token_payload = {"username": username}
        token = jwt_service.generate(token_payload)
        print(5)

        if token is None:
            return exceptions.InternalServerError(description="Login failed")
        print(6)

        return {"token": token}


@app.route('/api/auth/sing_up', methods=["POST"])
def sign_up():
    username, password = request.json['username'], request.json['password']
    if request.headers.get("sing_up_key") != "sing_up_key":
        exceptions.Unauthorized(description="Incorrect Key")

    with session_manager() as session:
        password_hash = hashing_service.hash_bcrypt(
            password.encode("utf-8")).decode("utf-8")
        admin = Admins(username=username, password_hash=password_hash)
        session.add(admin)
        session.commit()
        return {"message": "Admin account created successfully"}


@app.route('/api/auth/is_logged_in')
def is_logged_in():
    # If this controller is reached this means the
    # Auth middleware recognizes the passed token
    return {"message": "Token is valid"}

app.run()
