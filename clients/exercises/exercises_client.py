from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class GetExercisesQueryString(TypedDict):
    """
    Описание структуры запроса на получении заданий для определенного курса.
    """

class GetExerciseQueryString(TypedDict):
    """
    Описание структуры запроса на получение информации о задании по exercise_id.
    """

class CreateExerciseQueryString(TypedDict):
    """
    Описание структуры запроса на создание задания.
    """

class UpdateExerciseQueryString(TypedDict):
    """
    Описание структуры запроса на обновление задания.
    """

class DeleteExerciseQueryString(TypedDict):
    """
    Описание структуры запроса на удаление задания.
    """

class ExercisesClient(APIClient):



    def get_exercises_api:
        pass

    def get_exercise_api:
        pass

    def create_exercise_api:
        pass

    def update_exercise_api:
        pass

    def delete_exercise_api:
        pass
