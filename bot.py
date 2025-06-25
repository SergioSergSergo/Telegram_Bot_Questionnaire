from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from dotenv import load_dotenv
import os
from questionnaire import States
from questionnaire import (
    start, get_name, get_phone, get_business, get_website, get_employees,
    get_legal_form, get_roles, get_fin_knowledge, get_fin_person, get_fin_reports, get_crm,
    get_crm_name, get_finmap, get_google_sheets, get_meetings, get_meeting_details, help_command,
    get_requests, get_used_consultants, get_format, get_referral, get_confirm,  cancel, restart, provide_calendly, timeout_callback
)
# Load environment variables
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



load_dotenv(dotenv_path=".env")
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set.")

CHAT_ID = os.getenv("GROUP_CHAT_ID")
if not CHAT_ID:
    raise ValueError("GROUP_CHAT_ID environment variable not set.")

CALENDLY_URL = os.getenv("CALENDLY_URL")
if not CALENDLY_URL:
    raise ValueError("CALENDLY_URL environment variable not set.")

def main():
    #  Build the application
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .arbitrary_callback_data(True)
        .concurrent_updates(True)
        .build()
    )
    app.bot_data['chat_id'] = CHAT_ID
    app.bot_data['calendly_url'] = CALENDLY_URL
    logger.info("Bot started")
    #  Conversation handler for the questionnaire
    conv_handler = ConversationHandler(

        entry_points=[CommandHandler("start", start),
                       CommandHandler("help", help_command),],
        states={
                States.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
                States.PHONE: [
                    MessageHandler(filters.CONTACT, get_phone),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)  # fallback in case user types instead
                ],
                States.BUSINESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_business)],
                States.WEBSITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_website)],
                States.EMPLOYEES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_employees)],
                States.LEGAL_FORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_legal_form)],
                States.ROLES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_roles)],
                States.FIN_KNOWLEDGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fin_knowledge)],
                States.FIN_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fin_person)],
                States.FIN_REPORTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fin_reports)],
                States.CRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_crm)],
                States.CRM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_crm_name)],
                States.FINMAP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_finmap)],
                States.GOOGLE_SHEETS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_google_sheets)],
                States.MEETINGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_meetings)],
                States.MEETING_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_meeting_details)],
                States.REQUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_requests)],
                States.USED_CONSULTANTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_used_consultants)],
                States.FORMAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_format)],
                States.REFERRAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_referral)],
                States.CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_confirm)],
                States.CALLENDLY: [
                    CallbackQueryHandler(provide_calendly , pattern='^calendly$'),
                    CommandHandler("calendly", provide_calendly)
                ],
                # ⏰ Додано обробник неактивності
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, timeout_callback)],
            },  
    fallbacks=[
        CommandHandler("cancel", cancel),
        CommandHandler("restart", restart),
        CommandHandler("start", start),
        CommandHandler("help", help_command),],

    conversation_timeout=600,  # 10 хвилина до завершення сесії без дій
)
    # Register handlers
    app.add_handler(conv_handler)
    # Start the botapp
    app.run_polling(
    timeout=100,        # Telegram будет ждать 30 сек перед тем, как вернуть пустой ответ
    read_timeout=105    # HTTPX/HTTPCore ждёт ещё 5 сек на получение тела ответа
)

if __name__ == "__main__":
    main()
