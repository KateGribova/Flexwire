# FLEXWIRE

- Ссылка на Github Gist с парсером для фикстур:
[Генерация фикстур](https://gist.github.com/Arseniks/09cd42e1bb671be9f7402d01162b36da)

## Запуск проекта
- Клонируйте проект с GitHub с помощью команды:
```
git clone https://github.com/Arseniks/flexwire
```
- Перейдите в папку с проектом:
```
cd flexwire
```
### На Windows
- Скопируйте файл .env.template в .env, при необходимости отредактируйте 
  значения переменных:
```
copy .env.template .env
``` 
- Установите и активируйте виртуальное окружение с помощью команд:
```
python -m venv venv
``` 
```
venv\Scripts\activate.bat
``` 
- Установите необходимые вам зависимости
Для основных зависимостей из файла requirements.txt:
```
pip install -r requirements/requirements.txt
``` 
- Для разработки нужно также установить зависимости из файла requirements_dev.
txt:
```
pip install -r requirements/requirements_dev.txt
``` 
- А для тестирования нужно установить зависимости из файла requirements_test.
  txt:
```
pip install -r requirements/requirements_test.txt
```
В папке с файлом manage.py выполните команды:
- Установки миграций БД:
```
python manage.py migrate
```
- Заполнения БД данными из фикстуры:
```
python manage.py loaddata fixtures/roles_data.json
```
```
python manage.py loaddata fixtures/languages_data.json
```
```
python manage.py loaddata fixtures/technologies_data.json
```
- Запуска проекта:
```
python manage.py runserver
```
### На Linux/MAC
- Скопируйте файл .env.template в .env, при необходимости отредактируйте 
  значения переменных:
```
cp .env.template .env
``` 
- Установите и активируйте виртуальное окружение с помощью команд:
```
python3 -m venv venv
``` 
```
source venv/bin/activate
``` 
- Установите необходимые вам зависимости
Для основных зависимостей из файла requirements.txt:
```
pip3 install -r requirements/requirements.txt
``` 
- Для разработки нужно также установить зависимости из файла requirements_dev.txt:
```
pip3 install -r requirements/requirements_dev.txt
``` 
- А для тестирования нужно установить зависимости из файла requirements_test.txt:
```
pip3 install -r requirements/requirements_test.txt
```
В папке с файлом manage.py выполните команды:
- Установки миграций БД:
```
python3 manage.py migrate
``````
- Заполнения БД данными из фикстуры:
```
python3 manage.py loaddata fixtures/roles_data.json
```
```
python3 manage.py loaddata fixtures/languages_data.json
```
```
python3 manage.py loaddata fixtures/technologies_data.json
```
- Запуска проекта:
```
python3 manage.py runserver
```