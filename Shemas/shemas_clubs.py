response_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "count": {
            "type": "integer"
        },
        "next": {
            "type": ["string", "null"] # Может быть ссылкой или null
        },
        "previous": {
            "type": ["string", "null"] # Может быть ссылкой или null
        },
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "bookTitle": {
                        "type": "string"
                    },
                    "bookAuthors": {
                        "type": "string"
                    },
                    "publicationYear": {
                        "type": "integer"
                    },
                    "description": {
                        "type": "string"
                    },
                    "telegramChatLink": {
                        "type": "string",
                        "format": "uri" # Это ссылка, можно добавить формат для строгой проверки
                    },
                    "owner": {
                        "type": "integer"
                    },
                    "members": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        }
                    },
                    "reviews": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "club": {"type": "integer"},
                                "user": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "username": {"type": "string"}
                                    },
                                    "required": ["id", "username"]
                                },
                                "review": {"type": "string"},
                                "assessment": {"type": "integer"},
                                "readPages": {"type": "integer"},
                                "created": {"type": "string", "format": "date-time"},
                                # Поле modified может отсутствовать или быть null
                                "modified": {"type": ["string", "null"], "format": "date-time"}
                            },
                            # id, club, user, review, assessment, created обычно всегда есть
                            "required": ["id", "club", "user", "review", "assessment", "created"]
                        }
                    },
                    "created": {
                        "type": "string",
                        "format": "date-time"
                    },
                    # Поле modified может быть null
                    "modified": {
                        "type": ["string", "null"],
                        "format": "date-time"
                    }
                },
                # Обязательные поля для каждого клуба. Reviews не обязателен (может быть [])
                "required": [
                    "id", "bookTitle", "bookAuthors", "publicationYear", "description",
                    "telegramChatLink", "owner", "members", "created"
                ]
            }
        }
    },
    # count и results должны быть всегда в ответе
    "required": ["count", "results"]
}