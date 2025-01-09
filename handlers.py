# handlers.py
import random
from texts import default_template, language_mode_template
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from data_manager import (
    save_data,
    get_user_notes,
    get_flashcards,
    save_flashcards,
    delete_flashcard,
    add_flashcard_interaction,
    clear_data,
    get_conversation_history, 
    get_user_settings,
    add_conversation_turn,
    user_settings, 
)

# Persistent data file
DATA_FILE = "bot_data.json"

# Initialize the model
model = OllamaLLM(model='llama3.2:latest')
default_prompt = ChatPromptTemplate.from_template(default_template)
default_chain = default_prompt | model

# Data storage
conversation_context = {}
user_notes = {}
user_settings = {}

# Helper functions: Pass the conversion hitory as a context string 
def build_history_string(history_list):
    """Convert the conversation history into a single string."""
    history_str = ""
    for turn in history_list:
        user_text = turn.get("user", "Unknown")
        ai_text = turn.get("ai", "Unknown")
        history_str += f"\nUser: {user_text}\nAI: {ai_text}"
    return history_str

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    user_id = str(update.effective_user.id)
    conversation_context.setdefault(user_id, [])
    user_settings.setdefault(user_id, {"mode": "normal", "level": "beginner", "topic": "general"})
    await update.message.reply_text(
        "Hi! 🤖👋🤖 I am your personal productivity assistant, here to make your tasks easier and more organized."
        "If you'd like to explore all the commands and features I offer, simply type /help."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    await update.message.reply_text(
        "Here are the commands you can use, organized by category:\n\n"
        
        "📘 **General Commands:**\n"
        "/start - Start a conversation and initialize settings\n"
        "/help - Show this list of available commands\n"
        "/clear_data - Clear all saved data, including notes and flashcards\n\n"
        
        "📝 **Notes Management:**\n"
        "/note <text> - Save a note\n"
        "/shownotes - Display all saved notes\n"
        "/delete_note <index> - Delete a specific note by its index\n\n"
        
        "🌍 **Language Learning Mode:**\n"
        "/language_mode <level> <topic> - Switch to Italian language learning mode\n"
        "  - Example: /language_mode beginner travel\n"
        "/exit_language_mode - Exit Italian language learning mode and return to normal mode\n\n"
        
        "📚 **Flashcard Management:**\n"
        "/add_flashcard <Italian> <English> - Add a new flashcard for Italian to English translation\n"
        "/flashcards_study <number> - Study a specific number of random flashcards\n"
        "/show_flashcards - Show all your saved flashcards\n"
        "/delete_flashcard <Italian word> - Delete a specific flashcard by its Italian word\n"
    )

async def clear_data_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiate the data clearing process with a confirmation prompt."""
    user_id = str(update.effective_user.id)
    
    # Save that the user is being asked for confirmation
    context.user_data["clear_data_confirmation"] = True
    
    await update.message.reply_text(
        "⚠️ Are you sure you want to delete all your data? This action cannot be undone.\n"
        "This will clear all your notes and flashcards.\n\n"
        "Please type 'YES' to confirm or 'NO' to cancel."
    )

# Function to handle the user's confirmation
async def handle_clear_data_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the confirmation response for clearing all data."""
    user_id = str(update.effective_user.id)
    confirmation = update.message.text.strip().upper()
    
    # Check if the user is in the confirmation state
    if context.user_data.get("clear_data_confirmation"):
        if confirmation == "YES":
            # Clear all data and reset the confirmation state
            clear_data()
            context.user_data["clear_data_confirmation"] = False
            await update.message.reply_text("✅ All your data has been cleared.")
        elif confirmation == "NO":
            # Reset the confirmation state and cancel the operation
            context.user_data["clear_data_confirmation"] = False
            await update.message.reply_text("❌ Data clearing operation canceled.")
        else:
            # Ask again if the response is invalid
            await update.message.reply_text(
                "⚠️ Invalid response. Please type 'YES' to confirm or 'NO' to cancel."
            )
    
    else:
        # If no confirmation is required, pass control to handle_message
        await handle_message(update, context)

async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /note command."""
    user_id = str(update.effective_user.id)
    note_text = ' '.join(context.args).strip()
    if not note_text:
        await update.message.reply_text("Please provide some text after /note to save it.")
        return
    # Add note to the user's notes
    user_notes = get_user_notes(user_id)
    user_notes.append(note_text)
    save_data()  # Persist the updated data
    await update.message.reply_text(f"Note saved! You now have {len(user_notes)} notes.")

async def shownotes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /shownotes command."""
    user_id = str(update.effective_user.id)

    # Use the helper function to retrieve notes
    notes = get_user_notes(user_id)

    if not notes:
        await update.message.reply_text("You have no notes saved.")
    else:
        notes_str = "\n".join([f"{idx + 1}. {note}" for idx, note in enumerate(notes)])
        await update.message.reply_text(f"Here are your saved notes:\n{notes_str}")


async def delete_note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /delete_note command."""
    user_id = str(update.effective_user.id)
    user_notes = get_user_notes(user_id)
    if not user_notes:
        await update.message.reply_text("You have no notes to delete.")
        return
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Please provide the index of the note to delete. For example: /delete_note 1")
        return
    index = int(context.args[0]) - 1  # Convert 1-based index to 0-based
    if 0 <= index < len(user_notes):
        deleted_note = user_notes.pop(index)
        save_data()  # Persist the updated data
        await update.message.reply_text(f"Deleted note: {deleted_note}")
    else:
        await update.message.reply_text(f"Invalid index. Please provide a number between 1 and {len(user_notes)}.")

async def language_mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /language_mode command."""
    user_id = str(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text("Please specify a level and a topic. e.g.: /language_mode beginner travel")
        return
    level = context.args[0].lower()
    topic = ' '.join(context.args[1:]).lower()
    # Validate level
    if level not in ["beginner", "intermediate", "advanced"]:
        await update.message.reply_text("Level must be one of: beginner, intermediate, advanced.")
        return
    # Update and save user settings
    settings = get_user_settings(user_id)
    settings.update({"mode": "language_learning", "level": level, "topic": topic})
    save_data()
    await update.message.reply_text(
            f"🌟 Language learning mode activated! 🌟\n"
            f"Level: {level.capitalize()}\n"
            f"Topic: {topic.capitalize()}\n\n"
            "Here's how it works:\n"
            "- Send me a sentence in Italian related to this topic, and I'll correct it if there are any mistakes. "
            "Then, I'll continue the conversation in a friendly and engaging way!\n"
            "Let's get started! 😊"
    )

from data_manager import get_user_settings, save_data

async def exit_language_mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /exit_language_mode command."""
    user_id = str(update.effective_user.id)

    # Access user settings via helper
    settings = get_user_settings(user_id)

    # Check if the mode is already normal
    if settings["mode"] == "normal":
        await update.message.reply_text("You are already in the normal assistant mode!")
        return

    # Update settings and save
    settings["mode"] = "normal"
    settings["level"] = "beginner"
    settings["topic"] = "general"
    save_data()

    await update.message.reply_text(
        "You've successfully exited language learning mode. Welcome back to normal assistant mode! 😊 Let me know how I can assist you next."
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_input = update.message.text
    # Retrieve or initialize settings
    settings = get_user_settings(user_id)
    mode = settings.get("mode", "normal")
    # Generate response
    if mode == "language_learning":
        level = settings["level"]
        topic = settings["topic"]
        ai_response = model.invoke(language_mode_template.format(level=level, topic=topic, user_sentence=user_input))
    else:
        history_str = build_history_string(get_conversation_history(user_id))
        ai_response = default_chain.invoke({'context': history_str, 'question': user_input})
    # Save to conversation history
    add_conversation_turn(user_id, user_input, ai_response)
    # Send response to user
    await update.message.reply_text(ai_response)

# Flashcards Management

async def add_flashcard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /add_flashcard <Italian> <English>")
        return
    italian_word = context.args[0].strip().lower()
    english_word = " ".join(context.args[1:]).strip().lower()
    user_flashcards = get_flashcards(user_id)
    user_flashcards[italian_word] = english_word
    save_flashcards(user_id, user_flashcards)
    await update.message.reply_text(f"Flashcard added: {italian_word} -> {english_word}")

# Define conversation state for flashcard study

FLASHCARD = range(1)

async def flashcards_study_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiate flashcard study session."""
    user_id = str(update.effective_user.id)
    # Check if a session is already active
    if "flashcard_session" in context.user_data:
        await update.message.reply_text(
            "You already have an active flashcard study session. Use /cancel_flashcards_study to end it."
        )
        return ConversationHandler.END
    try:
        num_words = int(context.args[0]) if context.args else 10
    except ValueError:
        await update.message.reply_text("Please provide a valid number. Example: /flashcards_study 10")
        return ConversationHandler.END
    # Load flashcards
    flashcards = get_flashcards(user_id)
    if not flashcards:
        await update.message.reply_text("No flashcards available. Add flashcards using /add_flashcard.")
        return ConversationHandler.END
    # Select random flashcards
    selected_flashcards = random.sample(list(flashcards.items()), min(num_words, len(flashcards)))
    # Initialize session data
    context.user_data["flashcard_session"] = {
        "flashcards": selected_flashcards,
        "correct_count": 0,
        "current_index": 0,
    }
    # Start the first flashcard
    italian, english = selected_flashcards[0]
    await update.message.reply_text(f"Flashcard 1/{len(selected_flashcards)}: What does '{italian}' mean?")
    return FLASHCARD

async def handle_flashcard_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the user's response to a flashcard."""
    session = context.user_data.get("flashcard_session")
    if not session:
        await update.message.reply_text("No active flashcard study session. Use /flashcards_study to start.")
        return ConversationHandler.END
    user_response = update.message.text.strip().lower()
    user_id = str(update.effective_user.id)
    # Get the current flashcard
    italian, english = session["flashcards"][session["current_index"]]
    if user_response == english.lower():
        await update.message.reply_text("Correct! 🎉")
        session["correct_count"] += 1
        add_flashcard_interaction(user_id, {italian: english}, user_response, True)
    else:
        await update.message.reply_text(f"Wrong! The correct answer is '{english}'.")
        add_flashcard_interaction(user_id, {italian: english}, user_response, False)
    # Move to the next flashcard
    session["current_index"] += 1
    if session["current_index"] < len(session["flashcards"]):
        italian, english = session["flashcards"][session["current_index"]]
        await update.message.reply_text(
            f"Flashcard {session['current_index'] + 1}/{len(session['flashcards'])}: What does '{italian}' mean?"
        )
        return FLASHCARD
    else:
        # End the session
        correct_count = session["correct_count"]
        total = len(session["flashcards"])
        del context.user_data["flashcard_session"]
        await update.message.reply_text(f"Study session complete! You got {correct_count}/{total} correct.")
        return ConversationHandler.END

async def cancel_flashcards_study(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the flashcard study session."""
    if "flashcard_session" in context.user_data:
        del context.user_data["flashcard_session"]
        await update.message.reply_text("Flashcard study session canceled.")
    else:
        await update.message.reply_text("No active flashcard study session to cancel.")
    return ConversationHandler.END


async def show_flashcards_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all flashcards for the user."""
    user_id = str(update.effective_user.id)
    flashcards = get_flashcards(user_id)

    if not flashcards:
        await update.message.reply_text("You have no flashcards saved. Add some using /add_flashcard <Italian> <English>.")
        return

    # Format the flashcards for display
    flashcards_str = "\n".join([f"{idx + 1}. {italian} -> {english}" for idx, (italian, english) in enumerate(flashcards.items())])
    await update.message.reply_text(f"Here are your flashcards:\n{flashcards_str}")

async def delete_flashcard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /delete_flashcard <Italian word>")
        return
    italian_word = context.args[0].strip().lower()
    user_flashcards = get_flashcards(user_id)
    if italian_word in user_flashcards:
        del user_flashcards[italian_word]
        save_flashcards(user_id, user_flashcards)
        await update.message.reply_text(f"Flashcard '{italian_word}' has been deleted.")
    else:
        await update.message.reply_text(f"Flashcard '{italian_word}' not found.")
