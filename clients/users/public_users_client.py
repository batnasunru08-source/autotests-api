from typing import TypedDict
from httpx import Response
from clients.api_client import APIClient

class UserCreateRequest(TypedDict):
    """Структура данных для создания нового пользователя."""
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str

class PublicUsersClient(APIClient):
    """
    Клиент для работы с эндпоинтом /api/v1/users
    """

    def create_user_api(self, request: UserCreateRequest) -> Response:
        """
        Создаёт нового пользователя.

        Отправляет POST-запрос на /api/v1/users с данными пользователя.

        :param request: Словарь с обязательными полями:
            - email (str) – электронная почта,
            - password (str) – пароль,
            - lastName (str) – фамилия,
            - firstName (str) – имя,
            - middleName (str) – отчество.
        :return: Ответ сервера httpx.Response
        """
        return  self.post("/api/v1/users", json=request)