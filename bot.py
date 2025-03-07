import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Токен вашего бота
TOKEN = "8065727129:AAEVafcatHHJ6xQ0QtdARgKIawWn0F0gY-A"

# Курс юаня к рублю (фиксированный)
CNY_TO_RUB_RATE = 14  # 1 CNY = 14 RUB

# Функция для расчета стоимости с учетом условий
def calculate_total_price(amount_cny):
    # Конвертируем сумму в рубли
    amount_rub = amount_cny * CNY_TO_RUB_RATE

    # Добавляем дополнительные расходы
    if amount_cny < 1000:
        amount_rub += 500  # +500 рублей, если сумма меньше 1000 юаней
    else:
        amount_rub += 1000  # +1000 рублей, если сумма больше или равна 1000 юаней

    return amount_rub

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Получена команда /start")  # Отладочное сообщение
    await update.message.reply_text(
        "👋 Привет! Я бот для расчета стоимости товара из Китая. 🛒\n"
        "Просто отправь мне стоимость товара в юанях, и я рассчитаю итоговую стоимость в рублях. 💰"
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Получено текстовое сообщение")  # Отладочное сообщение
    try:
        # Получаем текст сообщения (стоимость товара в юанях)
        amount_cny = float(update.message.text)

        # Рассчитываем итоговую стоимость
        total_price = calculate_total_price(amount_cny)

        # Отправляем результат пользователю
        await update.message.reply_text(
            f"📦 Стоимость товара: {amount_cny} CNY\n"
            f"💸 Итоговая стоимость без учета доставки: {total_price:.2f} RUB\n\n"
            "📨 Для заказа напишите нам в Telegram:\n"
            "👉 @XASTERSELL\n\n"
            "🚀 Мы поможем вам с оформлением заказа и расчетом доставки!"
        )
    except ValueError:
        # Если пользователь ввел не число
        await update.message.reply_text("❌ Пожалуйста, введите стоимость товара в юанях (например, 500).")

# Основная функция
def main():
    print("Бот запускается...")  # Отладочное сообщение
    try:
        # Создаем приложение и передаем токен
        application = Application.builder().token(TOKEN).build()

        # Регистрируем команду /start
        application.add_handler(CommandHandler("start", start))

        # Регистрируем обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Запускаем бота
        print("Бот начал работу.")  # Отладочное сообщение
        application.run_polling()
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")  # Отладочное сообщение

if __name__ == "__main__":
    main()