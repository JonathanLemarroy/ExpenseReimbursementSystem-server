
import json
from pathlib import Path
from ..services.accountservices import AccountServices
from ..util.postgresdb import PostgresDB
from ..util.authenticator import Authenticator
from ..daos.employeedao import EmployeeDAO
from ..daos.reimbursementrequestdao import ReimbursementRequestDAO
from ..entities.employee import Employee
from ..entities.reimbursementrequest import ReimbursementRequest
from ..services.requestservices import RequestServices
from ..errors.permissionerror import PermissionError
from ..errors.nosuchelementerror import NoSuchElementError

credeitnal_file = open(
    f"{Path(__file__).parent.parent}\\config\\db_credentials.json")
credentials = json.load(credeitnal_file)
credeitnal_file.close()
EMPLOYEE_TABLE = "test_employees"
REQUEST_TABLE = "test_requests"
database = PostgresDB(credentials["host"],
                      credentials["username"],
                      credentials["password"])
request_dao = ReimbursementRequestDAO(database, REQUEST_TABLE)
employee_dao = EmployeeDAO(database, EMPLOYEE_TABLE)
request_clear = ReimbursementRequest("asdf", 0, "asdf", 0)
authenticator = Authenticator()
account_services = AccountServices(EMPLOYEE_TABLE, authenticator)
added_employee1 = None
added_employee2 = None
added_manager = None
employee_session1 = None
employee_session2 = None
manager_session = None


def test_init():
    global added_employee1
    global added_employee2
    global added_manager
    global employee_session1
    global employee_session2
    global manager_session
    added_employee1 = Employee("employee1@gmail.com", "employee1", "password",
                               "new", "employee", "employee")
    added_employee2 = Employee("employee2@gmail.com", "employee2", "password",
                               "new", "employee", "employee")
    added_manager = Employee("manager@gmail.com", "manager", "password",
                             "new", "manager", "manager")
    employee_dao.save_object(added_employee1)
    employee_dao.save_object(added_employee2)
    employee_dao.save_object(added_manager)
    employee_session1 = account_services.log_into_account("employee1@gmail.com",
                                                          "password")
    employee_session2 = account_services.log_into_account("employee2@gmail.com",
                                                          "password")
    manager_session = account_services.log_into_account("manager@gmail.com",
                                                        "password")


def test_create_request():
    request_dao.save_object(request_clear)
    database.execute(f"DELETE FROM {REQUEST_TABLE}")
    request_services = RequestServices(REQUEST_TABLE,
                                       EMPLOYEE_TABLE,
                                       authenticator)
    request = request_services.create_request(employee_session1, 100,
                                              "something random")
    assert request.get_id() != 0
    assert request.get_email() == added_employee1.get_email()
    assert request.get_amount() == 100
    assert request.get_reason() == "something random"
    assert request.get_creation_date() != 0
    assert request.get_closing_date() == 0
    assert request.get_status() == "pending"


def test_get_requests():
    request_dao.save_object(request_clear)
    database.execute(f"DELETE FROM {REQUEST_TABLE}")
    request_services = RequestServices(REQUEST_TABLE,
                                       EMPLOYEE_TABLE,
                                       authenticator)
    request = request_services.create_request(employee_session1, 100,
                                              "something random")
    request2 = request_services.create_request(employee_session2, 100,
                                               "something random")
    assert request2.get_id() != request.get_id()
    requests = request_services.get_requests(employee_session1)
    assert len(requests) == 1
    returned_request = requests[0]
    assert request.get_id() == returned_request.get_id()
    assert request.get_email() == returned_request.get_email()


def test_edit_request_success():
    request_dao.save_object(request_clear)
    database.execute(f"DELETE FROM {REQUEST_TABLE}")
    request_services = RequestServices(REQUEST_TABLE,
                                       EMPLOYEE_TABLE,
                                       authenticator)
    request = request_services.create_request(employee_session1, 100,
                                              "something random")
    edited_request = request_services.edit_request(employee_session1,
                                                   request.get_id(),
                                                   200, "new reason")
    assert edited_request.get_id() == request.get_id()
    assert edited_request.get_email() == added_employee1.get_email()
    assert edited_request.get_amount() == 200
    assert edited_request.get_reason() == "new reason"


def test_edit_request_failure():
    request_dao.save_object(request_clear)
    database.execute(f"DELETE FROM {REQUEST_TABLE}")
    request_services = RequestServices(REQUEST_TABLE,
                                       EMPLOYEE_TABLE,
                                       authenticator)
    request = request_services.create_request(employee_session1, 100,
                                              "something random")
    try:
        edited_request = request_services.edit_request(employee_session2,
                                                       request.get_id(),
                                                       200, "new reason")
        assert False
    except PermissionError as e:
        pass
    except Exception as e:
        assert False


def test_delete_request_success():
    request_dao.save_object(request_clear)
    database.execute(f"DELETE FROM {REQUEST_TABLE}")
    request_services = RequestServices(REQUEST_TABLE,
                                       EMPLOYEE_TABLE,
                                       authenticator)
    request = request_services.create_request(employee_session1, 100,
                                              "something random")
    edited_request = request_services.delete_request(employee_session1,
                                                     request.get_id())
    results = request_services.get_requests(employee_session1)
    assert len(results) == 0


def test_delete_request_failure():
    request_dao.save_object(request_clear)
    database.execute(f"DELETE FROM {REQUEST_TABLE}")
    request_services = RequestServices(REQUEST_TABLE,
                                       EMPLOYEE_TABLE,
                                       authenticator)
    request = request_services.create_request(employee_session1, 100,
                                              "something random")
    try:
        edited_request = request_services.delete_request(employee_session2,
                                                         request.get_id())
        assert True
    except PermissionError as e:
        pass
    except Exception as e:
        assert False


def test_approve_request_success():
    request_dao.save_object(request_clear)
    database.execute(f"DELETE FROM {REQUEST_TABLE}")
    request_services = RequestServices(REQUEST_TABLE,
                                       EMPLOYEE_TABLE,
                                       authenticator)
    request = request_services.create_request(employee_session1, 100,
                                              "something random")
    approved = request_services.approve_deny_request(manager_session,
                                                     request.get_id(),
                                                     True, "Something")
    assert approved.get_id() == request.get_id()
    assert approved.get_status() == "approved"


def test_deny_request_success():
    request_dao.save_object(request_clear)
    database.execute(f"DELETE FROM {REQUEST_TABLE}")
    request_services = RequestServices(REQUEST_TABLE,
                                       EMPLOYEE_TABLE,
                                       authenticator)
    request = request_services.create_request(employee_session1, 100,
                                              "something random")
    approved = request_services.approve_deny_request(manager_session,
                                                     request.get_id(),
                                                     False, "Something")
    assert approved.get_id() == request.get_id()
    assert approved.get_status() == "denied"


def test_approve_request_failure():
    request_dao.save_object(request_clear)
    database.execute(f"DELETE FROM {REQUEST_TABLE}")
    request_services = RequestServices(REQUEST_TABLE,
                                       EMPLOYEE_TABLE,
                                       authenticator)
    request = request_services.create_request(employee_session1, 100,
                                              "something random")
    try:
        approved = request_services.approve_deny_request(employee_session1,
                                                         request.get_id(),
                                                         True, "Something")
        assert False
    except PermissionError as e:
        pass
    except Exception as e:
        assert False
