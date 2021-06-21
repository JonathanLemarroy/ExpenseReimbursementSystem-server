

class ReimbursementRequest:
    def __init__(self, email: str, amount: float, reason: str,
                 creation_date: int, closing_date: int = 0,
                 status: str = "pending", id: int = 0,
                 responder: str = "n/a", response: str = "n/a") -> None:
        self.__email = email
        self.__amount = float(amount)
        self.__reason = reason
        self.__creation_date = creation_date
        self.__closing_date = closing_date
        self.__status = status
        self.__id = id
        self.__responder = responder
        self.__response = response

    def get_email(self) -> str:
        return self.__email

    def get_amount(self) -> int:
        return self.__amount

    def set_amount(self, new_amount: float) -> None:
        self.__amount = float(new_amount)

    def get_reason(self) -> str:
        return self.__reason

    def set_reason(self, new_reason) -> None:
        self.__reason = new_reason

    def get_creation_date(self) -> int:
        return self.__creation_date

    def set_creation_date(self, new_date) -> None:
        self.__creation_date = new_date

    def get_closing_date(self) -> int:
        return self.__closing_date

    def set_closing_date(self, date: int) -> None:
        self.__closing_date = date

    def get_status(self) -> str:
        return self.__status

    def set_status(self, new_status) -> None:
        self.__status = new_status

    def get_id(self) -> int:
        return self.__id

    def set_id(self, new_id) -> None:
        self.__id = new_id

    def get_responder(self) -> str:
        return self.__responder

    def set_responder(self, responder: str) -> None:
        self.__responder = responder

    def get_response(self) -> str:
        return self.__response

    def set_response(self, response: str) -> None:
        self.__response = response

    def to_json_dict(self) -> dict[str, int, str, int, int, str]:
        return {"email": self.__email, "amount": self.__amount,
                "reason": self.__reason, "creationDate": self.__creation_date,
                "closingDate": self.__closing_date, "status": self.__status,
                "id": self.__id, "responder": self.__responder,
                "response": self.__response}
