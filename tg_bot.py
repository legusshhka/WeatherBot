import asyncio
import logging
import requests
import datetime
from config import tg_token, weather_token
from aiogram import Bot, Dispatcher, types

bot = Bot(token=tg_token)
dp = Dispatcher()

@dp.message()
async def weahter(message: types.Message):
    if message.text == "/start":
        await message.answer(text="Привет! Напиши мне название города, а я отправлю тебе сводку погоды на сегодня!")
    else:
        smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U0001F327",
            "Drizzle": "Моросящий дождь \U0001F327",
            "Thunderstorm": "Гроза \U000026C8",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"

        }
        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric"
            )
            data = r.json()

            temp = data["main"]["temp"]
            feels_temp = data["main"]["feels_like"]

            weather_discription = data["weather"][0]["main"]
            if weather_discription in smile:
                wd = smile[weather_discription]
            else:
                wd = ""

            pressure = data["main"]["pressure"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

            await message.reply(f"\U0001F5D3{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\U0001F5D3\n"
              f"\U0001F4CCПогода\U0001F4CC\n"
              f"\U0001F4CDГород: {message.text}\n"
              f"{wd}\n"
              f"\U0001F321Температура: {temp}°C(Ощущается как: {feels_temp}°C)\n"
              f"\U00002696Давление: {pressure} мм.рт.ст\n"
              f"\U0001F4A7Влажность воздуха: {humidity}%\n"
              f"\U0001F32CСкорость ветра: {wind} м/c\n"
              f"\U0001F305Восход: {sunrise}\n"
              f"\U0001F307Закат: {sunset}\n"
              f"Удачного дня!")

        except Exception as ex:
            await message.reply("Неверно введён город или превышено время ожидания")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



