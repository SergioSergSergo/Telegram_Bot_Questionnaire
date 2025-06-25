
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, 
    ConversationHandler, ContextTypes, CallbackQueryHandler, filters
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove,  KeyboardButton
from telegram.ext import ContextTypes
from pathlib import Path
from telegram.ext import ContextTypes
from enum import Enum, auto

async def timeout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text(
            "⏰ Ви не відповідали протягом 30 хвилин. Сесію завершено.\n"
            "Натисніть /start, щоб почати спочатку."
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "⏰ Ви не відповідали протягом 30 хвилин. Сесію завершено.\n"
            "Натисніть /start, щоб почати спочатку."
        )
    return ConversationHandler.END

class Questions:
    NAME = "Як я можу до вас звертатися?"
    PHONE = "Особистий номер телефону:"
    BUSINESS = "Короткий опис вашого поточного або  майбутнього бізнесу (назва, ніша, рік заснування):"
    WEBSITE = "Сайт та соцмережі вашого бізнесу:"
    EMPLOYEES = "Кількість працівників:"
    LEGAL_FORM = "Форма діяльності:"
    ROLES = "Які ролі ви виконуєте в бізнесі?"
    FIN_KNOWLEDGE = "Чи розумієте ви різницю між P&L та Cash Flow?"
    FIN_PERSON = "Хто з команди займається фінансовим аналізом?"
    FIN_REPORTS = "Які фінансові звіти та показники відслідковуються станом на сьогодні?"
    CRM = "Чи користуєтесь CRM системою?"
    CRM_NAME = "Якщо так, то якою CRM користуєтесь?"
    FINMAP = "Чи користуєтесь додатком Finmap?"
    GOOGLE_SHEETS = "Чи ведете фінансовий облік у Google Таблицях?"
    MEETINGS = "Чи сформований графік нарад із командою?"
    MEETING_DETAILS = "В яких ключових нарадах приймаєте участь?"
    REQUESTS = "Детально опишіть запити, які спонукали вас звернутись по консультацію/аудит/фін.модель:"
    USED_CONSULTANTS = "Чи користувались ви раніше послугами фінансових консультантів?"
    FORMAT = "Бажаний формат проведення зустрічі:"
    REFERRAL = "Як ви дізнались про мене?"
    CONFIRM = "Перевірте свої відповіді"

class States(Enum):
    NAME = auto()
    PHONE = auto()
    BUSINESS = auto()
    WEBSITE = auto()
    EMPLOYEES = auto()
    LEGAL_FORM = auto()
    ROLES = auto()
    FIN_KNOWLEDGE = auto()
    FIN_PERSON = auto()
    FIN_REPORTS = auto()
    CRM = auto()
    CRM_NAME = auto()
    FINMAP = auto()
    GOOGLE_SHEETS = auto()
    MEETINGS = auto()
    MEETING_DETAILS = auto()
    REQUESTS = auto()
    USED_CONSULTANTS = auto()
    FORMAT = auto()
    REFERRAL = auto()
    CONFIRM = auto()
    CALLENDLY = auto()

