# Реферальная система

Этот проект реализует систему авторизации пользователей по номеру телефона с генерацией кода для верификации и инвайт-кодами. Также реализованы профили пользователей и возможность активации инвайт-кодов.

## Стек технологий

- **Python 3.12**
- **Django 4.2**
- **Django REST Framework (DRF)**
- **PostgreSQL**
- **Redis** (для хранения кода подтверждения)
- **Docker**

## Функционал

1. **Авторизация по номеру телефона**
    - Первый запрос: Пользователь вводит свой номер телефона.
    - Сервер отправляет 4-значный код для верификации.
    - Второй запрос: Пользователь вводит полученный код.
    - Если пользователь не авторизовывался ранее, создается запись в базе данных с его номером телефона и уникальным 6-значным реферальным кодом.
    
2. **Инвайт-коды**
    - Пользователь может ввести чужой инвайт-код в своем профиле.
    - Пользователь может активировать только один инвайт-код. Если инвайт-код уже был активирован, он будет отображен в профиле.
    - В профиле пользователя отображается список номеров телефонов, которые использовали его инвайт-код.

3. **Профиль пользователя**
    - Запрос на получение профиля пользователя.
    - Профиль содержит информацию о статусе инвайт-кода и список пользователей, которые использовали инвайт.

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/CringeT1Me/referral_code
cd referral_core
```
### 2. Запустить Docker
```bash
docker compose up --build
```

## API

Документация доступна по ссылкам

 - http:/localhost:8000/redoc/
 - http:/localhost:8000/swagger/


### Вход в систему

####`POST /api/v1/login/`

- **Описание**: Отправка SMS с кодом подтверждения на указанный номер телефона.
- **Параметры**:
  - `data` (body):
    - `phone_number`: Номер телефона пользователя.
- **Ответы**:
  - `200`: Код подтверждения успешно отправлен.
  - `400`: Ошибка валидации данных.
---
### Ввод кода подтверждения

#### `POST /api/v1/verify/`

- **Описание**: Верификация введенного кода подтверждения.
- **Параметры**:
  - `data` (body):
    - `code`: Введенный код подтверждения.
- **Ответы**:
  - `200`: Успешный вход.
  - `400`: Неправильный код подтверждения.
---

### Выход из системы

#### `POST /api/v1/logout/`

- **Описание**: Завершает текущую сессию пользователя.
- **Ответы**:
  - `200`: Успешный выход из системы.
---

### Список пользователей

#### `GET /api/v1/users/`

- **Описание**: Возвращает список всех пользователей.
- **Ответы**:
  - `200`: Список пользователей.
  - `403`: Пользователь не авторизован.
---

### Применение реферального кода

#### `POST /api/v1/users/apply-referral/`

- **Описание**: Позволяет пользователю активировать реферальный код.
- **Параметры**:
  - `data` (body):
    - `referral_code`: Реферальный код для активации.
- **Ответы**:
  - `200`: Код успешно применен.
  - `400`: Ошибка валидации.
  - `403`: Пользователь не авторизован.
---

### Валидировать реферальный код

#### `GET /api/v1/users/validate-referral/{referral_code}/`

- **Описание**: Проверяет, доступен ли указанный реферальный код.
- **Параметры**:
  - `referral_code` (путь): Реферальный код для проверки.
- **Ответы**:
  - `200`: Код доступен.
  - `400`: Неверный код или код уже активирован.
  - `403`: Пользователь не авторизован.
---

### Профиль пользователя

#### `GET /api/v1/users/{id}/`

- **Описание**: Возвращает профиль конкретного пользователя по его ID.
- **Параметры**:
  - `id` (путь): Уникальный идентификатор пользователя.
- **Ответы**:
  - `200`: Детали пользователя.
  - `403`: Пользователь не авторизован.
  - `404`: Пользователь не найден.
---
