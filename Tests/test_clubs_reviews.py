import requests
from jsonschema import validate
from Shemas.reviews import response_schema

BASE_URL = "https://book-club.qa.guru/api/v1"


def test_review_id_exists():
    response = requests.get(f"{BASE_URL}/clubs/reviews/?club=1")

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()

    # Ищем ID, который нужен
    target_id = 1
    review_found = False

    # Перебираем каждый отзыв в списке body['results']
    for review in body['results']:
        # Сравниваем id текущего отзыва с исходным
        if review['id'] == target_id:
            review_found = True
            print(f"✅ Отзыв с id={target_id} найден.")
            break # Выходим из цикла, так как мы нашли то, что искали

    # Если после завершения цикла переменная осталась False — тест падает
    assert review_found is True, f"Отзыв с id={target_id} не найден в результатах."

def test_get_reviews_for_specific_club():
    club_id = 1
    url = f"{BASE_URL}/clubs/reviews/?club={club_id}"

    response = requests.get(url)

    print("\\n--- Testing GET Reviews for Club (ID: 1) ---")
    print("Status code:", response.status_code)
    print("Body:", response.text)

    # Проверяем, что запрос прошел успешно
    assert response.status_code == 200, f"Failed to get reviews for club ID {club_id}"

    body = response.json()

    # 2. Валидация структуры ответа по схеме СПИСКА отзывов
    # Используем review_list_schema, а не club_schema!
    validate(instance=body, schema=response_schema)

    # 3. Логические проверки данных
    # Проверяем, что массив результатов не пустой (для ID 1 там должны быть отзывы)
    assert len(body['results']) > 0, f"No reviews found for club ID {club_id}"

    # Важная проверка: Все отзывы в ответе должны относиться к клубу с ID 1
    # Это проверяет корректность работы фильтрации на бэкенде.
    for review in body['results']:
        assert (
                review['club'] == club_id
        ), f"Review ID {review['id']} belongs to another club (ID {review['club']})"

    print("✅ Test passed: Reviews structure is valid and all reviews belong to club ID 1.")