def build_summary_o(user_data: dict) -> str:
    lines = [
        f"{Questions.NAME}: {user_data.get(States.NAME)}",
        f"{Questions.PHONE}: {user_data.get(States.PHONE)}",
        f"{Questions.BUSINESS}: {user_data.get(States.BUSINESS)}",
        f"{Questions.WEBSITE}: {user_data.get(States.WEBSITE)}",
        f"{Questions.EMPLOYEES}: {user_data.get(States.EMPLOYEES)}",
        f"{Questions.LEGAL_FORM}: {user_data.get(States.LEGAL_FORM)}",
        f"{Questions.ROLES}: {user_data.get(States.ROLES)}",
        f"{Questions.FIN_KNOWLEDGE}: {user_data.get(States.FIN_KNOWLEDGE)}",
        f"{Questions.FIN_PERSON}: {user_data.get(States.FIN_PERSON)}",
        f"{Questions.FIN_REPORTS}: {user_data.get(States.FIN_REPORTS)}",
        f"{Questions.CRM}: {user_data.get(States.CRM)}",
        f"{Questions.CRM_NAME}: {user_data.get(States.CRM_NAME)}",
        f"{Questions.FINMAP}: {user_data.get(States.FINMAP)}",
        f"{Questions.GOOGLE_SHEETS}: {user_data.get(States.GOOGLE_SHEETS)}",
        f"{Questions.MEETINGS}: {user_data.get(States.MEETINGS)}",
        f"{Questions.MEETING_DETAILS}: {user_data.get(States.MEETING_DETAILS)}",
        f"{Questions.REQUESTS}: {user_data.get(States.REQUESTS)}",
        f"{Questions.USED_CONSULTANTS}: {user_data.get(States.USED_CONSULTANTS)}",
        f"{Questions.FORMAT}: {user_data.get(States.FORMAT)}",
        f"{Questions.REFERRAL}: {user_data.get(States.REFERRAL)}",
    ]

    # Додаємо нумерацію до кожного рядка
    numbered_lines = [f"{i+1}. {line}" for i, line in enumerate(lines)]

    return "\n\n".join(numbered_lines)

def build_summary(user_data: dict) -> str:
    fields = [
        (Questions.NAME, States.NAME),
        (Questions.PHONE, States.PHONE),
        (Questions.BUSINESS, States.BUSINESS),
        (Questions.WEBSITE, States.WEBSITE),
        (Questions.EMPLOYEES, States.EMPLOYEES),
        (Questions.LEGAL_FORM, States.LEGAL_FORM),
        (Questions.ROLES, States.ROLES),
        (Questions.FIN_KNOWLEDGE, States.FIN_KNOWLEDGE),
        (Questions.FIN_PERSON, States.FIN_PERSON),
        (Questions.FIN_REPORTS, States.FIN_REPORTS),
        (Questions.CRM, States.CRM),
        (Questions.CRM_NAME, States.CRM_NAME),
        (Questions.FINMAP, States.FINMAP),
        (Questions.GOOGLE_SHEETS, States.GOOGLE_SHEETS),
        (Questions.MEETINGS, States.MEETINGS),
        (Questions.MEETING_DETAILS, States.MEETING_DETAILS),
        (Questions.REQUESTS, States.REQUESTS),
        (Questions.USED_CONSULTANTS, States.USED_CONSULTANTS),
        (Questions.FORMAT, States.FORMAT),
        (Questions.REFERRAL, States.REFERRAL),
    ]

    numbered_lines = [
        f"{i+1}. *{question}* \n→ `{user_data.get(state, '—')}`"
        for i, (question, state) in enumerate(fields)
    ]

    return "\n\n".join(numbered_lines)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💡 *Довідка по боту EMMA Consulting*\n\n"
        "Цей бот допоможе вам пройти опитування і забронювати зустріч з фінансовим експертом.\n\n"
        "Основні команди:\n"
        "• /start — почати спілкування з ботом\n"
        "• /cancel — скасувати поточне опитування\n"
        "• /restart — почати опитування заново\n"
        "• /help — показати це повідомлення\n\n"
        "Якщо маєте питання — звертайтесь, ми завжди раді допомогти!"
        ,
        parse_mode='Markdown'
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    context.chat_data.clear()

    await update.message.reply_text(
        "❌ Опитування скасовано. Щоб почати знову, надішліть команду /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    context.chat_data.clear()
    await update.message.reply_text(
        " Ви розпочали анкету спочатку.\n\n"
        f"{Questions.NAME}",
        reply_markup=ReplyKeyboardRemove()
    )
    return States.NAME

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    # Перше — привітальне повідомлення
    await update.message.reply_text(
        f"Вітаю, {user.first_name or 'шановний користувачу'}! 👋\n\n"
        "Я — бот команди *EMMA Consulting*. Допоможу зібрати базову інформацію перед вашою зустріччю з фінансовим експертом.\n\n"
        "📋 Я поставлю вам кілька простих запитань.\n"
        "Після цього ви зможете *забронювати зручний час для онлайн-зустрічі* через Calendly 📅.\n\n"
        "ℹ️ У будь-який момент ви можете:\n"
        "•  скасувати — командою /cancel\n"
        "•  почати опитування спочатку — командою /restart\n"
        "•  перезапустити бота — командою /start\n"
        "•  отримати довідку — командою /help",
        parse_mode='Markdown'
    )
    # Друге — окрема інструкція
    await update.message.reply_text(
        "Напишіть своє *ім'я*, щоб розпочати 👇",
        parse_mode='Markdown'
    )

    return States.NAME

'''
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(Questions.NAME)
    return States.NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.NAME] = update.message.text
    await update.message.reply_text(Questions.PHONE)
    return States.PHONE
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.PHONE] = update.message.text
    await update.message.reply_text(Questions.BUSINESS)
    return States.BUSINESS
'''

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.NAME] = update.message.text

    # Create a keyboard button to request contact
    contact_button = KeyboardButton("📞 Поділитися номером телефону", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "📲 Поділіться своїм номером телефону, натиснувши кнопку нижче.",
        reply_markup=reply_markup
    )
    return States.PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact:
        context.user_data[States.PHONE] = update.message.contact.phone_number
    else:
        await update.message.reply_text("Поділіться своїм номером телефону, натиснувши кнопку.")
        return States.PHONE

    # Remove keyboard and proceed
    await update.message.reply_text(
        Questions.BUSINESS,
        reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True)
    )
    return States.BUSINESS


