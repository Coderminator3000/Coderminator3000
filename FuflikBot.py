import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

BOT_TOKEN = '8694790951:AAF0xOIB0IXJlGdZsF9gPGyB-98pFZXMSHw'
GEMINI_API_KEY = 'AIzaSyDYQtNOpyyANuIq8hje0FVJDDokSp9Cn7I'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    timeout = aiohttp.ClientTimeout(total=30)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=body) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    return f"Ошибка API: {resp.status}"
    except asyncio.TimeoutError:
        return "Таймаут запроса."
    except Exception as e:
        return f"Ошибка: {e}"

@dp.message(F.text.startswith('.ai '))
async def handle_ai(message: Message):
    prompt = message.text[4:].strip()
    print(f"Запрос: {prompt}")
    await bot.send_chat_action(message.chat.id, "typing")
    reply = await ask_gemini(prompt)
    await message.reply(reply)

async def main():
    print("Бот запускается... 🚀")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот выключен.")
