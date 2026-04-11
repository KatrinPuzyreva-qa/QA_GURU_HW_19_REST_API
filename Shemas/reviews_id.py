response_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Review Object Schema",
  "description": "Схема для валидации одного объекта отзыва на книгу",
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
      "description": "Пользователь, оставивший отзыв",
      "properties": {
        "id": {
          "type": "integer",
          "description": "ID пользователя"
        },
        "username": {
          "type": "string",
          "description": "Имя пользователя"
        }
      },
      "required": ["id", "username"]
    },
    "review": {
      "type": "string",
      "description": "Текст отзыва"
    },
    "assessment": {
      "type": "integer",
      "description": "Оценка книги"
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
    "modified": {
      "type": ["string", "null"],
      "description": "Дата и время последнего изменения отзыва (если есть)",
      "format": "date-time"
    }
  },
  # Список обязательных полей. Поле 'modified' не обязательно, так как может быть null.
  "required": [
    "id",
    "club",
    "user",
    "review",
    "assessment",
    "readPages",
    "created"
  ]
}