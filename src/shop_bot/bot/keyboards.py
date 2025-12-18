import logging

from datetime import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from shop_bot.data_manager.database import get_setting

logger = logging.getLogger(__name__)

main_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🏠 Главное меню")]],
    resize_keyboard=True
)

def create_main_menu_keyboard(user_keys: list, trial_available: bool, is_admin: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if trial_available and get_setting("trial_enabled") == "true":
        builder.button(text="🎁 Попробовать бесплатно", callback_data="get_trial")

    builder.button(text="👤 Мой кабинет", callback_data="show_profile")
    builder.button(text=f"💳 Мои тарифы ({len(user_keys)})", callback_data="manage_keys")
    builder.button(text="📞 Тех. поддержка", callback_data="show_help")
    builder.button(text="📖 Инструкция", callback_data="howto_vless")
    builder.button(text="🤝 Реферальная программа", callback_data="show_referral_program")
    builder.button(text="📢 Наши новости", callback_data="show_about")
    
    if is_admin:
        builder.button(text="📢 Рассылка", callback_data="start_broadcast")

    # Раскладка: [trial], [кабинет, тарифы], [поддержка, инструкция], [реферальная], [новости], [рассылка если админ]
    layout = []
    if trial_available and get_setting("trial_enabled") == "true":
        layout.append(1)  # Попробовать бесплатно - одна кнопка
    layout.append(2)  # Мой кабинет и Мои тарифы - две кнопки в строке
    layout.append(2)  # Тех. поддержка и Инструкция - две кнопки в строке
    layout.append(1)  # Реферальная программа - одна кнопка
    layout.append(1)  # Наши новости - одна кнопка
    if is_admin:
        layout.append(1)  # Рассылка - одна кнопка
    
    builder.adjust(*layout)
    
    return builder.as_markup()

def create_broadcast_options_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Добавить кнопку", callback_data="broadcast_add_button")
    builder.button(text="➡️ Пропустить", callback_data="broadcast_skip_button")
    builder.button(text="❌ Отмена", callback_data="cancel_broadcast")
    builder.adjust(2, 1)
    return builder.as_markup()

def create_broadcast_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Отправить всем", callback_data="confirm_broadcast")
    builder.button(text="❌ Отмена", callback_data="cancel_broadcast")
    builder.adjust(2)
    return builder.as_markup()

def create_broadcast_cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Отмена", callback_data="cancel_broadcast")
    return builder.as_markup()

def create_about_keyboard(channel_url: str | None, terms_url: str | None, privacy_url: str | None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if channel_url:
        builder.button(text="📰 Наш канал", url=channel_url)
    if terms_url:
        builder.button(text="📄 Условия использования", url=terms_url)
    if privacy_url:
        builder.button(text="🔒 Политика конфиденциальности", url=privacy_url)
    builder.button(text="⬅️ Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()
    
def create_support_keyboard(support_user: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🆘 Написать в поддержку", url=support_user)
    builder.button(text="⬅️ Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()

def create_support_telegram_keyboard(support_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📞 Написать в тех. поддержку", url=support_url)
    builder.button(text="⬅️ Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()

def create_news_channel_keyboard(channel_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📢 Перейти в канал новостей", url=channel_url)
    builder.button(text="⬅️ Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()

def create_host_selection_keyboard(hosts: list, action: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for host in hosts:
        callback_data = f"select_host_{action}_{host['host_name']}"
        builder.button(text=host['host_name'], callback_data=callback_data)
    builder.button(text="⬅️ Назад", callback_data="manage_keys" if action == 'new' else "back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()

def create_plans_keyboard(plans: list[dict], action: str, host_name: str, key_id: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for plan in plans:
        callback_data = f"buy_{host_name}_{plan['plan_id']}_{action}_{key_id}"
        builder.button(text=f"{plan['plan_name']} - {plan['price']:.0f} RUB", callback_data=callback_data)
    back_callback = "manage_keys" if action == "extend" else "buy_new_key"
    builder.button(text="⬅️ Назад", callback_data=back_callback)
    builder.adjust(1) 
    return builder.as_markup()

def create_email_input_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад к тарифам", callback_data="back_to_plans")
    builder.adjust(1)
    return builder.as_markup()

def create_payment_method_keyboard(payment_methods: dict, action: str, key_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if payment_methods and payment_methods.get("yookassa"):
        if get_setting("sbp_enabled"):
            builder.button(text="🏦 СБП / Банковская карта", callback_data="pay_yookassa")
        else:
            builder.button(text="🏦 Банковская карта", callback_data="pay_yookassa")
    builder.button(text="💳 Банковская карта РФ", callback_data="pay_bank_card_rf")
    if payment_methods and payment_methods.get("heleket"):
        builder.button(text="💎 Криптовалюта", callback_data="pay_heleket")
    if payment_methods and payment_methods.get("cryptobot"):
        builder.button(text="🤖 CryptoBot", callback_data="pay_cryptobot")
    if payment_methods and payment_methods.get("tonconnect"):
        callback_data_ton = "pay_tonconnect"
        logger.info(f"Creating TON button with callback_data: '{callback_data_ton}'")
        builder.button(text="🪙 TON Connect", callback_data=callback_data_ton)

    builder.button(text="⬅️ Назад", callback_data="back_to_email_prompt")
    builder.adjust(1)
    return builder.as_markup()

def create_ton_connect_keyboard(connect_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🚀 Открыть кошелек", url=connect_url)
    return builder.as_markup()

def create_payment_keyboard(payment_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти к оплате", url=payment_url)
    return builder.as_markup()

def create_payment_confirmed_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Я оплатил", callback_data="payment_confirmed")
    builder.button(text="⬅️ Назад", callback_data="back_to_payment_method")
    builder.adjust(1)
    return builder.as_markup()

def create_admin_document_keyboard(document_id: int, transaction_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Одобрить", callback_data=f"approve_document_{document_id}_{transaction_id}")
    builder.button(text="❌ Отклонить", callback_data=f"reject_document_{document_id}_{transaction_id}")
    builder.adjust(2)
    return builder.as_markup()

def create_keys_management_keyboard(keys: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if keys:
        for i, key in enumerate(keys):
            expiry_date = datetime.fromisoformat(key['expiry_date'])
            status_icon = "✅" if expiry_date > datetime.now() else "❌"
            host_name = key.get('host_name', 'Неизвестный хост')
            button_text = f"{status_icon} Ключ #{i+1} ({host_name}) (до {expiry_date.strftime('%d.%m.%Y')})"
            builder.button(text=button_text, callback_data=f"show_key_{key['key_id']}")
    builder.button(text="➕ Купить новый ключ", callback_data="buy_new_key")
    builder.button(text="⬅️ Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()

def create_key_info_keyboard(key_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Продлить этот ключ", callback_data=f"extend_key_{key_id}")
    builder.button(text="📱 Показать QR-код", callback_data=f"show_qr_{key_id}")
    builder.button(text="📖 Инструкция", callback_data=f"howto_vless_{key_id}")
    builder.button(text="⬅️ Назад к списку ключей", callback_data="manage_keys")
    builder.adjust(1)
    return builder.as_markup()

def create_howto_vless_keyboard(android_url: str, linux_url: str, ios_url: str, windows_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Android", url=android_url)
    builder.button(text="📱 iOS", url=ios_url)
    builder.button(text="💻 Windows", url=windows_url)
    builder.button(text="💻 macOS", url=linux_url)
    builder.button(text="⬅️ Назад в меню", callback_data="back_to_main_menu")
    builder.adjust(2, 2, 1)
    return builder.as_markup()

def create_howto_vless_keyboard_key(android_url: str, linux_url: str, ios_url: str, windows_url: str, key_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Android", url=android_url)
    builder.button(text="📱 iOS", url=ios_url)
    builder.button(text="💻 Windows", url=windows_url)
    builder.button(text="💻 macOS", url=linux_url)
    builder.button(text="⬅️ Назад к ключу", callback_data=f"show_key_{key_id}")
    builder.adjust(2, 2, 1)
    return builder.as_markup()

def create_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад в меню", callback_data="back_to_main_menu")
    return builder.as_markup()

def create_welcome_keyboard(channel_url: str | None, is_subscription_forced: bool = False, terms_url: str | None = None, privacy_url: str | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if channel_url and terms_url and privacy_url and is_subscription_forced:
        builder.button(text="📢 Перейти в канал", url=channel_url)
        builder.button(text="📄 Условия использования", url=terms_url)
        builder.button(text="🔒 Политика конфиденциальности", url=privacy_url)
        builder.button(text="✅ Я подписался", callback_data="check_subscription_and_agree")
    elif channel_url and terms_url and privacy_url:
        builder.button(text="📢 Наш канал (не обязательно)", url=channel_url)
        builder.button(text="📄 Условия использования", url=terms_url)
        builder.button(text="🔒 Политика конфиденциальности", url=privacy_url)
        builder.button(text="✅ Принимаю условия", callback_data="check_subscription_and_agree")
    elif terms_url and privacy_url:
        builder.button(text="📄 Условия использования", url=terms_url)
        builder.button(text="🔒 Политика конфиденциальности", url=privacy_url)
        builder.button(text="✅ Принимаю условия", callback_data="check_subscription_and_agree")
    elif terms_url:
        builder.button(text="📄 Условия использования", url=terms_url)
        builder.button(text="✅ Принимаю условия", callback_data="check_subscription_and_agree")
    elif privacy_url:
        builder.button(text="🔒 Политика конфиденциальности", url=privacy_url)
        builder.button(text="✅ Принимаю условия", callback_data="check_subscription_and_agree")
    else:
        builder.button(text="📢 Наш канал (не обязательно)", url=channel_url)
        builder.button(text="✅ Я подписался", callback_data="check_subscription_and_agree")
    builder.adjust(1)
    return builder.as_markup()

def get_main_menu_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="🏠 В главное меню", callback_data="show_main_menu")

def get_buy_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="💳 Купить подписку", callback_data="buy_vpn")

