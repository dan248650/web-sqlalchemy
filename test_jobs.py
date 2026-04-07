import requests
import json
import datetime

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


def test_get_all_jobs(cookies):
    print("\n1. GET /jobs")
    resp = requests.get(f'{BASE_URL}/jobs', cookies=cookies)
    print_response(resp, "GET /api/v2/jobs")
    return resp.status_code == 200


def test_get_job(cookies, job_id):
    print(f"\n2. GET /jobs/{job_id}")
    resp = requests.get(f'{BASE_URL}/jobs/{job_id}', cookies=cookies)
    print_response(resp, f"GET /api/v2/jobs/{job_id}")
    return resp.status_code == 200


def test_get_job_not_found(cookies):
    print("\n3. GET /jobs/99999 (не существует)")
    resp = requests.get(f'{BASE_URL}/jobs/99999', cookies=cookies)
    print_response(resp, "GET /api/v2/jobs/99999")
    return resp.status_code == 404


def test_create_job(cookies):
    print("\n4. POST /jobs (корректный)")
    today = datetime.datetime.now().date().isoformat()
    data = {
        "job": "Test RESTful Job",
        "team_leader": 1,
        "work_size": 25,
        "start_date": today,
        "collaborators": [2, 3],
        "categories": [1, 2],
        "is_finished": False
    }
    resp = requests.post(f'{BASE_URL}/jobs', json=data, cookies=cookies)
    print_response(resp, "POST /api/v2/jobs")
    return resp.json().get('id') if resp.status_code == 201 else None


def test_create_job_missing_fields(cookies):
    print("\n5. POST /jobs (без обязательных полей)")
    resp = requests.post(f'{BASE_URL}/jobs', json={"job": "Test"}, cookies=cookies)
    print_response(resp, "POST /api/v2/jobs (неполные данные)")
    return resp.status_code == 400


def test_create_job_invalid_team_leader(cookies):
    print("\n6. POST /jobs (несуществующий тимлид)")
    data = {"job": "Test", "team_leader": 99999, "work_size": 10}
    resp = requests.post(f'{BASE_URL}/jobs', json=data, cookies=cookies)
    print_response(resp, "POST /api/v2/jobs (неверный тимлид)")
    return resp.status_code == 404


def test_create_job_invalid_date(cookies):
    print("\n7. POST /jobs (неверный формат даты)")
    data = {
        "job": "Test",
        "team_leader": 1,
        "work_size": 10,
        "start_date": "2023-13-45"
    }
    resp = requests.post(f'{BASE_URL}/jobs', json=data, cookies=cookies)
    print_response(resp, "POST /api/v2/jobs (неверная дата)")
    return resp.status_code == 400


def test_update_job(cookies, job_id):
    print(f"\n8. PUT /jobs/{job_id} (корректный)")
    data = {
        "job": "Updated RESTful Job",
        "work_size": 50,
        "is_finished": True
    }
    resp = requests.put(f'{BASE_URL}/jobs/{job_id}', json=data, cookies=cookies)
    print_response(resp, f"PUT /api/v2/jobs/{job_id}")
    return resp.status_code == 200


def test_update_job_not_found(cookies):
    print("\n9. PUT /jobs/99999 (не существует)")
    resp = requests.put(f'{BASE_URL}/jobs/99999', json={"job": "test"}, cookies=cookies)
    print_response(resp, "PUT /api/v2/jobs/99999")
    return resp.status_code == 404


def test_update_job_invalid_team_leader(cookies, job_id):
    print(f"\n10. PUT /jobs/{job_id} (неверный тимлид)")
    resp = requests.put(f'{BASE_URL}/jobs/{job_id}',
                        json={"team_leader": 99999}, cookies=cookies)
    print_response(resp, f"PUT /api/v2/jobs/{job_id} (неверный тимлид)")
    return resp.status_code == 404


def test_delete_job(cookies, job_id):
    print(f"\n11. DELETE /jobs/{job_id}")
    resp = requests.delete(f'{BASE_URL}/jobs/{job_id}', cookies=cookies)
    print_response(resp, f"DELETE /api/v2/jobs/{job_id}")
    return resp.status_code == 200


def test_delete_job_not_found(cookies):
    print("\n12. DELETE /jobs/99999")
    resp = requests.delete(f'{BASE_URL}/jobs/99999', cookies=cookies)
    print_response(resp, "DELETE /api/v2/jobs/99999")
    return resp.status_code == 404


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
    results.append(("GET всех работ", test_get_all_jobs(cookies)))
    results.append(("GET работы по ID", test_get_job(cookies, 1)))
    results.append(("GET несуществующей", test_get_job_not_found(cookies)))

    # POST тесты
    job_id = test_create_job(cookies)
    results.append(("POST создание", job_id is not None))
    results.append(("POST без полей", test_create_job_missing_fields(cookies)))
    results.append(("POST неверный тимлид", test_create_job_invalid_team_leader(cookies)))
    results.append(("POST неверная дата", test_create_job_invalid_date(cookies)))

    # PUT тесты
    if job_id:
        results.append(("PUT обновление", test_update_job(cookies, job_id)))
        results.append(("PUT несуществующий", test_update_job_not_found(cookies)))
        results.append(("PUT неверный тимлид", test_update_job_invalid_team_leader(cookies, job_id)))

    # DELETE тесты
    if job_id:
        results.append(("DELETE работы", test_delete_job(cookies, job_id)))
    results.append(("DELETE несуществующей", test_delete_job_not_found(cookies)))


if __name__ == '__main__':
    main()
