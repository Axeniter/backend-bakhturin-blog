# Название проекта

Тема №4: **Блог**. Сервис, где все могут быть авторами и читателями.

| | |
| --- | --- |
| Главная сущность | Пост (post) |
| Связанная сущность (1:N) | Комментарий (comment) |
| Фишка | ... |
| Стек | Python, FastAPI, SQLite |

## Как запустить (linux)

```bash
# repository install
git clone https://github.com/Axeniter/backend-bakhturin-blog.git
cd backend-bakhturin-blog

# requirements install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# server start
uvicorn src.main:app --reload --port 8000
```

Сервис работает на `http://localhost:8000`. Запросы для демонстрации лежат в `requests.http`.

## Эндпоинты

| Метод | Путь | Что делает | Ответ |
| --- | --- | --- | --- |
| GET | `/health` | Проверка, что сервис жив | 200 `{"status":"ok"}` |
| POST | `/api/posts` | Создать | 201 и объект с `id`; 400 при ошибке |
| GET | `/api/posts` | Список | 200 |
| GET | `/api/posts/{id}` | Получить одну запись | 200; 404 |
| PATCH | `/api/posts/{id}` | Изменить | 200; 400; 404 |
| DELETE | `/api/posts/{id}` | Удалить | 204; 404 |

## ER-диаграмма

<!-- С лабы 2. Блок mermaid GitHub рисует сам. -->

```mermaid
erDiagram
    parents ||--o{ children : "имеет"
    parents {
        int id PK
        varchar title
    }
    children {
        int id PK
        int parent_id FK
    }
```

## Интерфейс

<!-- С лабы 4: скриншот, например ![Интерфейс](docs/screenshot.png) -->
