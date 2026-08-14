import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import AsyncOpenAI


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

ai = AsyncOpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are an English tutor inside a Telegram bot.

Your job is to teach English effectively.

The student's native language is Russian.

Rules:
1. Communicate mainly in English.
2. If the student seems confused, explain briefly in Russian.
3. Correct important grammar, vocabulary and word-order mistakes.
4. Do not simply give the correct answer. Explain the mistake briefly.
5. Give one small follow-up exercise when useful.
6. Adapt difficulty to the student's apparent level.
7. Start around A1-A2 if the level is unknown.
8. Be concise and practical.
9. Encourage the student to produce English themselves.
10. Never overwhelm the student with long grammar lectures.

When correcting an answer, use this structure when appropriate:

Correction:
...

Why:
...

Try:
...

The goal is gradual improvement, not just conversation.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Keefe English Tutor.\n\n"
        "Я помогу тебе изучать английский с нуля.\n\n"
        "Напиши любое предложение на английском "
        "или просто напиши: «Начать урок»."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — начать\n"
        "/lesson — начать урок\n"
        "/help — помощь\n\n"
        "Также просто отправляй мне сообщения на английском."
    )


async def lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Первое задание:\n\n"
        "Translate into English:\n"
        "«Меня зовут Руди. Я хочу изучать английский каждый день.»\n\n"
        "Напиши свой вариант."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = await ai.responses.create(
            model="gpt-5.5",
            instructions=SYSTEM_PROMPT,
            input=user_text,
        )

        answer = response.output_text

        await update.message.reply_text(answer)

    except Exception as error:
        print("AI ERROR:", error)
        await update.message.reply_text(
            "Произошла ошибка соединения с ИИ. Попробуй ещё раз."
        )


def main():
    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("lesson", lesson))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("Keefe English Bot started.")

    app.run_polling()


if __name__ == "__main__":
    main()
