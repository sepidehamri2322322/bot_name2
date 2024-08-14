import sys
import telebot
import requests
import re
from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3
import psycopg2
from telebot import TeleBot, types
from telegram.ext import Updater, CommandHandler, MessageHandler
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup , KeyboardButton 
from telebot.types import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import hashlib
import uuid
from ChannelAccessManager import Chanel_telegram
from SubscriptionManager import DatabaseManager
import zarinpal
from admin_channel import AdminManager

# Create a Telegram bot instance using your bot token (replace with your actual token)
bot = telebot.TeleBot("6771369229:AAG9aUcdFXBysLjJTq1Wv5N5kFBtlHn1jN8")

# first we need to check that user is new or old 
# to not increase scores twice

# check user mobile when start the bot

# check user invite link
# if the link is existed in user table: 
db_name = 'telegram_bot.db'

channel_username = "sepidehtest"


chanel_message = Chanel_telegram(db_name, bot, channel_username)

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    user_id = message.chat.id
    user_name = message.chat.username
    chanel_message.process_user_message(message)
    # بررسی عضویت کاربر در کانال‌ها
    
    channels = chanel_message.get_channels()
    if not channels:  # بررسی می‌کنیم که آیا کانالی وجود دارد یا خیر
        bot.send_message(user_id, "هیچ کانالی برای پیوستن موجود نیست.")
        handle_help(message)
        return
    is_member, channels = admin_manager.check_membership(user_id)
    if is_member:
        bot.send_message(user_id, "خوش آمدید! شما عضو همه کانال‌ها هستید.")
        
        # ادامه عملیات اگر کاربر عضو همه کانال‌ها بود
        handle_help(message)
        db_manager = DatabaseManager(db_name)
        referral_id = None
        print(f"Start command received from user_id: {user_id}")

        if len(message.text.split()) > 1:
            referral_code = message.text.split()[1]
            referral_id = db_manager.get_user_id_from_link(referral_code)
            print(f"Referral code: {referral_code}, Referral ID: {referral_id}")

        if db_manager.user_exists(user_id):
            user_link, stored_user_name = db_manager.get_user_link(user_id)
            if user_link:
                bot.send_message(user_id, f"لینک کاربری شما قبلاً ایجاد شده است: {user_link}")
            else:
                bot.send_message(user_id, "خطا در بازیابی لینک کاربری.")
        else:
            bot.send_message(user_id, "لطفاً نام خود را ارسال کنید.")
            bot.register_next_step_handler(message, get_user_id_from_link, db_manager, user_id, referral_id)
    else:
        # ارسال پیام و نمایش لینک کانال‌ها برای عضویت
        markup = InlineKeyboardMarkup()
        for channel in channels:
            join_button = InlineKeyboardButton(text=f"Join {channel}", url=f"https://t.me/{channel}")
            
            markup.add(join_button)
        bot.send_message(user_id, "لطفاً برای استفاده از ربات، ابتدا عضو کانال‌های زیر شوید:", reply_markup=markup)


@bot.message_handler(commands=['my_referrals'])
def handle_my_referrals(message):
    
    try:
        user_id = message.from_user.id
        db_manager = DatabaseManager(db_name)
        referrals_count = db_manager.get_referrals_count(user_id)
        if referrals_count > 0:
            referrals = db_manager.get_referrals(user_id)
            referrals_list = '\n'.join([str(ref_id) for ref_id in referrals])
            bot.send_message(user_id, f"شما {referrals_count} زیرمجموعه دارید:\n{referrals_list}")
        else:
            bot.send_message(user_id, "شما هیچ زیرمجموعه‌ای ندارید.")
    except Exception as e:
        print(f"Error fetching referrals: {e}")
        bot.send_message(user_id, "خطا در بازیابی زیرمجموعه‌ها.")

@bot.message_handler(commands=['osv'])
def handle_osv(message):
    user_id = message.chat.id
    user_name = message.chat.username

    channels = chanel_message.get_channels()
    member_found = False

    for channel in channels:
        # حذف علامت @ اگر وجود داشته باشد و اضافه کردن پروتکل https
        channel_username = channel.lstrip('@')
        channel_url = f"https://t.me/{channel_username}"
        if chanel_message.is_member_of_channel(user_id, channel_username):
            chanel_message.update_user_status(user_id, 1, user_name, channel_username)
            bot.send_message(user_id, f"Welcome! You are a member of the channel {channel_username}.")
            member_found = True
            break

    if not member_found:
        markup = InlineKeyboardMarkup()
        for channel in channels:
            # حذف علامت @ اگر وجود داشته باشد و اضافه کردن پروتکل https
            channel_username = channel.lstrip('@')
            join_button = InlineKeyboardButton(text=f"Join {channel_username}", url=f"https://t.me/{channel_username}")
            markup.add(join_button)
        bot.send_message(user_id, "لطفا عضو کانال شوید", reply_markup=markup)

# @bot.message_handler(commands=['MANAGER'])
# def handle_management(message):
#     user_id = message.chat.id
#     if user_id != admin_id:
#         bot.send_message(user_id, "شما مجاز به استفاده از این دستور نیستید.")
#         return

