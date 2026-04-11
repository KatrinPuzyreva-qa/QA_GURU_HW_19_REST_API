import requests
from jsonschema import validate
from Shemas.reviews_id import response_schema

BASE_URL = "https://book-club.qa.guru/api/v1"


def test_get_single_review_success():
    review_id = 1
    url = f"{BASE_URL}/clubs/reviews/{review_id}"

    response = requests.get(url)

    print(f"\n--- Testing GET Single Review (ID: {review_id}) ---")
    print("Status code:", response.status_code)
    print("Body:", response.text)

    #  Проверяем, что отзыв найден (статус 200 OK)
    assert response.status_code == 200, f"Review with ID {review_id} was not found"

    body = response.json()

    # Проверяем, что ID в ответе совпадает с запрошенным
    assert body['id'] == review_id, "ID in response body does not match requested ID"

    print("✅ Test passed: Review exists and status is 200.")


def test_get_single_review_schema_validation():
    review_id = 1
    url = f"{BASE_URL}/clubs/reviews/{review_id}"

    response = requests.get(url)

    # Мы предполагаем, что отзыв существует, основываясь на предыдущем тесте
    assert response.status_code == 200, "Precondition failed: Review must exist for schema validation"

    body = response.json()

    # Валидация структуры ответа по схеме ОДНОГО отзыва
    validate(instance=body, schema=response_schema)

    # Проверяем наличие обязательного поля 'review'
    assert 'review' in body and isinstance(body['review'], str), "Field 'review' is missing or not a string"

    print("\n✅ Test passed: Response structure is valid according to JSON Schema.")


def test_get_single_review_not_found():
    non_existing_id = 999999  # Используем ID, которого точно нет в БД
    url = f"{BASE_URL}/clubs/reviews/{non_existing_id}"

    response = requests.get(url)

    print(f"\n--- Testing GET Non-existing Review (ID: {non_existing_id}) ---")
    print("Status code:", response.status_code)

    # Проверяем, что сервер корректно вернул статус 404 Not Found
    assert response.status_code == 404, f"Expected status 404, but got {response.status_code}"

    # Получаем тело ответа в формате JSON
    body = response.json()

    # 2. Проверяем текст ошибки в теле ответа
    assert 'detail' in body, "Error response does not contain 'detail' field"

    # Проверяем, что текст сообщения об ошибке совпадает с ожидаемым
    expected_message = "No BookReview matches the given query."
    assert body['detail'] == expected_message, f"Expected '{expected_message}', but got '{body['detail']}'"

    print("✅ Test passed: API correctly handles non-existing review (Status 404) and returns expected error message.")