# api_yatube
Проект Яндекс Практикум
---

## Запуск проекта
1. Клонируйте репозиторий:

    ```bash
    git clone git@github.com:AliceATG/api_final_yatube.git
    cd api_final_yatube
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv env
    source env/Scripts/activate
    ```

3. Установите зависимости:

    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. Выполните миграции:

    ```bash
    python manage.py migrate
    ```

5. Запустите сервер:

    ```bash
    python manage.py runserver
    ```

---

## Пример запросов

### Получить список всех постов:

**GET-запрос**:

```http
http://127.0.0.1:8000/api/v1/posts/
