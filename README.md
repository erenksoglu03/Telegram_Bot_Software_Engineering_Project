# Telegram Bot Project: README

## Overview

This project is a Telegram bot built with Python, designed to enhance productivity and support language learning. It provides features like note management, flashcard-based learning, and an interactive Italian language-learning mode. The bot utilizes the Telegram Bot API along with additional Python libraries to deliver these functionalities.

---

## Features

1. **Notes Management**:

   - Save, view, and delete personal notes.

2. **Flashcard System**:

   - Create, study, and delete flashcards for language learning.

3. **Language Learning Mode**:

   - Practice Italian with real-time corrections and tailored feedback based on your proficiency level.

4. **General Commands**:

   - Explore bot functionalities using `/help` and other commands.

---

## Requirements

1. **Python Version**:

   - Python 3.8 or later is required.

2. **Libraries**:

   - python-telegram-bot>=20.0
   - langchain>=0.0.90
   - ollama>=0.1.0
   - python-dotenv>=0.21.0
   - python-telegram-bot>=21.9
   - langchain-ollama>=0.2.1
   - Built-in Python modules like `os`, `json`, and `random`.

3. **Telegram Bot Token**:

   - Obtain a bot token by creating a Telegram bot through [BotFather](https://core.telegram.org/bots).

---

## Installation and Setup

1. Clone the repository using Git:

   ```bash
   git clone https://github.com/erenksoglu03/Telegram_Bot_Software_Engineering_Project.git
   cd Telegram_Bot_Software_Engineering_Project
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the bot token:

   Create a .env file in the root directory of your project. Add the following line to the .env file:

   TELEGRAM_API_KEY=PLACEHOLDER_FOR_YOUR_API_KEY

   Save the file. This will securely store your API key.

5. Install and Configure Ollama:

   Install Ollama:
   ```bash
   brew install ollama
   ```

   Use the following command to locate the Ollama executable on your system:
   ```bash
   which ollama
   ```

   Copy the Ollama executable to your project repository if needed:
    ```bash
   cp ollama path/to/repository
   ```

   Start the Ollama server:
    ```bash
   ollama serve
   ```
      This will launch the Ollama server. By default, it listens on http://127.0.0.1:11434.

   Open a new terminal window or tab. Go to the project repository and activate the virtual environment again:
   
    ```bash
   cd Telegram_Bot_Software_Engineering_Project
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

   Pull the Llama model:

    ```bash
   ollama pull llama3.2:latest
   ```

6. Start the bot:

   Run the bot using the following command:

     ```bash
     python main.py
     ```

7. Prepare the persistent data file:

   - Ensure a `bot_data.json` file exists in the working directory. If it doesn’t, the bot will initialize an empty file during runtime.

---

## Running the Bot

### Preventing API Key Conflicts

To ensure the bot runs only on one device at a time for the same API key:

1. The bot checks if it is already running using a simple lock file mechanism.
2. If a second instance attempts to start with the same API key, the bot will terminate and display an error message.

This ensures that the bot operates reliably and avoids conflicts.

### Start the Bot

Run the bot using the following command:

```bash
python main.py
```

### Interact with the Bot

1. Open Telegram and start a chat with your bot.
2. Use `/start` to initialize the bot.
3. Explore commands with `/help`.

---

## Project Structure

- **`main.py`**: Entry point of the bot. Sets up handlers and launches the application.
- **`data_manager.py`**: Manages persistent data storage and retrieval.
- **`handlers.py`**: Implements the logic for all bot commands and interactions.
- **`texts.py`**: Stores response templates and language-learning content.
- **`bot_data.json`**: A JSON file used to persist user data such as notes, flashcards, and settings. It ensures that user data is saved acros
- **`requirements.txt`**: Lists the Python dependencies required to run the bot sessions.
- **`.env`**: Environment file for securely storing sensitive information like API keys.
- **`.gitignore`**: Specifies intentionally untracked files that Git should ignore.
- **`LICENSE`**: Specifies the licensing terms for using and distributing the project.
- **`README.md`**: Documentation file providing an overview and setup instructions for the project

---

## Troubleshooting

### Common Issues

1. **Bot Not Responding**:

   - Verify the bot token in `main.py`.
   - Ensure all required libraries are installed.

2. **Library Installation Errors**:

   - Update `pip` using:
     ```bash
     pip install --upgrade pip
     ```
   - Ensure Python 3.8+ is installed.

3. **JSON File Issues**:

   - If `bot_data.json` is missing, the bot will create a new file.
   - Check file permissions if data isn’t saving.

4. **API Key Conflict**:

   - Ensure only one instance of the bot is running with the same API key. Terminate duplicate processes if necessary.

---

## Customization

To extend the bot’s functionalities:

- Add new commands in `handlers.py`.
- Modify or expand persistent data logic in `data_manager.py`.
- Update templates or language content in `texts.py`.

---

## Recommendations

If you want to create the same bot with a different bot API key, you can use the /setcommands feature from **BotFather**. These commands were set for the user interface in this project:

- start: Start the bot and initialize settings.
- help: Show the list of available commands.
- language_mode: Activate Italian language learning mode. Example: /language_mode beginner travel.
- exit_language_mode: Exit Italian language learning mode and return to normal mode.
- note: Save a note. Example: /note Learn Italian daily.
- shownotes: Show all saved notes.
- delete_note: Delete a specific note by its index. Example: /delete_note 1.
- clear_data: Clear all user data (notes, flashcards, context).
- add_flashcard: Add a new flashcard. Example: /add_flashcard ciao hello.
- show_flashcards: Display all saved flashcards.
- flashcards_study: Start a flashcard study session. Example: /flashcards_study 5.
- delete_flashcard: Delete a flashcard by its Italian word. Example: /delete_flashcard ciao.


