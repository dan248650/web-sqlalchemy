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
    """Тест 1: Получение всех работ"""
    print("\nТест 1: Получение всех работ")
    response = requests.get(f'{BASE_URL}/jobs')

    if response.status_code == 200:
        data = response.json()
        print(f"Успешно")
    else:
        print(f"Ошибка: Статус {response.status_code}")

    return response


def test_get_valid_job(job_id=1):
    """Тест 2: Корректное получение одной работы"""
    print(f"\nТест 2: Получение работы с ID {job_id}")
    response = requests.get(f'{BASE_URL}/jobs/{job_id}')

    if response.status_code == 200:
        data = response.json()
        job = data.get('job', {})
        print(f"Успешно: Найдена работа '{job.get('job')}'")
    else:
        print(f"Ошибка: Статус {response.status_code}")

    return response


def test_get_invalid_job_id():
    """Тест 3: Error - неверный ID"""
    print("\nТест 3: Получение работы с несуществующим ID")
    invalid_id = 9999
    response = requests.get(f'{BASE_URL}/jobs/{invalid_id}')

    if response.status_code == 404:
        data = response.json()
        print(f"Успешно: Корректная ошибка 404")
        print(f"   Сообщение: {data.get('error')} - {data.get('message')}")
    else:
        print(f"Ошибка: Ожидался статус 404, получен {response.status_code}")

    return response


def test_get_invalid_job_string():
    """Тест 4: Error - строка вместо ID"""
    print("\nТест 4: Получение работы со строковым ID")
    invalid_id = "abc"
    response = requests.get(f'{BASE_URL}/jobs/{invalid_id}')

    if response.status_code == 404:
        data = response.json()
        print(f"Успешно: Корректная ошибка 404")
        print(f"   Сообщение: {data.get('error')} - {data.get('message')}")
    else:
        print(f"Ошибка: Ожидался статус 404, получен {response.status_code}")

    return response


def test_get_invalid_job_negative():
    """Тест 5: Error - отрицательный ID"""
    print("\nТест 5: Получение работы с отрицательным ID")
    invalid_id = -1
    response = requests.get(f'{BASE_URL}/jobs/{invalid_id}')

    if response.status_code == 404:
        data = response.json()
        print(f"Успешно: Корректная ошибка 404 для отрицательного ID")
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

    test_get_all_jobs()
    test_get_valid_job(1)
    test_get_invalid_job_id()
    test_get_invalid_job_string()
    test_get_invalid_job_negative()


if __name__ == '__main__':
    main()
