import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai

logging.basicConfig(level=logging.INFO)

openai.api_key = "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"

bot = Bot(token="5932493765:AAEYveJzy_qeXWpXyr2Qnits94-9jgTSrNA")
dp = Dispatcher(bot)

if not os.path.exists("users"):
    os.mkdir("users")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_message(message: types.Message):
    if f"{message.chat.id}.txt" not in os.listdir("users"):
        with open(f"users/{message.chat.id}.txt", "x") as f:
            f.write("")

    with open(f"users/{message.chat.id}.txt", "r", encoding="utf-8") as file:
        oldmes = file.read()

    if message.text == "/clear":
        with open(f"users/{message.chat.id}.txt", "w", encoding="utf-8") as file:
            file.write("")
        return await bot.send_message(chat_id=message.chat.id, text="История очищена!")

    try:
        send_message = await bot.send_message(chat_id=message.chat.id, text="Обрабатываю запрос, пожалуйста подождите!")
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            temperature=0.9,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["You:"]
        )

        await bot.edit_message_text(
            text=completion.choices[0].text,
            chat_id=message.chat.id,
            message_id=send_message.message_id,
        )

        with open(f"users/{message.chat.id}.txt", "a+", encoding="utf-8") as file:
            file.write(
                message.text.replace("\n", " ")
                + "\n"
                + completion.choices[0].text.replace("\n", " ")
                + "\n"
            )

        with open(f"users/{message.chat.id}.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()



    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text=str(e))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
