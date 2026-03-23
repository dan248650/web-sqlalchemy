import requests
import json

BASE_URL = 'http://localhost:5000/api'


def print_response(response, title):
    print(title)
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(response.text)


def test_get_all_jobs():
    """Получение всех работ"""
    print("\nТест 1: Получение всех работ")
    response = requests.get(f'{BASE_URL}/jobs')

    if response.status_code == 200:
        data = response.json()
        print(f"Успешно")
    else:
        print(f"Ошибка: Статус {response.status_code}")

    return response


def api_login(email, password):
    """API авторизация"""
    print(f"\nАвторизация: {email}")
    response = requests.post(f'{BASE_URL}/login', json={
        'email': email,
        'password': password
    })
    print_response(response, f"POST /api/login")

    if response.status_code == 200:
        data = response.json()
        print(f"Авторизация успешна! Пользователь: {data['user']['name']}")
        return response.cookies
    else:
        print(f"Авторизация не удалась")
        return None


def test_add_job(cookies=None):
    """Добавление работы (POST)"""
    print("\nТест 6: Добавление новой работы")

    new_job = {
        "job": "Test Job from API",
        "team_leader": 2,
        "work_size": 10,
        "collaborators": [3, 4],
        "categories": [1, 2],
        "is_finished": False
    }

    print(f"Отправляем данные: {json.dumps(new_job, indent=2, ensure_ascii=False)}")
    response = requests.post(f'{BASE_URL}/jobs', json=new_job, cookies=cookies)
    print_response(response, "POST /api/jobs")

    if response.status_code == 201:
        print(f"Успешно: Работа создана с ID {response.json().get('id')}")
    elif response.status_code == 401:
        print("Требуется авторизация")
    else:
        print(f"Ошибка: Статус {response.status_code}")

    return response


def test_add_job_missing_fields(cookies=None):
    """Добавление работы с отсутствующими обязательными полями"""
    print("\nТест 7: Добавление работы без обязательных полей")

    new_job = {
        "job": "Test Job",
        "is_finished": False
    }

    print(f"Отправляем данные: {json.dumps(new_job, indent=2, ensure_ascii=False)}")
    response = requests.post(f'{BASE_URL}/jobs', json=new_job, cookies=cookies)
    print_response(response, "POST /api/jobs (неполные данные)")

    if response.status_code == 400:
        data = response.json()
        print(f"Успешно: Корректная ошибка 400")
        print(f"   Сообщение: {data.get('error')} - {data.get('message')}")
    else:
        print(f"Ошибка: Ожидался статус 400, получен {response.status_code}")

    return response


def test_add_job_invalid_team_leader(cookies=None):
    """Добавление работы с несуществующим тимлидом"""
    print("\nТест 8: Добавление работы с несуществующим тимлидом")

    new_job = {
        "job": "Test Job",
        "team_leader": 9999,
        "work_size": 10,
        "is_finished": False
    }

    print(f"Отправляем данные: {json.dumps(new_job, indent=2, ensure_ascii=False)}")
    response = requests.post(f'{BASE_URL}/jobs', json=new_job, cookies=cookies)
    print_response(response, "POST /api/jobs (неверный тимлид)")

    if response.status_code == 404:
        data = response.json()
        print(f"Успешно: Корректная ошибка 404")
        print(f"   Сообщение: {data.get('error')} - {data.get('message')}")
    else:
        print(f"Ошибка: Ожидался статус 404, получен {response.status_code}")

    return response


def test_add_job_empty_request(cookies=None):
    """Добавление работы с пустым телом запроса"""
    print("\nТест 9: Добавление работы с пустым телом запроса")
    response = requests.post(f'{BASE_URL}/jobs', json={}, cookies=cookies)
    print_response(response, "POST /api/jobs (пустой запрос)")

    if response.status_code == 400:
        data = response.json()
        print(f"Успешно: Корректная ошибка 400")
        print(f"   Сообщение: {data.get('error')} - {data.get('message')}")
    else:
        print(f"Ошибка: Ожидался статус 400, получен {response.status_code}")

    return response


def test_edit_job(cookies=None, job_id=1):
    """Редактирование работы (PUT)"""
    print("\nТест 10: Редактирование работы")

    edited_data = {
        "job": "Test edited Job from API",
        "team_leader": 2,
        "work_size": 15,
        "collaborators": [3, 4, 6],
        "categories": [1, 2, 3],
        "is_finished": True
    }

    print(f"Отправляем данные: {json.dumps(edited_data, indent=2, ensure_ascii=False)}")
    response = requests.put(f'{BASE_URL}/jobs/{job_id}', json=edited_data, cookies=cookies)
    print_response(response, f"PUT /api/jobs/{job_id}")

    if response.status_code == 200:
        print(f"Успешно: Работа с ID {response.json().get('id')} отредактирована")
    elif response.status_code == 401:
        print("Требуется авторизация")
    elif response.status_code == 403:
        print("Нет прав")
    else:
        print(f"Ошибка: Статус {response.status_code}")

    return response


