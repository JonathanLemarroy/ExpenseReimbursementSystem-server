from abc import ABC, abstractmethod
from .postgresdb import PostgresDB
from ..errors.authenticationerror import AuthenticationError
from ..entities.employee import Employee
from ..daos.employeedao import EmployeeDAO
import secrets
import time


class AuthenticatorInterface(ABC):

    @abstractmethod
    def generate_session(self, email: str, TTL: int) -> str:
        pass

    @abstractmethod
    def get_session_owner(self, session_id: str) -> bool:
        pass


class Authenticator(AuthenticatorInterface):

    def __init__(self):
        self.__sessions: dict[str, (str, int)] = {}

    def generate_session(self, email: str, TTL: int) -> str:
        expriation_date = time.time() + TTL
        session_id = secrets.token_urlsafe(16)
        self.__sessions[session_id] = (email, expriation_date)
        return session_id

    def get_session_owner(self, session_id: str) -> str:
        try:
            session_time = self.__sessions[session_id][1]
            if time.time() <= session_time:
                return self.__sessions[session_id][0]
            else:
                return None
        except Exception as e:
            return None
