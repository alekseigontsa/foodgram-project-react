# Fooodgram by Aleksei Gontsa

admin admin<br>
http://???/redoc/<br>
http://???/admin/<br>

![example workflow](https://github.com/alekseigontsa/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

**foodgram - сервис «Продуктовый помощник».**<br>
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд..<br>

Сервис позволяет отправлять запросы GET, POST, DELETE, PATCH для добавления, изменения и удаления рецептов.<br>
Для добавления рецептов необходимо зарегистрироваться с изпользванием почты.<br>
<hr>

### Технологиии, реализованные в проекте

Сервис api реализован при помощи библиотеки rest_framework.

#### Для работы с проектом:  
1. Скачайте репозиторий.
2. Запустите контейнер командой sudo docker-compose up --build
3. Выполните команды:
  - docker-compose exec web python manage.py createsuperuser
<hr>

#### Примеры запросов:
* Регистрация "POST": `</api/auth/signup/>`<br>
* Получение токена "POST": `</api/auth/token/>`<br>
* Получить данные о себе "GET": `</api/users/me/>`<br>
* Получить все рецепты или выбрать конкретной "GET": `</api/recipe/<recipe_id>/>`<br>


#### Об авторах.<br>
**Студент Яндекс.Практикум**<br>
Гонца Алексей<br>
[DockerHub](https://hub.docker.com/u/alexgon354)<br>

