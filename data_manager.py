import os
import json

# Persistent data file
DATA_FILE = "bot_data.json"

# Data storage
conversation_context = {}
user_notes = {}
user_settings = {}
flashcards = {}

def load_data():
    """Load conversation_context, user_notes, user_settings, and flashcards from a JSON file."""
    global conversation_context, user_notes, user_settings, flashcards

    if os.path.exists(DATA_FILE):
        print(f"Loading data from {DATA_FILE}...")
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            conversation_context = data.get("conversation_context", {})
            user_notes = data.get("user_notes", {})
            user_settings = data.get("user_settings", {})
            flashcards = data.get("flashcards", {})

    else:
        print(f"{DATA_FILE} does not exist. Initializing empty data.")
        conversation_context = {}
        user_notes = {}
        user_settings = {}
        flashcards = {}


def save_data():
    """Save conversation_context, user_notes, user_settings, and flashcards to a JSON file."""
    data = {
        "conversation_context": conversation_context,
        "user_notes": user_notes,
        "user_settings": user_settings,
        "flashcards": flashcards,
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=3)

def add_conversation_turn(user_id, user_input, ai_response):
    """Add a conversation turn to the history."""
    if user_id not in conversation_context:
        conversation_context[user_id] = []  # Ensure user history exists
    conversation_context[user_id].append({"user": user_input, "ai": ai_response})
    save_data()


def clear_data():
    """Clear all in-memory data."""
    global conversation_context, user_notes, user_settings, flashcards
    conversation_context.clear()
    user_notes.clear()
    user_settings.clear()
    flashcards.clear()
   # save_data()

def get_user_settings(user_id):
    """Retrieve or initialize settings for a specific user."""
    if user_id not in user_settings:
        user_settings[user_id] = {"mode": "normal", "level": "beginner", "topic": "general"}
        save_data()
    return user_settings[user_id]


def get_conversation_history(user_id):
    """Retrieve the conversation history for a specific user."""
    return conversation_context.setdefault(user_id, [])

def get_user_notes(user_id):
    """Get notes for a specific user."""
    return user_notes.setdefault(user_id, [])

def add_user_note(user_id, note):
    """Add a note for a specific user."""
    notes = get_user_notes(user_id)
    notes.append(note)
    save_data()

def delete_user_note(user_id, index):
    """Delete a note by index for a specific user."""
    notes = get_user_notes(user_id)
    if 0 <= index < len(notes):
        deleted_note = notes.pop(index)
        save_data()
        return deleted_note
    return None

def get_flashcards(user_id):
    """Retrieve or initialize flashcards for a specific user."""
    return flashcards.setdefault(user_id, {})

def save_flashcards(user_id, updated_flashcards):
    """Save updated flashcards for a specific user."""
    flashcards[user_id] = updated_flashcards
    save_data()

def add_flashcard(user_id, italian, english):
    """Add a flashcard for a specific user."""
    flashcards = get_flashcards(user_id)
    flashcards[italian] = english
    save_data()

def delete_flashcard(user_id, italian):
    """Delete a specific flashcard for a user."""
    flashcards = get_flashcards(user_id)
    if italian in flashcards:
        del flashcards[italian]
        save_data()
        return True
    return False

def add_flashcard_interaction(user_id, flashcard, user_response, correct):
    """Log a flashcard interaction."""
    history = get_conversation_history(user_id)
    interaction = {
        "flashcard": flashcard,
        "user_response": user_response,
        "correct": correct,
    }
    history.append({"type": "flashcard", **interaction})
    save_data()
