import aiohttp
import asyncio
import aiosqlite
import openpyxl
from datetime import datetime
import sys

API_URL = ("https://api.open-meteo.com/v1/forecast"
           "?latitude=55.698&longitude=37.356&current_weather=true")
DB_NAME = "weather.db"
EXPORT_INTERVAL = 180  # Интервал в секундах (3 минуты)


def convert_wind_direction(degrees):
    """Преобразование направления ветра из градусов в буквенное обозначение."""
    directions = ["С", "ССВ", "СВ", "ВВС", "В", "ВЮВ", "ЮВ", "ЮЮВ",
                  "Ю", "ЮЮЗ", "ЮЗ", "ЗЮЗ", "З", "ЗСЗ", "СЗ", "ССЗ"]
    idx = round(degrees / 22.5) % 16
    return directions[idx]


async def fetch_weather_data():
    """Функция для получения данных о погоде через API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            data = await response.json()
            weather_data = {
                "temperature": data['current_weather']['temperature'],
                "wind_speed": data['current_weather']['windspeed'],
                "wind_direction": (convert_wind_direction(
                    data['current_weather']['winddirection'])),
                "timestamp": datetime.now().strftime('%Y.%m.%d %H:%M')
            }
            return weather_data


async def save_to_database(weather_data):
    """Сохранение данных о погоде в базу данных."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS weather_data ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "temperature REAL, "
            "wind_speed REAL, "
            "wind_direction TEXT, "
            "timestamp TEXT)"
        )
        await db.execute(
            "INSERT INTO weather_data "
            "(temperature, wind_speed, wind_direction, timestamp) "
            "VALUES (?, ?, ?, ?)",
            (
                weather_data["temperature"], weather_data["wind_speed"],
                weather_data["wind_direction"], weather_data["timestamp"]
            )
        )
        await db.commit()


async def export_to_excel():
    """Экспорт данных о погоде в файл Excel."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
                "SELECT * FROM weather_data ORDER BY id DESC LIMIT 10"
        ) as cursor:
            rows = await cursor.fetchall()

            # Создаем новый Excel файл
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Weather Data"

            # Добавляем заголовки
            headers = [
                "ID", "Temperature (°C)", "Wind Speed (m/s)",
                "Wind Direction", "Timestamp"]
            ws.append(headers)

            # Добавляем строки с данными
            for row in rows:
                ws.append(row)

            # Сохраняем Excel файл в текущую папку
            file_name = ("weather_data_"
                         f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
            wb.save(file_name)

            print(f"Данные экспортированы в {file_name}")


async def main():
    """Основная функция для запуска периодического запроса погоды."""
    while True:
        # Запрашиваем данные о погоде
        weather_data = await fetch_weather_data()

        # Сохраняем данные в базу
        await save_to_database(weather_data)

        # Ожидаем перед следующим запросом
        await asyncio.sleep(EXPORT_INTERVAL)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    if len(sys.argv) > 1 and sys.argv[1] == "export":
        # Если передана команда "export", выполняем экспорт в Excel
        loop.run_until_complete(export_to_excel())
    else:
        # Если команда не передана, запускаем сбор данных о погоде
        loop.run_until_complete(main())
