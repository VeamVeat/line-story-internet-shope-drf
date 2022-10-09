# Line Story
> API интернет магазина по продаже картин 

---

## Оглавление
* [Общее](#общее)
* [Используемые языки и фрейворки](#используемые-языки-и-фрейворки)
* [Используемые базы данных](#используемые-базы-данных)
* [Функции API](#функции-api)
* [Настройка проекта и запуск проекта](#настройка-проекта-и-запуск-проекта)
* [Применение](#применение)


## Общее
- API интернет магазина
- целью являет продажа картин ручной работы с необычной техникой изготовления
- Изготовление картин было моим хобби и с целью распространения своего творчества был необходим свой интернет магазин
- <img src="https://user-images.githubusercontent.com/67123448/194765156-326737e1-9e40-4a64-9e75-3b4a44670b5f.png" align="center" width="600" height="300" />

## Используемые языки и фрейворки
- Python 3.10
- Django 4.1
- Django Rest Framework 3.13.1
- Pytest 7.1.3
- Celery 5.2.7

## Используемые технологие
- Docker 20.10.18

## Используемые базы данных
- Posrgresql 2.9.3
- Redis 4.3.4

## Функции API
-  http://127.0.0.1:8000/admin/users/user/{id} -> забанить пользователя (post)
- http://127.0.0.1:8000/api/jwtauth/email-verify/ -> подтверждение регистрации (patch)
- http://127.0.0.1:8000/api/jwtauth/login/ -> вход (post)
- http://127.0.0.1:8000//api/jwtauth/logout/ -> выход (post)
- http://127.0.0.1:8000/api/jwtauth/password-reset/complete/ -> установка нового пароля (patch)
- http://127.0.0.1:8000/api/jwtauth/password-reset/confirm/{uid64}/{token}/ -> переход по ссылке в почте для сброса пароля (get)
- http://127.0.0.1:8000/api/jwtauth/password-reset/email/ -> отправка email для сброса пароля (post)
- http://127.0.0.1:8000/api/jwtauth/register/ -> зарегистрировать нового пользователя (post)
- http://127.0.0.1:8000/api/jwtauth/token/ -> получить новый access токен (post)
- http://127.0.0.1:8000/api/jwtauth/token/refresh/ -> получить новый refresh токен (post)
- http://127.0.0.1:8000/api/orders/cart/ -> получить список товаров в корзине (get)
- http://127.0.0.1:8000/api/orders/cart/diminish_product/-> уменьшить количество товара в корзине (post)
- http://127.0.0.1:8000/api/orders/cart/{product_id}/ -> удалить товар из корзины (delete)
- http://127.0.0.1:8000/api/orders/reserved/ -> получить список зарезервированных товаров (get)
- http://127.0.0.1:8000/api/orders/reserved/ -> зарезервировать товар (post)
- http://127.0.0.1:8000/api/orders/reserved/{product_id}/ -> удалить товар из резерва
- http://127.0.0.1:8000/api/products/all/ -> получить список всех продуктов (get)
- http://127.0.0.1:8000/api/products/{product_id}/ -> показать детальное описание продукта (get)
- http://127.0.0.1:8000/api/orders/reserved/{product_id}/ -> показать профиль пользователя (get)
- http://127.0.0.1:8000/api/users/profile/{id}/ -> обновить информацию профиля пользователя (patch)

## Настройка и запуск проекта
Каковы требования/зависимости проекта? Где они перечислены? Возможно, файл requirements.txt или файл Pipfile.lock? Где он находится?

Перейдите к описанию того, как установить / настроить локальную среду / начать работу с проектом.

## Применение
Для начала склонируйте репозиторий и установить зависимости

`git clone https://github.com/VeamVeat/line_story_internet_shope_drf.git`

`pip install -r requirements.txt`

#### Для локального запуска
`python manage.py runserver 8000`

#### Для запуска develop версии проекта
- `make build` билдим наш docker-compose файл
- `make up` поднимаем наш контейнер со всеми зависимыми сервисами в docker-compose файле
- `make login` заходим в работающий контейнер
- `pytest` выполняем команду в контейнере для прогона тестов
- Убеждаемся что наши тесты пройдены
- <img src="https://user-images.githubusercontent.com/67123448/194768136-8e5d4cf7-0d95-4961-92ec-abcd460239c4.png" align="center" width="600" height="300" />
- перейти в браузере по ссылке http://0.0.0.0:8000

#### Для запуска develop версии проекта на alpine
- `make build-alpine` билдим наш docker-compose файл
- `make up-alpine` поднимаем наш контейнер со всеми зависимыми сервисами в docker-compose файле
- `make login-alpine` заходим в работающий контейнер
- `pytest` выполняем команду в контейнере для прогона тестов
- Убеждаемся что наши тесты пройдены
- <img src="https://user-images.githubusercontent.com/67123448/194768349-b242136c-7289-46d9-8b40-daf7107ac9e7.png" align="center" width="600" height="300" />
- - перейти в браузере по ссылке http://0.0.0.0:8000

#### Для запуска production версии проекта
- `make build-prod` билдим наш docker-compose файл
- `make up-prod` поднимаем наш контейнер со всеми зависимыми сервисами в docker-compose файле
- `make login-prod` заходим в работающий контейнер
- `pytest` выполняем команду в контейнере для прогона тестов
- Убеждаемся что наши тесты пройдены
- <img src="https://user-images.githubusercontent.com/67123448/194768404-23240c33-e8b7-485a-8f3e-5e9bface95d3.png" align="center" width="600" height="300" />
- перейти в браузере по ссылке http://0.0.0.0:1337

#### Для запуска production версии проекта на alpine
- `make build-prod-alpine` билдим наш docker-compose файл
- `make up-prod-alpine` поднимаем наш контейнер со всеми зависимыми сервисами в docker-compose файле
- `make login-prod-alpine` заходим в работающий контейнер
- `pytest` выполняем команду в контейнере для прогона тестов
- Убеждаемся что наши тесты пройдены
- <img src="https://user-images.githubusercontent.com/67123448/194768468-cd9b95c2-3a31-4a0e-9de1-6a2780959700.png" align="center" width="600" height="300" />
- перейти в браузере по ссылке http://0.0.0.0:1337
