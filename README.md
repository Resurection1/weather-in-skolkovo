## Weather-in-skolkovo - данная программа позволяет узнавать температуру в районе Сколтеха и делать выгрузки последних 10 записей из базы данных


## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Resurection1/weather-in-skolkovo.git
```
```
cd weather-in-skolkovo
```
* Если у вас Linux/macOS
    ```
    python3 -m venv env
    ```

    ```
    source env/bin/activate
    ```

* Если у вас Windows
    ```
    python -m venv env
    ```

    ```
    source env/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

## Запуск программы

```
python main.py
```

Команда на получение .xlsx файла
```
python main.py export
```

## Технологический стек

Для разработки этого проекта использовались следующие технологии:

- **Python**: Основной язык программирования для бизнес-логики и взаимодействия с базой данных.
- **SQLite**: Встроенная реляционная база данных, используемая в качестве хранилища данных проекта.
- **RESTful API**: Проектирование и разработка API с учетом принципов REST для обеспечения эффективного взаимодействия клиентов с сервером.

### Автор
[Podzorov Mihail] - https://github.com/Resurection1