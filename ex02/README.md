## Миграции

Первоначальная миграция:

- alembic revision --autogenerate -m "initial migration"

Обновление миграции

- alembic revision --autogenerate -m "add speed field to Spaceship"

Применил миграцию:

- alembic upgrade head
