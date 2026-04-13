response_schema = {
"$schema": "http://json-schema.org/draft-07/schema#",
"title": "Book Club Schema",
"description": "Схема для валидации объекта книжного клуба",
"type": "object",
"properties": {
"id": {
"type": "integer",
"description": "Уникальный идентификатор клуба"
},
"bookTitle": {
"type": "string",
"description": "Название книги"
},
"bookAuthors": {
"type": "string",
"description": "Автор(ы) книги"
},
"publicationYear": {
"type": "integer",
"description": "Год публикации книги"
},
"description": {
"type": "string",
"description": "Описание клуба или книги"
},
"telegramChatLink": {
"type": "string",
"description": "Ссылка на чат в Telegram",
"format": "uri"
},
"owner": {
"type": "integer",
"description": "ID владельца клуба"
},
"members": {
"type": "array",
"description": "Список ID участников клуба",
"items": {
"type": "integer"
}
},
"reviews": {
"type": "array",
"description": "Список отзывов о книге в клубе",
"items": {
"type": "object",
"properties": {
"id": { "type": "integer" },
"club": { "type": "integer" },
"user": {
"type": "object",
"properties": {
"id": { "type": "integer" },
"username": { "type": "string" }
},
"required": ["id", "username"]
},
"review": { "type": "string" },
"assessment": { "type": "integer" },
"readPages": { "type": "integer" },
# Дата и время в формате ISO 8601
"created": { "type": "string", "format": "date-time" },
# Поле может быть строкой (дата) или отсутствовать (null)
"modified": {
"type": ["string", "null"],
"format": "date-time"
}
},
#Отзыв всегда должен иметь эти поля
"required": ["id", "club", "user", "review", "assessment", "readPages", "created"]
}
},
# Дата создания клуба
"created": {
"type": "string",
"format": "date-time"
},
# Поле может быть строкой (дата) или отсутствовать (null)
"modified": {
"type": ["string", "null"],
"format": "date-time"
}
},
#Эти поля обязательны для каждого клуба
# reviews не обязательно, так как массив может быть пустым []
# modified не обязательно, так как может быть null
"required": [
"id",
"bookTitle",
"bookAuthors",
"publicationYear",
"description",
"telegramChatLink",
"owner",
"members",
"created"
]
}