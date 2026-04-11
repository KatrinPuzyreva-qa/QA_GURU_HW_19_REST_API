import requests
from jsonschema import validate
from Shemas.shemas_clubs import response_schema

BASE_URL = "https://book-club.qa.guru/api/v1"

def test_count():
    response = requests.get(f"{BASE_URL}/clubs/")

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()

    assert body['count'] == 592


def test_count_with_schema_validation():
    response = requests.get(f"{BASE_URL}/clubs/")

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(instance=body, schema=response_schema)

    assert body['count'] == 592


def test_pagination_second_page():
    # Запрос к первой странице
    response_first = requests.get(f"{BASE_URL}/clubs/")
    body_first = response_first.json()
    first_page_results = body_first['results']

    # Запрос ко второй странице
    response_second = requests.get(f"{BASE_URL}/clubs/?page=2")

    print("\n--- Testing Pagination (Page 2) ---")
    print("Status code:", response_second.status_code)
    assert response_second.status_code == 200, "Failed to get second page"

    body_second = response_second.json()

    # Проверяем, что общее количество элементов не изменилось
    assert body_second['count'] == 592, "Total count changed on second page"

    # Проверяем, что список клубов на второй странице отличается от первой
    # Это доказывает, что пагинация работает, а не отдает одни и те же данные
    assert body_second['results'] != first_page_results, "Second page returns the same data as the first page"

    print("✅ Pagination test passed: Second page has different data.")


def test_search_by_book_title():
    # Название книги для поиска
    search_query = "Сети"

    # Кодируем строку для URL (заменяем пробелы и кириллицу на спецсимволы)
    encoded_query = requests.utils.requote_uri(search_query)

    # Формируем итоговый URL
    url = f"{BASE_URL}/clubs/?search={encoded_query}'"

    response = requests.get(url)

    print("\n--- Testing Search by Book Title ---")
    print(f"Search Query: '{search_query}'")
    print(f"Request URL: {url}")
    print("Status code:", response.status_code)

    assert response.status_code == 200, f"Search request failed with status {response.status_code}"

    body = response.json()

    # Проверяем, что в результатах есть данные
    # Если API работает верно, мы должны найти хотя бы одну книгу.
    assert body['count'] >= 1, f"No books found with title '{search_query}'"

    # Проверяем содержимое ответа
    # Проходим по всем найденным клубам и ищем наше название
    found = False
    for club in body['results']:
        # Проверяем, содержит ли title исходную строку (без учета регистра)
        if search_query.lower() in club['bookTitle'].lower():
            found = True
            print(f"✅ Found match: ID {club['id']}, Title: '{club['bookTitle']}'")
            break  # Достаточно найти один раз, чтобы тест подтвердил логику

    # Если после проверки всех клубов совпадение не найдено — тест падает
    assert found is True, f"Search logic error: No club titles contain '{search_query}'"

    print(f"🎉 Test passed: API correctly found books containing '{search_query}'.")