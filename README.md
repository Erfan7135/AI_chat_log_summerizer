# Chat Log Analyzer

## Overview
Chat Log Analyzer is a Python script designed to process chat log files, extract messages, perform statistical and keyword analysis, and generate summaries. It uses NLTK for natural language processing and scikit-learn for TF-IDF analysis to identify key topics and terms in conversations.

## Features
- **Message Parsing**: Reads chat logs and separates messages by speaker (User or AI).
- **Statistics**: Counts total messages, user messages, and AI messages.
- **Keyword Analysis**: Identifies frequently used words, excluding stop words and non-alphabetic terms.
- **TF-IDF Analysis**: Computes TF-IDF scores to rank important words in the conversation.
- **Summary Generation**: Creates a summary file with key statistics and the top 5 keywords.

## Requirements
- Python 3.6+
- Required Python packages:
  - `nltk`
  - `scikit-learn`
- NLTK data:
  - `stopwords`
  - `punkt_tab`

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Erfan7135/AI_chat_log_summerizer
   cd AI_chat_log_summerizer
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install nltk scikit-learn
   ```

4. **Download NLTK Data**:
   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('punkt_tab')
   ```

## Usage
1. **Prepare Chat Logs**:
   - Place your chat log files (`.txt`) in a `logs/` directory in the project root.
   - Each log file should follow a format where messages start with `User:` or `AI:`, followed by content (potentially spanning multiple lines).

2. **Run the Script**:
   ```bash
   python .\src\chat_analyzer.py
   ```
   - The script processes all `.txt` files in the `logs/` directory.
   - Summaries are saved as `_summary.txt` files in an `output/` directory.

3. **Example Chat Log Format** (`logs/chat1.txt`):
   ```
   User: Hi, can you tell me about Python?
   AI: Sure! Python is a popular programming language known for its readability.
   User: What can I use it for?
   AI: You can use Python for web development, data analysis, AI, and more.
   ```

4. **Output**:
   - For each input file (e.g., `logs/chat1.txt`), a summary file (e.g., `output/chat1_summary.txt`) is generated with:
     - Total number of exchanges.
     - A simple summary based on the top keyword.
     - Top 5 keywords.

   **Example Summary** (`output/chat1_summary.txt`):
   ```
   The Conversation had 4 exchanges.
   This conversation is about python.
   Most common keywords: python, use, web, development, data
   ```

## Project Structure
```
AI_CHAT_LOG_SUMMERIZER/
├── logs/                  # Directory for input chat log files
├── output/                # Directory for generated summary files
├── src/chat_analyzer.py       # Main Python script
└── README.md              # This file
```

## Notes
- Ensure the `logs/` and `output/` directories exist in the project root. The script does not create them automatically.
- The script assumes UTF-8 encoded text files. Modify the encoding in the `parse_chat` function if needed.
- The summary generation is basic and uses the top keyword. For more advanced summaries, consider integrating a language model API.
- Custom stop words (e.g., "hi", "hello") are included to filter common conversational terms.

