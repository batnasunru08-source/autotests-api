from http import HTTPStatus

import pytest
from clients.errors_schema import InternalErrorResponseSchema

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesQuerySchema, \
    GetExercisesResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(self, exercises_client: ExercisesClient, function_course: CourseFixture):
        # Формируем запрос на создание задания, используя id созданного курса
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        # Отправляем POST-запрос на создание задания
        response = exercises_client.create_exercise_api(request)
        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа (200 OK)
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что тело ответа соответствует запросу
        assert_create_exercise_response(request, response_data)

        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())


    def test_get_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        # Отправляем GET-запрос на получение созданного задания
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа (200 OK)
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что тело ответа соответствует ответу на создание задания
        assert_get_exercise_response(response_data, function_exercise.response)

        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())


    def test_update_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        # Формируем данные для обновления задания
        request = UpdateExerciseRequestSchema()
        # Отправляем PATCH-запрос на обновление задания
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id, request)
        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа (200 OK)
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что тело ответа соответствует запросу на обновление
        assert_update_exercise_response(request, response_data)

        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())


    def test_delete_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        # 1. Удаляем задание
        delete_response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)
        # 2. Проверяем, что задание успешно удалено (статус 200 OK)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # 3. Пытаемся получить удаленное задание
        get_response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # 4. Проверяем, что сервер вернул 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        # 5. Проверяем, что в ответе содержится ошибка "Exercise not found"
        assert_exercise_not_found_response(get_response_data)

        # 6. Проверяем, что ответ соответствует схеме
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())


    def test_get_exercises(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture,
            function_exercise: ExerciseFixture
    ):
        # Формируем параметры запроса, передавая course_id
        query = GetExercisesQuerySchema(course_id=function_course.response.course.id)
        # Отправляем GET-запрос на получение списка заданий
        response = exercises_client.get_exercises_api(query)
        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что список заданий соответствует ранее созданным заданиям
        assert_get_exercises_response(response_data, [function_exercise.response])

        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())
