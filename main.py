import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Keefe English Tutor.\n\n"
        "Я помогу тебе изучать английский с нуля.\n\n"
        "Команды:\n"
        "/lesson — начать урок\n"
        "/help — помощь\n\n"
        "Напиши любое английское слово или предложение."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — начать\n"
        "/lesson — начать урок\n"
        "/help — помощь\n\n"
        "Также можешь просто отправлять сообщения."
    )


async def lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Урок 1 — знакомство\n\n"
        "Переведи на английский:\n\n"
        "«Меня зовут Руди. Я хочу изучать английский каждый день.»\n\n"
        "Напиши свой вариант."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text in ["hello", "hi", "hey"]:
        answer = (
            "Good! Let's practice English.\n\n"
            "Question: How are you today?"
        )

    elif "my name is" in text:
        answer = (
            "Good sentence!\n\n"
            "Now try:\n"
            "Where are you from?"
        )

    elif text in ["yes", "no"]:
        answer = (
            "Good! Now make a complete sentence using "
            "your answer."
        )

    elif len(text.split()) <= 2:
        answer = (
            "Good word!\n\n"
            "Try to make a sentence with it."
        )

    else:
        answer = (
            "Good attempt!\n\n"
            "Let's continue practicing.\n\n"
            "Write another sentence in English."
        )

    await update.message.reply_text(answer)


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
