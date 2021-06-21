

class Employee:
    def __init__(self, email: str,
                 username: str,
                 password: str,
                 first_name: str,
                 last_name: str,
                 title: str) -> None:
        self.__email = email
        self.__username = username
        self.__password = password
        self.__first_name = first_name
        self.__last_name = last_name
        self.__title = title

    def get_email(self) -> str:
        return self.__email

    def set_email(self, new_email: str):
        self.__email = new_email

    def get_username(self) -> str:
        return self.__username

    def set_username(self, new_username: str):
        self.__username = new_username

    def get_password(self) -> str:
        return self.__password

    def set_password(self, new_password: str):
        self.__password = new_password

    def get_first_name(self) -> str:
        return self.__first_name

    def set_first_name(self, new_first_name):
        self.__first_name = new_first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def set_last_name(self, new_last_name: str):
        self.__last_name = new_last_name

    def get_title(self) -> str:
        return self.__title

    def set_title(self, new_title: str):
        self.__title = new_title

    def to_json_dict(self) -> dict[str, str, str, str]:
        return {"email": self.__email, "firstName": self.__first_name,
                "lastName": self.__last_name, "title": self.__title}