async def get_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.BUSINESS] = update.message.text
    await update.message.reply_text(Questions.WEBSITE)
    return States.WEBSITE

async def get_website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.WEBSITE] = update.message.text
    reply_markup = ReplyKeyboardMarkup(
        [["Соло-підприємець"], ["До 5-ти працівників у команді"],
         ["До 10-ти працівників у команді"], ["До 50-ти працівників у команді"],
         ["Більше 50-ти"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.EMPLOYEES, reply_markup=reply_markup)
    return States.EMPLOYEES

async def get_employees(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.EMPLOYEES] = update.message.text
    reply_markup = ReplyKeyboardMarkup(
        [["ФОП"], ["ТЗОВ"], ["Інше"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.LEGAL_FORM, reply_markup=reply_markup)
    return States.LEGAL_FORM

async def get_legal_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.LEGAL_FORM] = update.message.text
    await update.message.reply_text(Questions.ROLES, reply_markup=ReplyKeyboardRemove())
    return States.ROLES

async def get_roles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.ROLES] = update.message.text
    reply_markup = ReplyKeyboardMarkup(
        [["Так"], ["Ні"], ["Не знайомий(а) із цими високими матеріями 🙂"]],
        one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.FIN_KNOWLEDGE, reply_markup=reply_markup)
    return States.FIN_KNOWLEDGE

async def get_fin_knowledge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.FIN_KNOWLEDGE] = update.message.text
    await update.message.reply_text(Questions.FIN_PERSON, reply_markup=ReplyKeyboardRemove())
    return States.FIN_PERSON

async def get_fin_person(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.FIN_PERSON] = update.message.text
    await update.message.reply_text(Questions.FIN_REPORTS)
    return States.FIN_REPORTS

async def get_fin_reports(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.FIN_REPORTS] = update.message.text
    reply_markup = ReplyKeyboardMarkup([["Так"], ["Ні"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.CRM, reply_markup=reply_markup)
    return States.CRM

async def get_crm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.CRM] = update.message.text
    if update.message.text == "Так":
        await update.message.reply_text(Questions.CRM_NAME)
        return States.CRM_NAME
    else:
        context.user_data[States.CRM_NAME] = "Ні"
        return await get_crm_name(update, context)

async def get_crm_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text != "Ні":
        context.user_data[States.CRM_NAME] = update.message.text
    reply_markup = ReplyKeyboardMarkup([["Так"], ["Ні"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.FINMAP, reply_markup=reply_markup)
    return States.FINMAP

async def get_finmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.FINMAP] = update.message.text
    reply_markup = ReplyKeyboardMarkup([["Так"], ["Ні"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.GOOGLE_SHEETS, reply_markup=reply_markup)
    return States.GOOGLE_SHEETS

async def get_google_sheets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.GOOGLE_SHEETS] = update.message.text
    reply_markup = ReplyKeyboardMarkup([["Так"], ["Ні"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.MEETINGS, reply_markup=reply_markup)
    return States.MEETINGS

async def get_meetings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.MEETINGS] = update.message.text
    if update.message.text == "Так":
        await update.message.reply_text(Questions.MEETING_DETAILS)
        return States.MEETING_DETAILS
    else:
        context.user_data[States.MEETING_DETAILS] = "Немає"
        return await get_meeting_details(update, context)

async def get_meeting_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text != "Немає":
        context.user_data[States.MEETING_DETAILS] = update.message.text
    await update.message.reply_text(Questions.REQUESTS)
    return States.REQUESTS

async def get_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.REQUESTS] = update.message.text
    reply_markup = ReplyKeyboardMarkup([["Так"], ["Ні"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.USED_CONSULTANTS, reply_markup=reply_markup)
    return States.USED_CONSULTANTS

async def get_used_consultants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.USED_CONSULTANTS] = update.message.text
    reply_markup = ReplyKeyboardMarkup([["Offline у м. Львів"], ["Online Zoom/Google Meet"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.FORMAT, reply_markup=reply_markup)
    return States.FORMAT

async def get_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[States.FORMAT] = update.message.text
    reply_markup = ReplyKeyboardMarkup(
        [["Instagram"], ["Порада одноклубника"], ["Порада друга/подруги"], ["Google пошук"]],
        one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(Questions.REFERRAL, reply_markup=reply_markup)
    return States.REFERRAL

async def get_referral(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data[States.REFERRAL] = update.message.text

    user_data = context.user_data
    summary = build_summary(user_data)
    reply_markup = ReplyKeyboardMarkup([["Так"], ["Ні"]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(f"*{Questions.CONFIRM}*\n\n{summary}\n\nВсе правильно?",
        parse_mode='Markdown', reply_markup=reply_markup)
    return States.CONFIRM

async def get_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text.lower()
    context.user_data[States.CONFIRM] = user_answer

    user_data = context.user_data
    if user_answer.lower() in ["так", "yes"]:

         # Збереження в SQLite
        #save_to_sqlite(user_data)
        # Відправка в групу
        group_id = context.application.bot_data.get("chat_id")
        if group_id:
            summary = build_summary(user_data)
            await context.bot.send_message(chat_id=group_id, text=f"📬 Нова анкета:\n\n{summary}", parse_mode='Markdown')
        else: 
            print("❌ Group chat ID not found in bot data.")

        await update.message.reply_text(
    
            "Дякуємо! Ваша анкета збережена і відправлена.\n\n"
        )
        
        return await provide_calendly(update, context)
    else:
        await update.message.reply_text(
            "Добре, давайте почнемо спочатку. Введіть /restart для початку заново."
        )
        return States.CONFIRM # Waiting for  /restart


async def provide_calendly(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    url = context.application.bot_data.get("calendly_url", "https://calendly.com/your-default-url")
    if not url:
        await update.message.reply_text("❌ URL Calendly не знайдено. Будь ласка, налаштуйте його в bot_data.")
        return ConversationHandler.END
    keyboard = [[InlineKeyboardButton("📅 Забронювати зустріч", url=url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Натисніть кнопку нижче, щоб обрати зручний час для зустрічі:",
        reply_markup=reply_markup
    )

    return ConversationHandler.END
