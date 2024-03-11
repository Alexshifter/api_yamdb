### Описание:

Портал для публикации/просмотра/комментирования постов с настроенным API.

Автор проекта: [Vardemson](https://github.com/VardDemson)

### Используемые технологии:

* Python 3.9,
* Django,
* DjangoRestFramework,
* Djoser
* JWT

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/VardDemson/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Посмотреть всю документацию для API можно по адресу:

http://127.0.0.1:8000/redoc/

### Примеры запросов к API:
Пример ответа получения всех опубликованных постов по URL:

```
http://127.0.0.1:8000/api/v1/posts/
```

![Пример ответа получения всех опубликованных постов по URL http://127.0.0.1:8000/api/v1/posts/.](/images/Postman_posts_requests.png)

Пример ответа получения всех подписок пользователя по URL:

```
http://127.0.0.1:8000/api/v1/follow/
```

![Пример ответа получения всех подписок пользователя по URL http://127.0.0.1:8000/api/v1/follow/.](/images/Postman_follow_requests.png)
