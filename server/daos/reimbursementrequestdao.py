from abc import ABC, abstractmethod
from ..errors.nosuchelementerror import NoSuchElementError
from ..entities.reimbursementrequest import ReimbursementRequest
from ..util.postgresdb import PostgresDB


class ReimbursementRequestDAOInterface(ABC):

    @abstractmethod
    def save_object(self, request: ReimbursementRequest) -> None:
        pass

    @abstractmethod
    def load_objects(self, email: str) -> list[ReimbursementRequest]:
        pass

    @abstractmethod
    def load_object(self, id: int) -> ReimbursementRequest:
        pass

    @abstractmethod
    def load_all_objects(self) -> list[ReimbursementRequest]:
        pass

    @abstractmethod
    def remove_object(self, id: int) -> None:
        pass


class ReimbursementRequestDAO(ReimbursementRequestDAOInterface):

    def __init__(self, database: PostgresDB, table_name: str):
        self.__database = database
        self.__table_name = table_name
        self.__database.execute(f"""CREATE TABLE IF NOT EXISTS
            {self.__table_name} (
            email varchar(64) NOT NULL,
            amount NUMERIC,
            reason varchar(512),
            creation_date INT,
            closing_date INT,
            status varchar(16),
            responder varchar(64),
            response varchar(512),
            id SERIAL PRIMARY KEY);""")

    def save_object(self, request: ReimbursementRequest) -> None:
        sql = f"""SELECT * FROM {self.__table_name} WHERE id = %s;"""
        results = self.__database.execute(sql, (request.get_id(),))
        if len(results) == 0:
            sql = f"""INSERT INTO {self.__table_name}
            (email, amount, reason, creation_date,
            closing_date, status, responder, response)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
            rtn = self.__database.execute(sql, (request.get_email(),
                                                request.get_amount(),
                                                request.get_reason(),
                                                request.get_creation_date(),
                                                request.get_closing_date(),
                                                request.get_status(),
                                                request.get_responder(),
                                                request.get_response()))
            request.set_id(rtn[0][0])
        else:
            sql = f"""UPDATE {self.__table_name} SET email = %s,
                                                    amount = %s,
                                                    reason = %s,
                                                    creation_date = %s,
                                                    closing_date = %s,
                                                    status = %s,
                                                    responder = %s,
                                                    response = %s
                                                    WHERE id = %s"""
            self.__database.execute(sql, (request.get_email(),
                                          request.get_amount(),
                                          request.get_reason(),
                                          request.get_creation_date(),
                                          request.get_closing_date(),
                                          request.get_status(),
                                          request.get_responder(),
                                          request.get_response(),
                                          request.get_id()))

    def load_objects(self, email: str) -> list[ReimbursementRequest]:
        sql = f"""SELECT * FROM {self.__table_name} WHERE email = %s"""
        results = self.__database.execute(sql, (email,))
        requests = []
        for result in results:
            requests.append(ReimbursementRequest(result[0],
                                                 result[1],
                                                 result[2],
                                                 result[3],
                                                 result[4],
                                                 result[5],
                                                 result[8],
                                                 result[6],
                                                 result[7]))
        return requests

    def load_object(self, id: int) -> ReimbursementRequest:
        sql = f"""SELECT * FROM {self.__table_name} WHERE id = %s"""
        results = self.__database.execute(sql, (id,))
        if len(results) == 0:
            raise NoSuchElementError("This request id doesn't exist")
        result = results[0]
        return ReimbursementRequest(result[0],
                                    result[1],
                                    result[2],
                                    result[3],
                                    result[4],
                                    result[5],
                                    result[8],
                                    result[6],
                                    result[7])

    def load_all_objects(self) -> list[ReimbursementRequest]:
        sql = f"""SELECT * FROM {self.__table_name}"""
        results = self.__database.execute(sql)
        requests = []
        for result in results:
            requests.append(ReimbursementRequest(result[0],
                                                 result[1],
                                                 result[2],
                                                 result[3],
                                                 result[4],
                                                 result[5],
                                                 result[8],
                                                 result[6],
                                                 result[7]))
        return requests

    def remove_object(self, id: int) -> None:
        sql = f"""DELETE FROM {self.__table_name} WHERE id = %s"""
        self.__database.execute(sql, (id,))
