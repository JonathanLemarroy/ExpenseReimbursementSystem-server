from ..errors.nosuchelementerror import NoSuchElementError
from ..util.postgresdb import PostgresDB
from ..entities.employee import Employee
from ..daos.employeedao import EmployeeDAO
from pathlib import Path
import json

credentials_file = open(
    f"{Path(__file__).parent.parent}\\config\\db_credentials.json")
credentials = json.load(credentials_file)
credentials_file.close()
TABLE_NAME = "test_employees"
database = PostgresDB(credentials["host"],
                      credentials["username"],
                      credentials["password"])
employee_dao = EmployeeDAO(database, TABLE_NAME)


def test_save_load_employee():
    employee1 = Employee("example1@mail.com", "exampleUsername1",
                         "examplePassword1", "John1", "Smith1", "employee")
    employee2 = Employee("example2@mail.com", "exampleUsername2",
                         "examplePassword2", "John2", "Smith2", "manager")
    employee_dao.save_object(employee1)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    employee_dao.save_object(employee2)
    employee_dao.save_object(employee1)
    new_employee = employee_dao.load_object(employee1.get_email())
    assert new_employee.get_email() == employee1.get_email()
    assert new_employee.get_first_name() == employee1.get_first_name()
    assert new_employee.get_last_name() == employee1.get_last_name()
    assert new_employee.get_password() == employee1.get_password()
    assert new_employee.get_title() == employee1.get_title()
    assert new_employee.get_username() == employee1.get_username()
    assert new_employee.get_email() != employee2.get_email()
    assert new_employee.get_first_name() != employee2.get_first_name()
    assert new_employee.get_last_name() != employee2.get_last_name()
    assert new_employee.get_password() != employee2.get_password()
    assert new_employee.get_title() != employee2.get_title()
    assert new_employee.get_username() != employee2.get_username()


def test_remove_employee():
    employee_clear = Employee("asdf", "asdf", "asdf",
                              "asdf", "asdf", "asdf")
    employee = Employee("example2@mail.com", "exampleUsername2",
                        "examplePassword2", "John2", "Smith2", "manager")
    employee_dao.save_object(employee_clear)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    employee_dao.save_object(employee)
    new_employee = employee_dao.load_object(email="example2@mail.com")
    assert new_employee.get_email() == employee.get_email()
    employee_dao.remove_object(employee.get_email())
    try:
        employee_dao.load_object(email="example2@mail.com")
        assert False
    except NoSuchElementError as e:
        assert True