#     markup = ReplyKeyboardMarkup(one_time_keyboard=True)
#     add_channel_button = KeyboardButton('اضافه کردن کانال')
#     cancel_button = KeyboardButton('لغو')
#     markup.add(add_channel_button, cancel_button)
#     bot.send_message(user_id, "در این قسمت می‌توانید کانال‌های خود را مدیریت کنید:", reply_markup=markup)
    

    # markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    # add_channel_button = KeyboardButton('ضافه کردن کاناال')
    # cancel_button = KeyboardButton('لغو')
    # markup.add(add_channel_button, cancel_button)
    # bot.send_message(user_id, "در این قسمت می‌توانید کانال‌های خود را مدیریت کنید:", reply_markup=markup)
@bot.message_handler(commands=['add_channel'])
def handle_add_channel(message):
    admin_manager.request_channel_info(message)
    
@bot.message_handler(commands=['list_channels'])
def handle_list_channels(message):
    admin_manager.list_channels(message)

    
@bot.message_handler(commands=['add_channel_admin'])
def request_channel_info(message):
    user_id = message.chat.id
    if user_id != admin_id:
        bot.send_message(user_id, "شما مجاز به استفاده از این دستور نیستید.")
        return

    
def process_channel_info(message):
    user_id = message.chat.id
    channel_username = message.text.strip()
    user_name = message.chat.username

    print(f"User ID: {user_id}, Channel Username: {channel_username}, User Name: {user_name}")

    if chanel_message.channel_exists(channel_username):
        bot.send_message(user_id, "این کانال قبلاً ثبت شده است.")
        return

    success = chanel_message.add_channel(channel_username, user_id, user_name)
    if success:
        bot.send_message(user_id, f"کانال {channel_username} با موفقیت ثبت شد.")
    else:
        bot.send_message(user_id, "خطایی در ثبت کانال رخ داده است. لطفاً مجدداً تلاش کنید.")
@bot.message_handler(func=lambda message: message.text == 'لغو')
def cancel_management(message):
    user_id = message.chat.id
    bot.send_message(user_id, "عملیات مدیریت کانال لغو شد.")

admin_id = 1277323739
admin_manager = AdminManager(bot, chanel_message, admin_id)



@bot.message_handler(commands=['add_channel_user'])
def add_ch(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, "لطفاً نام کاربری کانال را وارد کنید:")
    bot.register_next_step_handler(msg, process_channel_info)


def process_channel_info(message):
    user_id = message.chat.id
    channel_username = message.text.strip()
    user_name = message.chat.username

    # if not is_valid_channel_username(channel_username):
    #     bot.send_message(user_id, "نام کاربری کانال معتبر نیست. لطفاً یک نام کاربری معتبر وارد کنید.")
    #     return

    # chanel_message.add_channel(channel_username, user_id, user_name)
    bot.send_message(user_id, f" {user_name} کانال  {channel_username} با موفقیت ثیت شد لطفا منتظر پیام پشتیبانی باشید ")
    bot.send_message(admin_id, f"کاربر @{user_name} کانالی با نام کاربری {channel_username} ثبت کرده است.")

@bot.message_handler(commands=['admin'])
def handle_admin_channel(message):
    user_id = message.chat.id
    if user_id != admin_id:
        bot.send_message(user_id, "شما مجاز به استفاده از این دستور نیستید.")
        return
    bot.send_message(user_id,"ادمین های عزیز دستور هایی مختص شماست که در ادامه با ان اشنا میشوید ")


@bot.message_handler(commands=['remove_channel'])
def handle_remove_channel(message):
    user_id = message.chat.id
    if user_id != admin_id:
        bot.send_message(user_id, "شما مجاز به استفاده از این دستور نیستید.")
        return
    
    msg = bot.send_message(user_id, "لطفاً نام کاربری کانال را که می‌خواهید حذف کنید وارد کنید:")
    bot.register_next_step_handler(msg, admin_manager.process_remove_channel)

def process_remove_channel(message):
    channel_username = message.text.strip()
    chanel_message.remove_channel(channel_username, admin_id)

    
@bot.message_handler(commands=['help'])
def handle_help(message):
    user_id = message.chat.id
    help_text = """
    خوش آمدید به ربات ما!

    در اینجا می‌توانید توضیحات مربوط به ربات و نحوه استفاده از آن را مشاهده کنید:

    1. برای شروع مجدد از دستور /start استفاده کنید.
    2. برای بررسی تعداد زیرمجموعه‌ها از دستور /my_referrals استفاده کنید.
    3. برای مشاهده وضعیت عضویت خود در کانال‌ها از دستور /osv استفاده کنید.
    4.اگر میخواهید کانالی به ربات اضافه کنید /add_channel_user 
    5.اگه ادمین هستین از دستور های مختص به ربات استفاده کنید /admin
    4. برای مدیریت کانال‌ها از دستور /add_channel استفاده کنید.
    5.از دستور /help برای راهنمایی گرفتن.
    
    """
    bot.send_message(user_id, help_text)

bot.polling()