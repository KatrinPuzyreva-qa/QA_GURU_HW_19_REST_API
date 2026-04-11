import requests
from jsonschema import validate
from Shemas.clubs_id import response_schema

BASE_URL = "https://book-club.qa.guru/api/v1"

def test_get_id():
    response = requests.get(f"{BASE_URL}/clubs/1")

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()

    assert body['id'] == 1
    print(f"🎉 Test passed: API correctly found books containing")


def test_get_single_club_by_id():
    club_id = 1
    url = f"{BASE_URL}/clubs/{club_id}"

    response = requests.get(url)

    print("\n--- Testing GET Single Club (ID: 1) ---")
    print("Status code:", response.status_code)
    print("Body:", response.text)

    # Проверяем, что клуб найден
    assert response.status_code == 200, f"Club with ID {club_id} not found"

    body = response.json()

    # Валидация структуры ответа по схеме ОДНОГО клуба
    validate(instance=body, schema=response_schema)

    # Дополнительная проверка данных (что это действительно тот клуб)
    assert body['id'] == club_id, "Returned club ID does not match requested ID"
    assert body['bookTitle'] == "Сети", "Book title does not match expected value for ID 1"

    print("✅ Test passed: Club structure is valid and data matches.")