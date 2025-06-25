
# Telegram Bot: Business Questionnaire & Calendly Booking

This is a Telegram bot that guides users through a business-related questionnaire, collects their answers, and posts the responses to a designated group chat. At the end of the flow, the user is invited to book a consultation via Calendly.

---

## ✨ Features

- 📋 Interactive questionnaire using Telegram conversation flow
- 🔒 Sensitive data stored in a `.env` file (never committed)
- 📩 Sends collected data to a specified group chat
- 📆 Allows booking a meeting through Calendly
- 🔁 Supports restarts, timeouts, and cancellations
- ☎ Accepts both typed and contact-based phone input

---

## 🧩 Bot Flow

1. User starts with `/start`
2. Bot asks for name, phone, business info, roles, and more
3. Answers are sent to a group chat for review
4. Calendly booking link is offered at the end
5. User can cancel or restart at any time

---

## 🛠 Requirements

- Python 3.8+
- Telegram bot token
- Group chat ID where data will be posted
- Calendly booking URL

---

## 📦 Installation

1. **Clone the repo**:
   ```bash
   git clone git@github.com:SergioSergSergo/Telegram_Bot_Questionnaire.git
   cd Telegram_Bot_Questionnaire
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔐 Environment Setup

Create a `.env` file in the root directory with the following content:

```env
BOT_TOKEN=your_telegram_bot_token
GROUP_CHAT_ID=-1001234567890
CALENDLY_URL=https://calendly.com/your-link
```

> ⚠️ Keep `.env` secret. It’s already in `.gitignore`.

---

## 🚀 Run the Bot

```bash
python bot.py
```

The bot will start polling Telegram for messages.


## 💡 Deployment

- Works locally or on cloud platforms like **Render**, **Heroku**, etc.
- Ensure that `render.yaml` or `Procfile` is configured for your platform
