import requests
from jsonschema import validate
from shemas.reviews import review_list_schema
from config import BASE_URL


def test_review_id_exists():
    response = requests.get(f"{BASE_URL}/clubs/reviews/?club=1")

    # Выводим всё одной строкой для компактности
    print(
        f"--- Testing Review ID Existence ---\n"
        f"Status code: {response.status_code}\n"
        f"Body: {response.text}"
    )

    assert response.status_code == 200

    body = response.json()

    # Проверяем наличие отзыва с нужным ID в списке (более лаконично)
    target_id = 1

    # any() возвращает True, если хотя бы один элемент в генераторе True.
    # Условие `if review_found` эквивалентно `if review_found is True`.
    review_found = any(review['id'] == target_id for review in body['results'])

    # Если отзыв не найден, тест падает с понятным сообщением
    assert review_found, f"Отзыв с id={target_id} не найден в результатах."


def test_get_reviews_for_specific_club():
    club_id = 1
    url = f"{BASE_URL}/clubs/reviews/?club={club_id}"

    response = requests.get(url)

    # Выводим всё одной строкой для компактности
    print(
        f"--- Testing GET Reviews for Club (ID: {club_id}) ---\n"
        f"Status code: {response.status_code}\n"
        f"Body: {response.text}"
    )

    # Проверяем, что запрос прошел успешно
    assert response.status_code == 200, f"Failed to get reviews for club ID {club_id}"

    body = response.json()

    # Валидация структуры ответа по схеме СПИСКА отзывов
    validate(instance=body, schema=review_list_schema)

    # Логические проверки данных
    assert len(body['results']) > 0, f"No reviews found for club ID {club_id}"

    # Проверяем, что все отзывы в ответе относятся к клубу с ID 1
    for review in body['results']:
        assert review['club'] == club_id, \
            f"Review ID {review['id']} belongs to another club (ID {review['club']})"
