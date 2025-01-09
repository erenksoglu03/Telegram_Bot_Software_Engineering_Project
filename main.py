from telegram.ext import Application, CommandHandler, MessageHandler, filters, Defaults, ConversationHandler
from data_manager import load_data
from dotenv import load_dotenv
import os
from handlers import (
    start_command,
    help_command,
    note_command,
    shownotes_command,
    delete_note_command,
    clear_data_command,
    handle_clear_data_confirmation,
    language_mode_command,
    exit_language_mode_command,
    add_flashcard_command,
    flashcards_study_command,
    handle_flashcard_response, 
    cancel_flashcards_study,
    show_flashcards_command,
    delete_flashcard_command,
    handle_flashcard_response,
    cancel_flashcards_study,
    handle_message,
)

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TELEGRAM_API_KEY")
if not TOKEN:
    raise ValueError("Missing TELEGRAM_API_KEY in .env file")

# BOT_USERNAME = '@Soft_Eng_Project_Bot'
FLASHCARD = range(1)


flashcards_handler = ConversationHandler(
    entry_points=[CommandHandler("flashcards_study", flashcards_study_command)],
    states={
        FLASHCARD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_flashcard_response)],
    },
    fallbacks=[CommandHandler("cancel_flashcards_study", cancel_flashcards_study)],
)


def main():
    """Start the Telegram bot."""
    print("Starting Telegram bot...")
    load_data()

    # Create the application
    app = Application.builder().token(TOKEN).defaults(Defaults()).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("note", note_command))
    app.add_handler(CommandHandler("shownotes", shownotes_command))
    app.add_handler(CommandHandler("delete_note", delete_note_command))
    app.add_handler(CommandHandler("clear_data", clear_data_command)) 
    app.add_handler(CommandHandler("language_mode", language_mode_command))
    app.add_handler(CommandHandler("exit_language_mode", exit_language_mode_command))
    app.add_handler(CommandHandler("add_flashcard", add_flashcard_command))
    app.add_handler(CommandHandler("show_flashcards", show_flashcards_command))
    app.add_handler(CommandHandler("delete_flashcard", delete_flashcard_command))
    app.add_handler(flashcards_handler)
    
    # Message handler for confirmation and regular messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_clear_data_confirmation))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is polling for updates. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
