from abc import ABC, abstractmethod
import json
from pathlib import Path
from time import struct_time
from ..util.permissions import Permissions
from ..errors.nosuchelementerror import NoSuchElementError
from ..util.postgresdb import PostgresDB
from ..entities.employee import Employee
from ..daos.employeedao import EmployeeDAO
from ..util.authenticator import Authenticator
import re


class AccountServicesInterface(ABC):

    @abstractmethod
    def create_account(self, email: str, username: str,
                       password: str, first_name: str,
                       last_name: str) -> str:
        pass

    @abstractmethod
    def log_into_account(self, user: str,
                         password: str) -> str:
        pass

    @abstractmethod
    def get_profile(self, session_id: str,
                    other_email: str = None) -> Employee:
        pass

    @abstractmethod
    def update_profile(self, session_id: str,
                       password: str = None,
                       first_name: str = None,
                       last_name: str = None) -> Employee:
        pass

    @abstractmethod
    def update_title(self, session_id: str, employee_updated: str,
                     new_title: str) -> Employee:
        pass


class AccountServices(AccountServicesInterface):

    def __init__(self, employee_table: str,
                 authenticator: Authenticator) -> None:
        credeitnal_file = open(
            f"{Path(__file__).parent.parent}\\config\\db_credentials.json")
        db_credentials = json.load(credeitnal_file)
        credeitnal_file.close()
        credeitnal_file = open(
            f"{Path(__file__).parent.parent}\\config\\admin_credentials.json")
        admin_credentials = json.load(credeitnal_file)
        credeitnal_file.close()
        self.__employee_dao = EmployeeDAO(
            PostgresDB(db_credentials["host"],
                       db_credentials["username"],
                       db_credentials["password"]),
            employee_table)
        admin = Employee("admin@email.com",
                         admin_credentials["username"],
                         admin_credentials["password"],
                         admin_credentials["firstName"],
                         admin_credentials["lastName"],
                         admin_credentials["title"])
        self.__employee_dao.save_object(admin)
        self.__authenticator = authenticator
        self.__permissions = Permissions()

    def create_account(self, email: str, username: str,
                       password: str, first_name: str,
                       last_name: str) -> str:
        regex = r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$"
        message = ""
        if not re.search(regex, email):
            message += "Email is not a valid email\n"
        else:
            try:
                self.__employee_dao.load_object(email=email)
                message += "This email is already in use\n"
            except NoSuchElementError as e:
                pass
        if len(username) == 0:
            message += "Username cannot be empty\n"
        else:
            try:
                self.__employee_dao.load_object(username=username)
                message += "This username is already in use\n"
            except NoSuchElementError as e:
                pass
        if len(password) == 0:
            message += "Password cannot be empty\n"
        if len(first_name) == 0:
            message += "First name cannot be empty\n"
        if len(last_name) == 0:
            message += "Last name cannot be empty\n"
        if len(message) != 0:
            raise ValueError(message)
        employee = Employee(email, username, password,
                            first_name, last_name, "employee")
        self.__employee_dao.save_object(employee)
        session_id = self.__authenticator.generate_session(
            employee.get_email(), 86400)
        return session_id

    def log_into_account(self, user: str,
                         password: str) -> str:
        message = ""
        if len(user) == 0:
            message += "User cannot be empty\n"
        if len(password) == 0:
            message += "Password cannot be empty\n"
        if len(message) != 0:
            raise ValueError(message)
        employee = None
        try:
            employee = self.__employee_dao.load_object(email=user)
        except NoSuchElementError as e:
            pass
        try:
            employee = self.__employee_dao.load_object(username=user)
        except NoSuchElementError as e:
            pass
        if employee is not None and employee.get_password() == password:
            session_id = self.__authenticator.generate_session(
                employee.get_email(), 86400)
            return session_id
        else:
            raise NoSuchElementError("Invalid username or password")

    def get_profile(self, session_id: str,
                    other_email: str = None) -> Employee:
        current_email: str = self.__authenticator.get_session_owner(session_id)
        if current_email is None:
            raise ValueError("Invalid session")
        if other_email is None:
            return self.__employee_dao.load_object(current_email)
        else:
            return self.__employee_dao.load_object(other_email)

    def update_profile(self, session_id: str,
                       password: str = None,
                       first_name: str = None,
                       last_name: str = None) -> Employee:
        email: str = self.__authenticator.get_session_owner(session_id)
        if email is None:
            raise ValueError("Invalid session")
        employee = self.__employee_dao.load_object(email)
        if password is not None:
            employee.set_password(password)
        if first_name is not None:
            employee.set_first_name(first_name)
        if last_name is not None:
            employee.set_last_name(last_name)
        self.__employee_dao.save_object(employee)
        return employee

    def update_title(self, session_id: str, employee_updated: str,
                     new_title: str) -> Employee:
        email: str = self.__authenticator.get_session_owner(session_id)
        if email is None:
            raise ValueError("Invalid session")
        employee = self.__employee_dao.load_object(email)
        if self.__permissions.has_permissions(employee, ("modify_titles",)):
            modified_employee = self.__employee_dao.load_object(
                employee_updated)
            modified_employee.set_title(new_title)
            self.__employee_dao.save_object(modified_employee)
            return modified_employee
        else:
            raise PermissionError(
                "This account does not have permission to modify titles")
