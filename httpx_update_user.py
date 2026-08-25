import httpx
from tools.fakers import get_random_email  # Импортируем функцию для генерации случайного email

# Создаем пользователя
create_user_payload = {
    "email": get_random_email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}
create_user_response = httpx.post("http://localhost:8000/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()
print('Create user data:', create_user_response_data)
print("Status Code:", create_user_response.status_code)

# Проходим аутентификацию
login_payload = {
    "email": create_user_payload['email'],
    "password": create_user_payload['password']
}
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print('Login data:', login_response_data)
print("Status Code:", login_response.status_code)


# Выполнить запрос patch для обновления
headers = {"Authorization": f"Bearer {login_response_data["token"]["accessToken"]}"}
user_id = create_user_response_data['user']['id']
user_email = create_user_response_data['user']['email']
change_user_payload = {
    "email": get_random_email(),
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

login_update = httpx.patch(f"http://localhost:8000/api/v1/users/{user_id}", headers=headers, json=change_user_payload)
login_update_data = login_update.json()
print('Login update data:', login_update_data)
print("Status Code:", login_update.status_code)