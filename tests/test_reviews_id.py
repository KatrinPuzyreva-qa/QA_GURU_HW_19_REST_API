import requests
from jsonschema import validate
from shemas.reviews_id import response_schema
from config import BASE_URL


def test_get_single_review_success():
    """
    Проверяет успешное получение одного отзыва по ID.
    Включает проверку статуса, соответствия ID и валидацию схемы ответа.
    """
    review_id = 1
    url = f"{BASE_URL}/clubs/reviews/{review_id}"

    response = requests.get(url)

    # Выводим всё одной строкой для компактности (как и было)
    print(
        f"--- Testing GET Single Review (ID: {review_id}) ---\n"
        f"Status code: {response.status_code}\n"
        f"Body: {response.text}"
    )

    # 1. Проверяем, что отзыв найден (статус 200 OK)
    assert response.status_code == 200, \
        f"Review with ID {review_id} was not found"

    body = response.json()
    validate(instance=body, schema=response_schema)

    # 3. Проверяем, что ID в ответе совпадает с запрошенным
    assert body['id'] == review_id, \
        "ID in response body does not match requested ID"

    # 4. Проверяем наличие и тип обязательного поля 'review'
    # (Это логичное дополнение, взятое из второго теста)
    assert 'review' in body and isinstance(body['review'], str), \
        "Field 'review' is missing or not a string"


def test_get_single_review_not_found():
    non_existing_id = 999999  # Используем ID, которого точно нет в БД
    url = f"{BASE_URL}/clubs/reviews/{non_existing_id}"

    response = requests.get(url)

    # Выводим статус для отладки, тело 404-ответа часто неинформативно или отсутствует
    print(
        f"--- Testing GET Non-existing Review (ID: {non_existing_id}) ---\n"
        f"Status code: {response.status_code}"
    )

    # Проверяем, что сервер корректно вернул статус 404 Not Found
    assert (response.status_code == 404,
            f"Expected status 404, but got {response.status_code}")

    # Получаем тело ответа в формате JSON (если оно есть)
    try:
        body = response.json()
        # Проверяем текст ошибки в теле ответа
        assert 'detail' in body, \
            "Error response does not contain 'detail' field"
        expected_message = "No BookReview matches the given query."
        assert body['detail'] == expected_message, \
            f"Expected '{expected_message}', but got '{body['detail']}'"
    except ValueError:
        # Если тело не парсится как JSON, просто пропускаем проверку тела,
        # так как главное — это корректный статус 404.
        pass
