import httpx  # Импортируем библиотеку HTTPX

# Данные для входа в систему
login_payload = {
    "email": "user@example.com",
    "password": "string"
}

# Выполняем запрос на аутентификацию
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

# Выводим полученные токены
print("Login response:", login_response_data)
print("Status Code:", login_response.status_code)

# Назначаем access токен
access_token= login_response_data["token"]["accessToken"]

# Делаем get запрос
profile_response = httpx.get("http://localhost:8000/api/v1/users/me", headers={"accept": "application/json", "Authorization": f"Bearer {access_token}"})
profile_response_data = profile_response.json()

# Выводим полученные данные профиля
print("Get response:", profile_response_data)
print("Status Code:", profile_response.status_code)