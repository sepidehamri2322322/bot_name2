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
import time
from ChannelAccessManager import Chanel_telegram 
bot = telebot.TeleBot("6771369229:AAG9aUcdFXBysLjJTq1Wv5N5kFBtlHn1jN8")

db_name = 'telegram_bot.db'
channel_username = "sepidehtest"
admin_id = 1277323739
chanel_message = Chanel_telegram(db_name, bot, channel_username)
class AdminManager:
    def __init__(self, bot, chanel_message, admin_id):
        self.bot = bot
        self.chanel_message = chanel_message
        self.admin_id = admin_id

    def is_admin(self, user_id):
        return user_id == self.admin_id

    def request_channel_info(self, message):
        user_id = message.chat.id
        if not self.is_admin(user_id):
            self.bot.send_message(user_id, "شما مجاز به استفاده از این دستور نیستید.")
            return

        msg = self.bot.send_message(user_id, "لطفاً نام کاربری کانال را وارد کنید:")
        self.bot.register_next_step_handler(msg, self.process_channel_info)

    def process_channel_info(self, message):
        user_id = message.chat.id
        channel_username = message.text.strip()
        user_name = message.chat.username

        print(f"User ID: {user_id}, Channel Username: {channel_username}, User Name: {user_name}")

        if self.chanel_message.channel_exists(channel_username):
            self.bot.send_message(user_id, "این کانال قبلاً ثبت شده است.")
            return

        success = self.chanel_message.add_channel(channel_username, user_id, user_name)
        if success:
            self.bot.send_message(user_id, f"کانال {channel_username} با موفقیت ثبت شد.")
        else:
            self.bot.send_message(user_id, "خطایی در ثبت کانال رخ داده است. لطفاً مجدداً تلاش کنید.")

    def process_remove_channel(self, message):
        channel_username = message.text.strip()
        if self.chanel_message.remove_channel(channel_username, self.admin_id):
            self.bot.send_message(self.admin_id, f"کانال {channel_username} با موفقیت حذف شد.")
        else:
            self.bot.send_message(self.admin_id, "خطا در حذف کانال. لطفاً مجدداً تلاش کنید.")
    def list_channels(self, message):
        user_id = message.chat.id
        if not self.is_admin(user_id):
            self.bot.send_message(user_id, "شما مجاز به استفاده از این دستور نیستید.")
            return

        channels = self.chanel_message.get_channels()
        if channels:
            channels_list = '\n'.join(channels)
            self.bot.send_message(user_id, f"لیست کانال‌های ثبت شده:\n{channels_list}")
        else:
            self.bot.send_message(user_id, "هیچ کانالی ثبت نشده است.")

    def check_membership(self, user_id):
        channels = self.chanel_message.get_channels()
        for channel in channels:
            if not self.chanel_message.is_member_of_channel(user_id, channel):
                return False, channels
        return True, []

# Initialize AdminManager with necessary dependencies
admin_manager = AdminManager(bot, chanel_message, admin_id)        

# Initialize AdminManager with necessary dependencies
admin_manager = AdminManager(bot, chanel_message, admin_id)

# Bot handlers for admin commands
# @bot.message_handler(func=lambda message: message.text == "add_channel_admin")
# def handle_add_channel_admin(message):
#     admin_manager.request_channel_info(message)

# @bot.message_handler(commands=['remove_channel'])
# def handle_remove_channel(message):
#     user_id = message.chat.id
#     if not admin_manager.is_admin(user_id):
#         bot.send_message(user_id, "شما مجاز به استفاده از این دستور نیستید.")
#         return
    
#     msg = bot.send_message(user_id, "لطفاً نام کاربری کانال را که می‌خواهید حذف کنید وارد کنید:")
#     bot.register_next_step_handler(msg, admin_manager.process_remove_channel)

# @bot.message_handler(func=lambda message: message.text == 'لغو')
# def cancel_management(message):
#     user_id = message.chat.id
#     bot.send_message(user_id, "عملیات مدیریت کانال لغو شد.")
    
    
# bot.polling()