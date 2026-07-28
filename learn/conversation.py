from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Define states
NAME, AGE, CONFIRM = range(3)

# --- Handlers for each step ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi! What's your name?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text(f"Nice to meet you, {update.message.text}! How old are you?")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["age"] = update.message.text
    await update.message.reply_text(
        f"Name: {context.user_data['name']}, Age: {context.user_data['age']}. Confirm? (yes/no)"
    )
    return CONFIRM

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == "yes":
        await update.message.reply_text("Saved! Session complete.")
    else:
        await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Conversation cancelled.")
    return ConversationHandler.END

# --- Build the app ---

def main():
    app = Application.builder().token("8814922990:AAELLZQXf0nruv_rV-o6jIiHXxU6hRRL_q8").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("hi", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()