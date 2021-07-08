from abc import ABC, abstractmethod
from ..util.postgresdb import PostgresDB
from ..entities.employee import Employee
from ..errors.nosuchelementerror import NoSuchElementError


class EmployeeDAOInterface(ABC):

    @abstractmethod
    def save_object(self, employee: Employee) -> None:
        pass

    @abstractmethod
    def load_object(self, email: str = None, username: str = None) -> Employee:
        pass

    @abstractmethod
    def remove_object(self, email: str = None, username: str = None) -> None:
        pass


class EmployeeDAO(EmployeeDAOInterface):

    def __init__(self, database: PostgresDB, table_name: str) -> None:
        self.__database = database
        self.__table_name = table_name
        self.__database.execute(f"""CREATE TABLE IF NOT EXISTS
            {self.__table_name} (
            email varchar(64) UNIQUE NOT NULL,
            username varchar(64) UNIQUE NOT NULL,
            password varchar(64) NOT NULL,
            first_name varchar(64),
            last_name varchar(64),
            title varchar(64) );""")

    def save_object(self, employee: Employee) -> None:
        sql = f"""SELECT * FROM {self.__table_name} WHERE email = %s;"""
        results = self.__database.execute(sql, (employee.get_email(),))
        if len(results) == 0:
            sql = f"""INSERT INTO {self.__table_name}
            (email, username, password, first_name, last_name, title)
            VALUES
            (%s, %s, %s, %s, %s, %s);"""
            self.__database.execute(sql, (employee.get_email(),
                                          employee.get_username(),
                                          employee.get_password(),
                                          employee.get_first_name(),
                                          employee.get_last_name(),
                                          employee.get_title()))
        else:
            sql = f"""UPDATE {self.__table_name} SET username = %s,
                                                    password = %s,
                                                    first_name = %s,
                                                    last_name = %s, title = %s
                                                    WHERE email = %s"""
            self.__database.execute(sql, (employee.get_username(),
                                          employee.get_password(),
                                          employee.get_first_name(),
                                          employee.get_last_name(),
                                          employee.get_title(),
                                          employee.get_email()))

    def load_object(self, email: str = None, username: str = None) -> Employee:
        sql = None
        results = None
        if email is not None:
            sql = f"""SELECT * FROM {self.__table_name} WHERE email = %s"""
            results = self.__database.execute(sql, (email,))
        elif username is not None:
            sql = f"""SELECT * FROM {self.__table_name} WHERE username = %s"""
            results = self.__database.execute(sql, (username,))
        else:
            raise ValueError(
                """To access an account a valid
                username or password must be provided""")
        if len(results) == 0:
            raise NoSuchElementError(
                "No employees found with those credentials")
        result = results[0]
        return Employee(result[0], result[1], result[2],
                        result[3], result[4], result[5])

    def remove_object(self, email: str = None, username: str = None) -> None:
        sql = None
        if email is not None:
            sql = f"""DELETE FROM {self.__table_name} WHERE email = %s"""
            self.__database.execute(sql, (email,))
        elif username is not None:
            sql = f"""DELETE FROM {self.__table_name} WHERE username = %s"""
            self.__database.execute(sql, (username,))
        else:
            raise ValueError(
                """To access an account a valid
                username or password must be provided""")
