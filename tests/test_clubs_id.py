import requests
from jsonschema import validate
from shemas.clubs_id import response_schema
from config import BASE_URL


def test_get_id():
    response = requests.get(f"{BASE_URL}/clubs/1")

    # Выводим всё одной строкой для компактности
    print(
        f"\nStatus: {response.status_code}\n"
        f"Headers: {response.headers}\n"
        f"Body: {response.text}"
    )

    assert response.status_code == 200

    body = response.json()
    assert body['id'] == 1


def test_get_single_club_by_id():
    club_id = 1
    url = f"{BASE_URL}/clubs/{club_id}"

    response = requests.get(url)

    # Выводим всё одной строкой для компактности
    print(
        f"--- Testing GET Single Club (ID: {club_id}) ---\n"
        f"Status code: {response.status_code}\n"
        f"Body: {response.text}"
    )

    # Проверяем, что клуб найден
    assert response.status_code == 200, f"Club with ID {club_id} not found"

    body = response.json()

    # Валидация структуры ответа по схеме ОДНОГО клуба
    validate(instance=body, schema=response_schema)

    # Дополнительная проверка данных (что это действительно тот клуб)
    assert body['id'] == club_id, "Returned club ID does not match requested ID"
    assert body['bookTitle'] == "Сети", "Book title does not match expected value for ID 1"
