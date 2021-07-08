import json
import time
from pathlib import Path
from ..util.postgresdb import PostgresDB
from ..util.authenticator import Authenticator
from ..daos.reimbursementrequestdao import ReimbursementRequestDAO
from ..daos.employeedao import EmployeeDAO
from ..entities.reimbursementrequest import ReimbursementRequest
from ..entities.employee import Employee
from ..util.permissions import Permissions
from ..errors.permissionerror import PermissionError


class RequestServices:

    def __init__(self, request_table: str, employee_table: str,
                 authenticator: Authenticator) -> None:
        credentials_file = open(
            f"{Path(__file__).parent.parent}\\config\\db_credentials.json")
        db_credentials = json.load(credentials_file)
        credentials_file.close()
        self.__request_dao = ReimbursementRequestDAO(
            PostgresDB(db_credentials["host"],
                       db_credentials["username"],
                       db_credentials["password"]),
            request_table)
        self.__employee_dao = EmployeeDAO(
            PostgresDB(db_credentials["host"],
                       db_credentials["username"],
                       db_credentials["password"]),
            employee_table)
        self.__authenticator = authenticator
        self.__permissions = Permissions()

    def create_request(self, session_id: str,
                       amount: float, reason: str) -> ReimbursementRequest:
        email: str = self.__authenticator.get_session_owner(session_id)
        if email is None:
            raise ValueError("Invalid session")
        employee = self.__employee_dao.load_object(email)
        if self.__permissions.has_permissions(employee, ("create_requests",)):
            if amount is None:
                raise ValueError("Amount cannot be none")
            if amount < 0:
                raise ValueError("Amount cannot be negative")
            request = ReimbursementRequest(employee.get_email(),
                                           amount, reason, time.time())
            self.__request_dao.save_object(request)
            return request
        else:
            raise PermissionError(
                "This account does not have permission to create requests")

    def edit_request(self, session_id: str,
                     request_id: int,
                     amount: float = None,
                     reason: str = None) -> ReimbursementRequest:
        email: str = self.__authenticator.get_session_owner(session_id)
        if email is None:
            raise ValueError("Invalid session")
        employee = self.__employee_dao.load_object(email)
        if self.__permissions.has_permissions(employee, ("edit_requests",)):
            if amount is None:
                raise ValueError("Amount cannot be none")
            if amount < 0:
                raise ValueError("Amount cannot be negative")
            request = self.__request_dao.load_object(request_id)
            if request.get_email() != employee.get_email():
                raise PermissionError(
                    "This account cannot edit this request")
            if request.get_closing_date() != 0:
                raise PermissionError(
                    "This request cannot be modified after being closed")
            if amount is not None:
                request.set_amount(amount)
            if reason is not None:
                request.set_reason(reason)
            request.set_creation_date(time.time())
            self.__request_dao.save_object(request)
            return request
        else:
            raise PermissionError(
                "This account does not have permission to edit requests")

    def delete_request(self, session_id: str,
                       request_id: int) -> None:
        email: str = self.__authenticator.get_session_owner(session_id)
        if email is None:
            raise ValueError("Invalid session")
        employee = self.__employee_dao.load_object(email)
        if self.__permissions.has_permissions(employee, ("edit_requests",)):
            request = self.__request_dao.load_object(request_id)
            if request.get_email() != employee.get_email():
                raise PermissionError(
                    "This account cannot delete this request")
            if request.get_closing_date() != 0:
                raise PermissionError(
                    "This request cannot be modified after being closed")
            self.__request_dao.remove_object(request.get_id())
        else:
            raise PermissionError(
                "This account does not have permission to edit requests")

    def get_requests(self, session_id: str) -> list[ReimbursementRequest]:
        email: str = self.__authenticator.get_session_owner(session_id)
        if email is None:
            raise ValueError("Invalid session")
        employee = self.__employee_dao.load_object(email)
        if self.__permissions.has_permissions(
                employee, ("view_all_requests",)):
            return self.__request_dao.load_all_objects()
        else:
            return self.__request_dao.load_objects(employee.get_email())

    def approve_deny_request(self, session_id: str,
                             request_id: int,
                             approved: bool,
                             response: str = None) -> ReimbursementRequest:
        email: str = self.__authenticator.get_session_owner(session_id)
        if email is None:
            raise ValueError("Invalid session")
        employee = self.__employee_dao.load_object(email)
        if self.__permissions.has_permissions(
                employee, ("approve_deny_requests",)):
            request = self.__request_dao.load_object(request_id)
            if approved:
                request.set_status("approved")
            else:
                request.set_status("denied")
            if response is not None:
                request.set_response(response)
            request.set_closing_date(time.time())
            self.__request_dao.save_object(request)
            return request
        else:
            raise PermissionError(
                "This account does not have permission to edit requests")
