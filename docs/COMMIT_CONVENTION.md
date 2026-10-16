# Соглашение о коммитах и ветках

В проекте используется **Conventional Commits**. Это соглашение помогает понимать историю изменений, искать исправления и проводить code review.

## 1. Формат сообщения коммита

```text
<type>(<scope>): <description>
```

- **type** — тип изменения, обязателен.
- **scope** — модуль или область изменения, необязателен (например, `auth`, `messages`, `frontend`, `infra`).
- **description** — краткое описание того, что сделано, обязательно.

Примеры:

```text
feat(auth): add user registration
fix(messages): prevent duplicate message creation
refactor(chats): simplify chat membership validation
test(auth): add registration unit tests
docs: describe local development setup
ci: run backend tests on pull requests
chore: update development dependencies
perf(messages): reduce message list query count
build(backend): update Docker image configuration
```

## 2. Допустимые типы

| Тип | Когда использовать |
| --- | --- |
| `feat` | Новая функциональность |
| `fix` | Исправление ошибки |
| `refactor` | Изменение структуры кода без изменения поведения |
| `docs` | Только документация |
| `test` | Добавление или изменение тестов |
| `chore` | Техническое обслуживание, не относящееся к другим типам |
| `ci` | Конфигурация CI/CD и автоматизации |
| `perf` | Оптимизация производительности |
| `build` | Сборка и зависимости сборки |

## 3. Правила оформления

1. Пишите сообщения коммитов **на английском языке**.
2. Используйте типы и scope в нижнем регистре: `feat(auth)`, а не `Feat(Auth)`.
3. Пишите описание в повелительном наклонении: `add`, `fix`, `remove`, `update`, а не `added`, `fixed`.
4. Не ставьте точку в конце первой строки.
5. Делайте коммит **логически завершённым**: одна самостоятельная цель — один коммит. Не обязательно один файл или одна строка изменений.
6. Не включайте в коммит пароли, токены, реальные `.env` и другие секреты.
7. Перед коммитом просмотрите изменения и убедитесь, что нет случайных файлов или отладочного кода.

**Хорошо:**

```text
feat(messages): add message pagination
fix(auth): reject expired access tokens
docs(api): document chat endpoints
```

**Плохо:**

```text
update
fix bugs
changes
feat: added stuff.
final final version
```

## 4. Именование веток

Формат:

```text
<type>/<issue-number>-<short-description>
```

Примеры:

```text
feat/12-user-registration
fix/24-message-duplication
refactor/31-auth-service
docs/35-api-guide
ci/40-backend-pipeline
```

Если задача не заведена в GitHub Issues, допускается название без номера, например `chore/update-dependencies`. Но для функциональных задач желательно сначала создать Issue.

Создавайте рабочую ветку от актуальной `main`. Не работайте напрямую в `main`.

## 5. Рекомендуемый рабочий процесс

```bash
# Обновить main
git switch main
git pull origin main

# Создать ветку для задачи
git switch -c feat/12-user-registration

# Проверить изменения
git status
git diff

# Добавить нужные файлы
git add backend/app/modules/auth/

# Проверить подготовленные изменения
git diff --cached

# Создать коммит
git commit -m "feat(auth): add user registration"

# Опубликовать ветку
git push -u origin feat/12-user-registration
```

После публикации откройте Pull Request в `main`, заполните шаблон PR и запросите review. Замечания исправляйте в той же ветке; после одобрения выполните merge. Удаляйте объединённые рабочие ветки.

## 6. Как связывать изменения с Issue

В описании Pull Request используйте:

```text
Closes #12
```

После merge PR в основную ветку связанный Issue автоматически закроется, если условия автозакрытия GitHub выполнены.

В сообщении коммита номер задачи указывать необязательно: связь можно оформить через PR.

## 7. Большие изменения и breaking changes

Если изменение несовместимо с предыдущим публичным интерфейсом, используйте `!` после типа или scope и поясните несовместимость в теле коммита:

```text
feat(api)!: change message response format

BREAKING CHANGE: message IDs are now returned as strings.
```

Для сложных изменений можно добавить тело после пустой строки:

```text
fix(messages): prevent duplicate delivery

Deduplicate incoming events by message ID before persistence.
This avoids repeated messages after client retries.
```

## 8. Что делать, если ошиблись

- **Ещё не отправили коммит:** можно исправить последний коммит через `git commit --amend`.
- **Уже отправили ветку и по ней идёт review:** предпочтительно создать новый исправляющий коммит, чтобы не переписывать историю без согласования.
- **Изменения уже в `main`:** создайте отдельный исправляющий PR. Для отмены коммита обычно используйте `git revert`, а не переписывание общей истории.

**Важно:** если секрет попал в Git, простого удаления файла новым коммитом недостаточно. Немедленно отзовите или замените секрет и сообщите участникам проекта.

## 9. Краткая проверка перед push

- [ ] Название ветки соответствует соглашению.
- [ ] Коммиты имеют понятный тип и описание.
- [ ] В коммит попали только нужные изменения.
- [ ] Тесты и линтеры запущены, если применимо.
- [ ] Нет секретов, временных файлов и отладочного кода.
- [ ] Для задачи подготовлен PR со ссылкой на Issue.