def test_edit_job_invalid_id(cookies=None, job_id=10000):
    """Редактирование несуществующей работы"""
    print("\nТест 11: Редактирование несуществующей работы")

    edited_data = {
        "job": "Test edited Job from API",
        "team_leader": 2,
        "work_size": 15,
        "collaborators": [3, 4, 6],
        "categories": [1, 2, 3],
        "is_finished": True
    }

    print(f"Отправляем данные: {json.dumps(edited_data, indent=2, ensure_ascii=False)}")
    response = requests.put(f'{BASE_URL}/jobs/{job_id}', json=edited_data, cookies=cookies)
    print_response(response, f"PUT /api/jobs/{job_id} (неверный id)")

    if response.status_code == 404:
        data = response.json()
        print(f"Успешно: Корректная ошибка 404")
        print(f"   Сообщение: {data.get('error')} - {data.get('message')}")
    else:
        print(f"Ошибка: Ожидался статус 404, получен {response.status_code}")

    return response


def test_edit_job_invalid_team_leader(cookies=None, job_id=1):
    """Редактирование работы с несуществующим тимлидом"""
    print("\nТест 12: Редактирование работы с несуществующим тимлидом")

    edited_data = {
        "job": "Test edited Job from API",
        "team_leader": 10000,
        "work_size": 15,
        "collaborators": [3, 4, 6],
        "categories": [1, 2, 3],
        "is_finished": True
    }

    print(f"Отправляем данные: {json.dumps(edited_data, indent=2, ensure_ascii=False)}")
    response = requests.put(f'{BASE_URL}/jobs/{job_id}', json=edited_data, cookies=cookies)
    print_response(response, f"PUT /api/jobs/{job_id} (неверный тимлид)")

    if response.status_code == 404:
        data = response.json()
        print(f"Успешно: Корректная ошибка 404")
        print(f"   Сообщение: {data.get('error')} - {data.get('message')}")
    else:
        print(f"Ошибка: Ожидался статус 404, получен {response.status_code}")

    return response


def test_edit_job_empty_request(cookies=None, job_id=1):
    """Редактирование работы с пустым телом запроса"""
    print("\nТест 13: Редактирование работы с пустым телом запроса")
    response = requests.put(f'{BASE_URL}/jobs/{job_id}', json={}, cookies=cookies)
    print_response(response, f"PUT /api/jobs/{job_id} (пустой запрос)")

    if response.status_code == 400:
        data = response.json()
        print(f"Успешно: Корректная ошибка 400")
        print(f"   Сообщение: {data.get('error')} - {data.get('message')}")
    else:
        print(f"Ошибка: Ожидался статус 400, получен {response.status_code}")

    return response


def test_delete_job(cookies=None, job_id=1):
    """Удаление работы (DELETE)"""
    print("\nТест 14: Удаление работы")

    response = requests.delete(f'{BASE_URL}/jobs/{job_id}', cookies=cookies)
    print_response(response, f"DELETE /api/jobs/{job_id}")

    if response.status_code == 200:
        print(f"Успешно: Работа с ID {response.json().get('id')} удалена")
    elif response.status_code == 401:
        print("Требуется авторизация")
    elif response.status_code == 403:
        print("Нет прав")
    else:
        print(f"Ошибка: Статус {response.status_code}")

    return response


def test_delete_job_invalid_id(cookies=None, job_id=10000):
    """Удаление несуществующей работы"""
    print("\nТест 15: Удаление несуществующей работы")

    response = requests.delete(f'{BASE_URL}/jobs/{job_id}', cookies=cookies)
    print_response(response, f"DELETE /api/jobs/{job_id} (неверный id)")

    if response.status_code == 404:
        data = response.json()
        print(f"Успешно: Корректная ошибка 404")
        print(f"   Сообщение: {data.get('error')} - {data.get('message')}")
    else:
        print(f"Ошибка: Ожидался статус 404, получен {response.status_code}")

    return response


def main():
    try:
        response = requests.get(f'{BASE_URL}/jobs', timeout=3)
        print("Сервер доступен")
    except Exception:
        print("ОШИБКА: Сервер не доступен!")
        return

    cookies = api_login("admin@mars.org", password="WPUevGhB")

    if cookies:
        # POST
        test_add_job(cookies)

        test_add_job_missing_fields(cookies)
        test_add_job_invalid_team_leader(cookies)
        test_add_job_empty_request(cookies)

        # PUT
        test_edit_job(cookies)

        test_edit_job_invalid_id(cookies)
        test_edit_job_invalid_team_leader(cookies)
        test_edit_job_empty_request(cookies)

        # DELETE
        test_delete_job(cookies, 8)

        test_delete_job_invalid_id(cookies)
    else:
        print("Не удалось авторизоваться, тесты добавления, редактирования и удаления работ пропущены")


if __name__ == '__main__':
    main()
