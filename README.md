# Проект для парсинга товаров на Ozon

### Запуск проекта

1. Клонировать репозиторий
```bash
git clone git@github.com:viator3m/viator3m-test-o-parser.git
```
2. Создать в корне репозитория файл `.env` для хранения переменных окружения ([пример](example.env))
3. Развернуть контейнеры (backend, mysql, db, firefox, rabbit, celery, nginx)
```bash
docker-compose up
```

При запуске контейнеров проекта автоматизировано:
- создание тестового пользователя с именем/паролем указанными в .env-файле.
- запуск миграции в БД
- запуск Telegram-бота  

Для получения уведомлений о завершении парсинга в Telegram,
начать диалог с ботом [@parser_ozon_bot](https://t.me/parser_ozon_bot)
и указать свой telegram_id в .env-файле. (id можно получить у [@userinfobot](https://t.me/userinfobot))

Документация к API проекта будет доступна по адресу http://localhost/api/v1/swagger/


### Эндпойнты и запросы

- POST `/api/v1/products/` — запуск задачи на парсинг товаров
Принимает необязательный параметр products_count в теле запроса.
```json
{
  "products_count": 5
}
```
Параметр отвечает за количество товаров для парсинга.  
Дефолтное значение 10.  
В теле ответа возращается информационное сообщение:
```json
{
  "info": "Parsing started"
}
```
- GET `/api/v1/products/` получение списка товаров последнего парсинга
```json
[
    {
        "id": 1,
        "title": "название товара",
        "price": 1000,
        "link": "https://ozon.ru/product/<some_item>",
        "parser": 1
    }
]
```
- GET `/api/v1/products/{product_id}/` получение одного товара по id
```json
{
    "id": 1,
    "title": "название товара",
    "price": 1000,
    "link": "https://ozon.ru/product/<some_item>",
    "parser": 1
}
```