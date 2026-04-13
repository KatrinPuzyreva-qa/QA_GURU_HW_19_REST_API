import pytest
import requests
from jsonschema import validate
from shemas.shemas_clubs import response_schema
from config import BASE_URL


def test_clubs_list_schema_and_count():
    response = requests.get(f"{BASE_URL}/clubs/")

    # Проверка HTTP-статуса
    assert response.status_code == 200, (
        f"Запрос к /clubs/ вернул статус {response.status_code}. "
        f"Ответ: {response.text}"
    )

    # Парсинг JSON и проверка структуры (схемы)
    body = response.json()
    try:
        validate(instance=body, schema=response_schema)
    except Exception as e:
        pytest.fail(f"Структура ответа не соответствует схеме: {e}")

    # Проверка бизнес-логики: количество клубов должно быть целым числом и больше 500
    count = body['count']
    assert isinstance(count, int), f"Значение 'count' должно быть integer, а не {type(count)}"

    assert count > 500, (
        f"Ожидаемое количество клубов больше 500, но получено {count}. "
        "Возможно, в тестовой базе недостаточно данных."
    )


def test_pagination_second_page():
    first_page_resp = requests.get(f"{BASE_URL}/clubs/")
    assert first_page_resp.status_code == 200
    first_page_data = first_page_resp.json()

    # Получаем вторую страницу
    second_page_resp = requests.get(f"{BASE_URL}/clubs/", params={"page": 2})

    assert second_page_resp.status_code == 200, (
        f"Не удалось получить вторую страницу. Статус: {second_page_resp.status_code}"
    )

    second_page_data = second_page_resp.json()

    # Проверка: данные на второй странице не должны быть идентичны первой
    # Сравниваем по ID элементов, так как это уникальный идентификатор.
    first_ids = {item["id"] for item in first_page_data["results"]}
    second_ids = {item["id"] for item in second_page_data["results"]}

    assert first_ids != second_ids, (
        "Пагинация не работает: вторая страница возвращает те же данные, что и первая.\n"
        f"ID на 1-й странице (первые 3): {[i for i in first_ids][:3]}\n"
        f"ID на 2-й странице (первые 3): {[i for i in second_ids][:3]}"
    )


def test_search_by_book_title():
    """
    Проверяет работу поиска по названию книги.
    Ищет клубы, где в названии книги есть слово 'Сети'.
    """
    search_query = "Сети"

    # Используем params для корректного кодирования строки в URL
    params = {"search": search_query}
    response = requests.get(f"{BASE_URL}/clubs/", params=params)

    assert response.status_code == 200, (
        f"Поиск по названию книги '{search_query}' завершился с ошибкой. "
        f"Статус: {response.status_code}. URL: {response.url}"
    )

    body = response.json()

    # Проверка: найдено хотя бы одно совпадение
    assert body["count"] >= 1, (
        f"По запросу '{search_query}' ничего не найдено. "
        "Либо сломан поиск, либо в базе нет подходящих данных."
    )

    # Проверка: хотя бы один из результатов действительно содержит искомое слово
    found = False
    for club in body["results"]:
        # .get() защищает от KeyError, если структура данных изменится
        book_title = club.get("bookTitle", "").lower()
        if search_query.lower() in book_title:
            found = True
            break

    assert found is True, (
        f"Логика поиска сломана: ни один из результатов не содержит '{search_query}'.\\n"
        f"Название первой найденной книги: '{body['results'][0].get('bookTitle', 'N/A')}'"
    )
