# aether

Aether Messenger — backend на FastAPI с PostgreSQL и миграциями Alembic.

## Локальный запуск

Понадобятся Python 3.12+, uv и Docker с Docker Compose.

1. В корне репозитория создайте `.env` из примера:

   ```powershell
   Copy-Item .env.example .env
   ```

   Если `.env` уже существует, дополните его вручную. В примере указан пароль
   для локальной разработки. При его изменении обновите и `POSTGRES_PASSWORD`,
   и пароль в `DATABASE_URL`. Реальный `.env` не добавляйте в Git.

2. Запустите PostgreSQL из корня репозитория и дождитесь готовности:

   ```powershell
   docker compose up -d --wait postgres
   ```

   База `aether` доступна на `localhost:5433`, пользователь — `aether`.
   Данные сохраняются в Docker volume `postgres_data`.

3. Установите зависимости и примените миграции:

   ```powershell
   cd backend
   uv sync --locked
   uv run --env-file ../.env alembic upgrade head
   ```

4. Из каталога `backend` запустите API:

   ```powershell
   uv run --env-file ../.env uvicorn app.main:app --reload
   ```

   Swagger UI: <http://127.0.0.1:8000/docs>.
   Проверка работы API: <http://127.0.0.1:8000/health/live>.

Параметр `--env-file ../.env` загружает настройки из корня репозитория:
при запуске из `backend` автоматический поиск `.env` в конфигурации приложения
относится к текущему каталогу.

Чтобы остановить PostgreSQL, выполните из корня репозитория:

```powershell
docker compose down
```

Данные базы сохранятся. `POSTGRES_PASSWORD` задаёт пароль при первой
инициализации базы; изменение `.env` не меняет пароль в существующем volume.

## Миграции

Команды выполняются из каталога `backend` при запущенном PostgreSQL.

```powershell
# Создать миграцию после изменения ORM-моделей
uv run --env-file ../.env alembic revision --autogenerate -m "describe schema change"

# Применить все миграции
uv run --env-file ../.env alembic upgrade head

# Посмотреть текущую ревизию
uv run --env-file ../.env alembic current
```

Проверяйте сгенерированные миграции перед применением и коммитом.

## Для разработчиков

- [Соглашение о коммитах](docs/COMMIT_CONVENTION.md)
- [Структура базы данных](docs/DATABASE.md)
- [ER-диаграмма drawio](docs/db-er-diagram.drawio)
