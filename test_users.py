import requests
import json

BASE_URL = 'http://localhost:5000/api/v2'


def print_response(response, title):
    print(f"\n{title}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)


def api_login(email, password):
    resp = requests.post('http://localhost:5000/api/login', json={'email': email, 'password': password})
    return resp.cookies if resp.status_code == 200 else None


def test_get_users(cookies):
    print("\n1. GET /users")
    resp = requests.get(f'{BASE_URL}/users', cookies=cookies)
    print_response(resp, "GET /api/v2/users")
    return resp.status_code == 200


def test_get_user(cookies, user_id):
    print(f"\n2. GET /users/{user_id}")
    resp = requests.get(f'{BASE_URL}/users/{user_id}', cookies=cookies)
    print_response(resp, f"GET /api/v2/users/{user_id}")
    return resp.status_code == 200


def test_get_user_not_found(cookies):
    print("\n3. GET /users/99999 (не существует)")
    resp = requests.get(f'{BASE_URL}/users/99999', cookies=cookies)
    print_response(resp, "GET /api/v2/users/99999")
    return resp.status_code == 404


def test_create_user(cookies):
    print("\n4. POST /users (корректный)")
    data = {
        "surname": "surname", "name": "name", "email": "test@mars.org",
        "password": "123", "age": 30, "position": "tester",
        "speciality": "qa", "address": "module_1", "city_from": "Moscow"
    }
    resp = requests.post(f'{BASE_URL}/users', json=data, cookies=cookies)
    print_response(resp, "POST /api/v2/users")
    return resp.json().get('id') if resp.status_code == 201 else None


def test_create_user_missing_fields(cookies):
    print("\n5. POST /users (без обязательных полей)")
    resp = requests.post(f'{BASE_URL}/users', json={"name": "Тест"}, cookies=cookies)
    print_response(resp, "POST /api/v2/users (неполные данные)")
    return resp.status_code == 400


def test_create_user_duplicate_email(cookies):
    print("\n6. POST /users (дубликат email)")
    data = {"surname": "Дубль", "name": "Тест", "email": "test@mars.org", "password": "123"}
    resp = requests.post(f'{BASE_URL}/users', json=data, cookies=cookies)
    print_response(resp, "POST /api/v2/users (дубликат)")
    return resp.status_code == 400


def test_update_user(cookies, user_id):
    print(f"\n7. PUT /users/{user_id} (корректный)")
    data = {"position": "senior", "city_from": "SPb"}
    resp = requests.put(f'{BASE_URL}/users/{user_id}', json=data, cookies=cookies)
    print_response(resp, f"PUT /api/v2/users/{user_id}")
    return resp.status_code == 200


def test_update_user_not_found(cookies):
    print("\n8. PUT /users/99999 (не существует)")
    resp = requests.put(f'{BASE_URL}/users/99999', json={"position": "test"}, cookies=cookies)
    print_response(resp, "PUT /api/v2/users/99999")
    return resp.status_code == 404


def test_update_user_duplicate_email(cookies, user_id):
    print("\n9. PUT /users (дубликат email)")
    data2 = {"surname": "2", "name": "test", "email": "second@mars.org", "password": "123"}
    resp2 = requests.post(f'{BASE_URL}/users', json=data2, cookies=cookies)
    if resp2.status_code == 201:
        second_id = resp2.json()['id']
        resp = requests.put(f'{BASE_URL}/users/{user_id}', json={"email": "second@mars.org"}, cookies=cookies)
        requests.delete(f'{BASE_URL}/users/{second_id}', cookies=cookies)
        print_response(resp, "PUT /api/v2/users (дубликат email)")
        return resp.status_code == 400
    return False


def test_delete_user(cookies, user_id):
    print(f"\n10. DELETE /users/{user_id}")
    resp = requests.delete(f'{BASE_URL}/users/{user_id}', cookies=cookies)
    print_response(resp, f"DELETE /api/v2/users/{user_id}")
    return resp.status_code == 200


def test_delete_user_not_found(cookies):
    print("\n11. DELETE /users/99999")
    resp = requests.delete(f'{BASE_URL}/users/99999', cookies=cookies)
    print_response(resp, "DELETE /api/v2/users/99999")
    return resp.status_code == 404


def test_delete_self(cookies):
    print("\n12. DELETE самого себя")
    resp = requests.get('http://localhost:5000/api/me', cookies=cookies)
    if resp.status_code == 200:
        current_id = resp.json()['user']['id']
        resp_del = requests.delete(f'{BASE_URL}/users/{current_id}', cookies=cookies)
        print_response(resp_del, f"DELETE /api/v2/users/{current_id} (сам себя)")
        return resp_del.status_code == 400
    return False


def test_access_denied():
    print("\n13. GET /users (обычный пользователь)")
    cookies = api_login("robert.taylor@mars.org", "taylor_password")
    if cookies:
        resp = requests.get(f'{BASE_URL}/users', cookies=cookies)
        print_response(resp, "GET /api/v2/users (обычный юзер)")
        return resp.status_code == 403
    return False


def main():
    print("ТЕСТИРОВАНИЕ RESTful API v2 (Flask-RESTful)")
    print()

    try:
        requests.get('http://localhost:5000/api/v2/users', timeout=2)
        print("Сервер доступен")
    except:
        print("Сервер не доступен!")
        return

    cookies = api_login("admin@mars.org", "KgM7RBNA")
    if not cookies:
        print("Ошибка авторизации")
        return

    results = []

    # GET тесты
    results.append(("GET всех пользователей", test_get_users(cookies)))
    results.append(("GET пользователя по ID", test_get_user(cookies, 1)))
    results.append(("GET несуществующего", test_get_user_not_found(cookies)))

    # POST тесты
    user_id = test_create_user(cookies)
    results.append(("POST создание", user_id is not None))
    results.append(("POST без полей", test_create_user_missing_fields(cookies)))
    results.append(("POST дубликат email", test_create_user_duplicate_email(cookies)))

    # PUT тесты
    if user_id:
        results.append(("PUT обновление", test_update_user(cookies, user_id)))
        results.append(("PUT несуществующий", test_update_user_not_found(cookies)))
        results.append(("PUT дубликат email", test_update_user_duplicate_email(cookies, user_id)))

    # DELETE тесты
    if user_id:
        results.append(("DELETE пользователя", test_delete_user(cookies, user_id)))
    results.append(("DELETE несуществующий", test_delete_user_not_found(cookies)))
    results.append(("DELETE себя", test_delete_self(cookies)))
    results.append(("Доступ запрещен", test_access_denied()))


if __name__ == '__main__':
    main()
