from http import HTTPStatus

import pytest

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from tests.fixtures.users import UserFixture
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema

@pytest.mark.authentication  # Добавили маркировку users
@pytest.mark.regression  # Добавили маркировку regression
def test_login(function_user: UserFixture, authentication_client: AuthenticationClient):

    # Запрос на логин (login_request -> request)
    request = LoginRequestSchema(email=function_user.email, password=function_user.password)
    # Выполняем логин (login_response -> response)
    response = authentication_client.login_api(request)
    # Валидация ответа (login_response_data -> response_data)
    response_data = LoginResponseSchema.model_validate_json(response.text)

    #Проверяем статус-код
    assert_status_code(response.status_code, HTTPStatus.OK)

    #Проверяем тело ответа
    assert_login_response(response_data)

    #Валидируем JSON-схему
    validate_json_schema(response.json(), LoginResponseSchema.model_json_schema())