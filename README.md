# **TechDigest_bot**


### What king of bot is this?

TechDigest Bot is your personal AI assistant for tracking tech news. It automatically gathers, filters, and sends the most important news from your area of interest.

This is a bot that:

- You can find articles for every taste daily

- Sort articles and choose only the most interesting and fresh ones

- Send them at any time convenient for you

## How should the bot work?

### Start the bot

### 1. When the /start button is pressed, the bot greets the user and records them in the database, after which it explains what it can do.

### 2. The user sets their interests (separated by commas)
Example:
[User writes to the bot]👤: 
/start

🤖: Hi! I'm your personal tech news curator!

What I can do:
- Gather news from Reddit, Hacker News, Habr
- Filter by your interests using AI
- Send a digest every morning

Let's set up your interests!
Write the technologies you're interested in, separated by commas:

Example: Python, Machine Learning, Web Development, DevOps

### 3. After the user enters their interests, the bot saves them in the database (PostgreSQL)

### 4. The bot prompts the user to choose a time when it will send notifications

## Daily interaction

### 5. Every day, at the time specified by the user, the bot will send filtered articles and provide statistics.
Example:
🤖: 🚀 Your Tech Digest for January 15:

📊 Collection Stats:
• Collected: 147 articles
• Filtered: 23 articles  
• Best: 5 articles

🔥 Top News:

1. 📚 Python 3.14 Release 
   New pattern matching features, performance improvements
   [Read](https://example.com)

2. ⚡OpenAI GPT-5 Announcement
   Breakthrough in generative AI, new capabilities
   [Read](https://example.com)

3. 📰 Django 5.0 Released
   Full async support, new ORM features
   [Read](https://example.com)

4. 🔬 New ML Research Paper
   Transformers for code generation, SOTA results
   [Read](https://example.com)

5. 🦀 Rust 1.70 Performance
   Compiler improvements, 15% speed boost
   [Read](https://example.com)

## Management and Settings (Button: interests)

### 6. After selecting a button, the bot will display the current interests and suggest one of the following actions:
- /edit - Edit all interests
- /add - Add interest
- /remove - Delete interest
- /back - return to main menu

### 7. After successfully editing the interests - the bot sends the message:
Example:
👤: /edit
🤖: Enter new interests separated by commas:

Current: Python, AI, Data Science, Backend development

👤: Python, Machine Learning, Web Development, Cloud, DevOps

🤖: Interests updated:
- Python
- Machine Learning
- Web Development
- Cloud
- DevOps

Changes will take effect from the next digest

## Testing and debugging
👤: /test

🤖: 🔍 Starting test collection...

Collecting articles...
Reddit: 45 articles
Hacker News: 32 articles
RSS: 28 articles

Filtering...
Quick filter: 18 articles
AI ranking: 5 articles

Test results:
- Total collected: 105 articles
- After filters: 5 articles

## Errors or unexpected situations

# Problems with sources:
🤖: Attention!

Failed to retrieve data from:
- Hacker News (timeout)

But don't worry! The digest has been compiled from other sources:
- Reddit: 38 articles
- RSS: 24 articles

Total number of articles: 62
Quality: slightly reduced

## Empty digest
🤖: There are no new articles today matching your interests

Possible reasons:
- It's a day off (fewer publications)
- Filters are too strict
- Problems with sources


### Tech stack

### Backend & core
- Python 3.11+ - Main language
- PostgreSQL - Database
- aiogram x3.0 - Telegram Bot API

**OPRIONAL**
- Docker - containerization

### News Sources & APIs
- Reddit API
- RSS
- Telegram Bot API(aiogram)


## Environment variables
- BOT_TOKEN=your_telegram_token
- DATABASE_URL=postgresql://user:pass@host/db
- REDDIT_CLIENT_ID=...
- REDDIT_CLIENT_SECRET=...


## 🧑‍💻 Author
Laurenz — [GitHub Profile](https://github.com/1Laurenz1)

## 📄 License
MIT License © 2025 Laurenz