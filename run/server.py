import json

from ..services.accountservices import AccountServices
from ..services.requestservices import RequestServices
from ..util.authenticator import Authenticator
from ..errors.nosuchelementerror import NoSuchElementError
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
authenticator = Authenticator()
account_services = AccountServices("employees", authenticator)
request_services = RequestServices("requests", "employees", authenticator)


@app.route('/newEmployee', methods=['POST'])
def new_employee():
    try:
        data: dict = request.get_json()
        if data is None:
            return "Error parsing request", 400
        email: str = None
        username: str = None
        password: str = None
        first_name: str = None
        last_name: str = None
        for k, v in data.items():
            if k == "email":
                email = v
            elif k == "username":
                username = v
            elif k == "password":
                password = v
            elif k == "firstName":
                first_name = v
            elif k == "lastName":
                last_name = v
        session = account_services.create_account(email,
                                                  username,
                                                  password,
                                                  first_name,
                                                  last_name)
        return json.dumps({"session": session}), 201
    except (ValueError, NoSuchElementError) as e:
        return str(e), 406
    except Exception as e:
        print(str(e))
        return "A server error occured", 500


@app.route('/login', methods=['POST'])
def log_in():
    try:
        data: dict = request.get_json()
        if data is None:
            return "Error parsing request", 400
        user: str = None
        password: str = None
        for k, v in data.items():
            if k == "user":
                user = v
            elif k == "password":
                password = v
        session = account_services.log_into_account(user, password)
        return json.dumps({"session": session}), 200
    except (ValueError, NoSuchElementError) as e:
        return str(e), 406
    except Exception as e:
        print(str(e))
        return "A server error occured", 500


@app.route('/profile', methods=['GET'])
def get_profile():
    try:
        args = request.args.to_dict()
        session = ""
        email = None
        for k, v in args.items():
            if k == "session":
                session = v
            elif k == "email":
                email = v
        employee = account_services.get_profile(session, email)
        return json.dumps(employee.to_json_dict()), 200
    except (ValueError, NoSuchElementError, PermissionError) as e:
        return str(e), 406
    except Exception as e:
        print(str(e))
        return "A server error occured", 500


@app.route('/editTitle', methods=['PATCH'])
def edit_title():
    try:
        args = request.args.to_dict()
        session = ""
        for k, v in args.items():
            if k == "session":
                session = v
        data: dict = request.get_json()
        if data is None:
            return "Error parsing request", 400
        email_updated: str = ""
        new_title: str = ""
        for k, v in data.items():
            if k == "email":
                email_updated = v
            elif k == "title":
                new_title = v
        req = account_services.update_title(session, email_updated, new_title)
        return json.dumps(req.to_json_dict()), 200
    except (ValueError, NoSuchElementError, PermissionError) as e:
        return str(e), 406
    except Exception as e:
        print(str(e))
        return "A server error occured", 500


@app.route('/newRequest', methods=['POST'])
def new_request():
    try:
        args = request.args.to_dict()
        session = ""
        for k, v in args.items():
            if k == "session":
                session = v
        data: dict = request.get_json()
        if data is None:
            return "Error parsing request", 400
        amount: float = None
        reason: str = ""
        for k, v in data.items():
            if k == "amount":
                amount = float(v)
            elif k == "reason":
                reason = v
        req = request_services.create_request(session, amount, reason)
        return json.dumps(req.to_json_dict()), 201
    except (ValueError, NoSuchElementError, PermissionError) as e:
        return str(e), 406
    except Exception as e:
        print(str(e))
        return "A server error occured", 500


@app.route('/editRequest', methods=['PATCH'])
def edit_request():
    try:
        args = request.args.to_dict()
        session = ""
        for k, v in args.items():
            if k == "session":
                session = v
        data: dict = request.get_json()
        if data is None:
            return "Error parsing request", 400
        amount: int = None
        reason: str = None
        request_id: int = None
        for k, v in data.items():
            if k == "amount":
                amount = float(v)
            elif k == "reason":
                reason = v
            elif k == "id":
                request_id = int(v)
        req = request_services.edit_request(session, request_id,
                                            amount, reason)
        return json.dumps(req.to_json_dict()), 200
    except (ValueError, NoSuchElementError, PermissionError) as e:
        return str(e), 406
    except Exception as e:
        print(str(e))
        return "A server error occured", 500


@app.route('/deleteRequest', methods=['DELETE'])
def delete_request():
    try:
        args = request.args.to_dict()
        session = ""
        for k, v in args.items():
            if k == "session":
                session = v
        data: dict = request.get_json()
        if data is None:
            return "Error parsing request", 400
        requestId: int = 0
        for k, v in data.items():
            if k == "id":
                requestId = int(v)
        request_services.delete_request(session, requestId)
        return "Deleted request", 200
    except (ValueError, NoSuchElementError, PermissionError) as e:
        return str(e), 406
    except Exception as e:
        print(str(e))
        return "A server error occured", 500


@app.route('/getRequests', methods=['GET'])
def get_requests():
    try:
        args = request.args.to_dict()
        session = ""
        for k, v in args.items():
            if k == "session":
                session = v
        requests = request_services.get_requests(session)
        json_requests = []
        for req in requests:
            json_requests.append(req.to_json_dict())
        return json.dumps(json_requests), 200
    except (ValueError, NoSuchElementError) as e:
        return str(e), 406
    except Exception as e:
        print(str(e))
        return "A server error occured", 500


@app.route('/approveDenyRequest', methods=['PATCH'])
def approve_deny_requests():
    try:
        args = request.args.to_dict()
        session = ""
        for k, v in args.items():
            if k == "session":
                session = v
        data: dict = request.get_json()
        if data is None:
            return "Error parsing request", 400
        request_id: int = 0
        approved: bool = None
        response = None
        for k, v in data.items():
            if k == "id":
                request_id = v
            elif k == "approved":
                approved = v
            elif k == "response":
                response = v
        req = request_services.approve_deny_request(session, request_id,
                                                    approved, response)
        return json.dumps(req.to_json_dict()), 200
    except (ValueError, NoSuchElementError) as e:
        return str(e), 406
    except Exception as e:
        print(str(e))
        return "A server error occured", 500


app.run()
