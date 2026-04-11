response_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "List of Reviews",
  "description": "Схема для валидации списка отзывов с пагинацией",
  "type": "object",
  "properties": {
    "count": {
      "type": "integer",
      "description": "Общее количество отзывов, соответствующих запросу"
    },
    "next": {
      "type": ["string", "null"],
      "description": "Ссылка на следующую страницу или null",
      "format": "uri"
    },
    "previous": {
      "type": ["string", "null"],
      "description": "Ссылка на предыдущую страницу или null",
      "format": "uri"
    },
    "results": {
      "type": "array",
      "description": "Массив объектов отзывов",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "description": "Уникальный идентификатор отзыва"
          },
          "club": {
            "type": "integer",
            "description": "ID клуба, к которому относится отзыв"
          },
          "user": {
            "type": "object",
            "description": "Информация о пользователе, оставившем отзыв",
            "properties": {
              "id": { "type": "integer" },
              "username": { "type": "string" }
            },
            "required": ["id", "username"]
          },
          "review": {
            "type": "string",
            "description": "Текст отзыва"
          },
          "assessment": {
            "type": "integer",
            "description": "Оценка книги (например, от 1 до 5)"
          },
          "readPages": {
            "type": "integer",
            "description": "Количество прочитанных страниц"
          },
          "created": {
            "type": "string",
            "description": "Дата и время создания отзыва",
            "format": "date-time"
          },
          # Поле 'modified' может быть строкой (дата) или отсутствовать (null)
          "modified": {
            "type": ["string", "null"],
            "description": "Дата и время последнего изменения отзыва",
            "format": "date-time"
          }
        },
        # Все поля, кроме 'modified', являются обязательными для отзыва
        "required": ["id", "club", "user", "review", "assessment", "readPages", "created"]
      }
    }
  },
  # Поля 'count' и 'results' всегда должны присутствовать в ответе
  #'next' и 'previous' могут быть null, но обычно присутствуют для структуры пагинации
  "required": ["count", "results"]
}