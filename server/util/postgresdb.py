from ..errors.postgreserror import PostgresError
from typing import Optional
import psycopg2


class PostgresDB:

    def __init__(self, host: str, username: str, password: str,
                 port: Optional[int] = 5432,
                 database: Optional[str] = "postgres") -> None:
        self.__host = host
        self.__username = username
        self.__password = password
        self.__port = port
        self.__database = database

    def execute(self, sql_statement: str,
                variables: Optional[tuple] = None) -> Optional[list[tuple]]:
        try:
            self.__pg = psycopg2.connect(host=self.__host,
                                         port=self.__port,
                                         user=self.__username,
                                         password=self.__password,
                                         database=self.__database)
            cursor = self.__pg.cursor()
            if variables is None:
                cursor.execute(sql_statement)
            else:
                cursor.execute(sql_statement, variables)
            self.__pg.commit()
            records = []
            try:
                records = cursor.fetchall()
            except Exception as e:
                records = []
            self.__pg.close()
            return records
        except Exception as e:
            self.__pg.rollback()
            self.__pg.close()
            raise PostgresError(str(e))
