import json
from pathlib import Path

from ..errors.nosuchelementerror import NoSuchElementError
from ..daos.employeedao import EmployeeDAO
from ..util.postgresdb import PostgresDB
from ..entities.employee import Employee
from ..services.accountservices import AccountServices
from ..util.authenticator import Authenticator

credeitnal_file = open(
    f"{Path(__file__).parent.parent}\\config\\db_credentials.json")
credentials = json.load(credeitnal_file)
credeitnal_file.close()
TABLE_NAME = "test_employees"
database = PostgresDB(credentials["host"],
                      credentials["username"],
                      credentials["password"])
employee_dao = EmployeeDAO(database, TABLE_NAME)
employee_clear = Employee("asdf", "asdf", "asdf",
                          "asdf", "asdf", "asdf")


def test_create_load_account_success():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)
    session_id = account_services.create_account("example@gmail.com",
                                                 "exampleUsername",
                                                 "examplePassword",
                                                 "John", "Doe")
    employee = account_services.get_profile(session_id)
    assert employee.get_email() == "example@gmail.com"
    assert employee.get_username() == "exampleUsername"
    assert employee.get_password() == "examplePassword"
    assert employee.get_first_name() == "John"
    assert employee.get_last_name() == "Doe"
    assert employee.get_title() == "employee"


def test_create_account_fail1():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)
    try:
        session_id = account_services.create_account("gmail.com",
                                                     "exampleUsername",
                                                     "examplePassword",
                                                     "John", "Doe")
        assert False
    except ValueError as e:
        pass
    except Exception as e:
        assert False


def test_create_account_fail2():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)
    try:
        session_id = account_services.create_account("",
                                                     "",
                                                     "",
                                                     "", "")
        assert False
    except ValueError as e:
        pass
    except Exception as e:
        assert False


def test_log_into_account_success():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)

    session_id1 = account_services.create_account("example@gmail.com",
                                                  "exampleUsername",
                                                  "examplePassword",
                                                  "John", "Doe")
    session_id2 = account_services.log_into_account("exampleUsername",
                                                    "examplePassword")
    assert session_id1 != session_id2
    employee1 = account_services.get_profile(session_id1)
    employee2 = account_services.get_profile(session_id2)
    assert employee1.get_email() == employee2.get_email()
    assert employee1.get_first_name() == employee2.get_first_name()
    assert employee1.get_last_name() == employee2.get_last_name()
    assert employee1.get_password() == employee2.get_password()
    assert employee1.get_title() == employee2.get_title()
    assert employee1.get_username() == employee2.get_username()


def test_log_into_account_failure():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)

    account_services.create_account("example@gmail.com",
                                    "exampleUsername",
                                    "examplePassword",
                                    "John", "Doe")
    try:
        session_id2 = account_services.log_into_account("exampleUsername",
                                                        "incorrectPassword")
        assert False
    except NoSuchElementError as e:
        pass


def test_log_into_account_failure():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)

    account_services.create_account("example@gmail.com",
                                    "exampleUsername",
                                    "examplePassword",
                                    "John", "Doe")
    try:
        session_id2 = account_services.log_into_account("exampleUsername",
                                                        "incorrectPassword")
        assert False
    except NoSuchElementError as e:
        pass


def test_update_profile():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)

    session_id = account_services.create_account("example@gmail.com",
                                                 "exampleUsername",
                                                 "examplePassword",
                                                 "John", "Doe")
    account_services.update_profile(session_id, "newPassword")
    employee = account_services.get_profile(session_id)
    assert employee.get_email() == "example@gmail.com"
    assert employee.get_password() == "newPassword"


def test_login_admin():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)

    credeitnal_file = open(
        f"{Path(__file__).parent.parent}\\config\\admin_credentials.json")
    admin_credentials = json.load(credeitnal_file)
    credeitnal_file.close()
    account_services.create_account("example@gmail.com",
                                    "exampleUsername",
                                    "examplePassword",
                                    "John", "Doe")
    session_id = account_services.log_into_account(
        admin_credentials["username"],
        admin_credentials["password"])
    employee = account_services.get_profile(session_id)
    assert employee.get_email() == "admin@email.com"
    assert employee.get_username() == admin_credentials["username"]
    assert employee.get_password() == admin_credentials["password"]
    assert employee.get_first_name() == admin_credentials["firstName"]
    assert employee.get_last_name() == admin_credentials["lastName"]
    assert employee.get_title() == admin_credentials["title"]


def test_update_title_success():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)

    credeitnal_file = open(
        f"{Path(__file__).parent.parent}\\config\\admin_credentials.json")
    admin_credentials = json.load(credeitnal_file)
    credeitnal_file.close()
    account_services.create_account("example@gmail.com",
                                    "exampleUsername",
                                    "examplePassword",
                                    "John", "Doe")
    session_id = account_services.log_into_account(
        admin_credentials["username"],
        admin_credentials["password"])
    account_services.update_title(session_id, "example@gmail.com", "admin")
    employee = account_services.get_profile(session_id, "example@gmail.com")
    assert employee.get_email() == "example@gmail.com"
    assert employee.get_username() == "exampleUsername"
    assert employee.get_password() == "examplePassword"
    assert employee.get_first_name() == "John"
    assert employee.get_last_name() == "Doe"
    assert employee.get_title() == "admin"


def test_update_title_failure():
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    authenticator = Authenticator()
    account_services = AccountServices(TABLE_NAME, authenticator)

    credeitnal_file = open(
        f"{Path(__file__).parent.parent}\\config\\admin_credentials.json")
    admin_credentials = json.load(credeitnal_file)
    credeitnal_file.close()
    account_services.create_account("example@gmail.com",
                                    "exampleUsername",
                                    "examplePassword",
                                    "John", "Doe")
    session_id = account_services.log_into_account("exampleUsername",
                                                   "examplePassword")
    try:
        account_services.update_title(session_id, "example@gmail.com", "admin")
        assert False
    except PermissionError as e:
        pass
