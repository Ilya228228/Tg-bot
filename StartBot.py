import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, filters

# Устанавливаем уровень логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Токен бота и платежного провайдера
BOT_TOKEN = 'Токен бота'
PAYMENT_PROVIDER_TOKEN = 'Токен платежа'

# URL, который будет отправлен после успешного платежа
SUCCESS_URL = "Ссылка после оплаты"


async def start(update, context):
    keyboard = [[InlineKeyboardButton("Купить", callback_data='buy')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)


async def button_callback(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'buy':
        chat_id = query.message.chat_id
        title = "Покупка товара"
        description = "Товар"
        payload = "custom_payload"
        currency = "RUB"
        prices = [LabeledPrice("Товар", 25000)]  # Цена в копейках (например, 250 руб)
        
        await context.bot.send_invoice(chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN,
                                       currency, prices)


async def precheckout_callback(update, context):
    query = update.pre_checkout_query
    await query.answer(ok=True)


async def successful_payment_callback(update, context):
    await update.message.reply_text(f"Платеж успешен!\nВот ваша ссылка: {SUCCESS_URL}")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    application.run_polling()

if __name__ == '__main__':
    main()
