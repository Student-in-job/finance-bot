# 🤖 Telegram Finance Bot (AI-Powered)

## 🚀 Setup Guide
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env` with your API keys and Postgres URL.
3. Seed the `categories` table in your database.
4. Run `python main.py`.
5. Authenticate in Telegram with `/auth <your_pin>`.

Certainly! Updating your **README.md** to include these specific setup instructions is vital for a smooth "first-run" experience. I have refined the instructions to cover both the technical environment and the external API registrations.

### Updated README.md Section

```markdown
## 🛠️ Step-by-Step Setup Guide

### 1. Register your Telegram Bot
1. Open Telegram and search for **@BotFather**.
2. Send the command `/newbot` and follow the instructions to name your assistant.
3. Once created, @BotFather will provide an **API Token**. 
4. Copy this token; you will need it for your `.env` file.
5. **Note**: If you plan to use the bot in a Channel, add it as an Administrator with "Post Messages" permissions.

### 2. Obtain your Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google Account.
3. Click on the **"Get API key"** button in the top left sidebar.
4. Select **"Create API key in new project"**.
5. Copy the generated key; this is your `GEMINI_API_KEY`.

### 3. Environment Preparation
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd telegram_fin_bot
   
```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   
```
3. **Configure Secrets**:
   Copy `.env.example` to a new file named `.env` and fill in your keys[cite: 12]:
   ```env
   TELEGRAM_TOKEN=your_telegram_token
   GEMINI_API_KEY=your_gemini_key
   DATABASE_URL=postgresql://user:password@localhost:5432/finance_db
   ADMIN_SECRET_PIN=123456
   
```

### 4. Database Initialization (Migrations)
Since this project uses Alembic for version control, do not use manual table creation[cite: 12]. 
Run the following to create tables and seed your 18 categories[cite: 12]:
```bash
alembic upgrade head
```

### 5. Start the Bot
```bash
python main.py
```

### 6. Final Authentication
Once the bot is running, open it in Telegram and send:
`/auth 123456` (Replace with your chosen PIN)
This will register your Telegram ID as an Admin in the database[cite: 10].
```