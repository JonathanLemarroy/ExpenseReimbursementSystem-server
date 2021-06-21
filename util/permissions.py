import json
from pathlib import Path
from ..entities.employee import Employee


class Permissions:

    def __init__(self) -> None:
        self.__perms: dict[str, list[str]] = json.load(
            open(f"{Path(__file__).parent.parent}\\config\\title_permissions.json"))

    def has_permissions(self, employee: Employee,
                        permissions_required: tuple[str]):
        employee_perms = []
        if employee.get_title() in self.__perms.keys():
            employee_perms = self.__perms[employee.get_title()]
        has_permission = True
        for perm in permissions_required:
            if perm not in employee_perms:
                has_permission = False
                break
        return has_permission
