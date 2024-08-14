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
# Create a Telegram bot instance using your bot token (replace with your actual token)
bot = telebot.TeleBot("6771369229:AAG9aUcdFXBysLjJTq1Wv5N5kFBtlHn1jN8")

db_name = 'telegram_bot.db'
channel_username = "sepidehtest"
class Chanel_telegram:
    def __init__(self,db_name,bot,channel_username):
        
        self.db_name=db_name
        self.connction=None
        self.cursor=None
        self.bot=bot
        self.channel_username=channel_username
        
    def connect(self):
        if self.connction is None:
            self.connction=sqlite3.connect(self.db_name)
            self.cursor=self.connction.cursor()
    
    def close(self):
        if self.connction  is not None:
            self.cursor.close()
            self.connction .close()
            self.connction  = None
            self.cursor = None
    
    def connect_to_db(self):
        self.connect()
        try:
            
            print("Connected to database successfully.")
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_status(
                    user_id INTEGER PRIMARY KEY,
                    is_member INTEGER,
                    channel_id INTEGER,
                    user_name TEXT,
                    FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
            )
                """
            )
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_username TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    user_name TEXT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connction.commit()
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.close()
    
    def add_channel(self,channel_username,user_id,user_name):
        self.connect_to_db()
        try:
            self.connect()
            self.cursor.execute(
                """
                INSERT INTO channels (channel_username, user_id, user_name)
                VALUES (?, ?, ?)
                
                """, (channel_username, user_id, user_name))
            self.connction.commit()
            print(f"Channel {channel_username} added successfully.")
        
        except Exception as e:
            print(f"Error adding channel: {e}")
        finally:
            self.close()

        
   
   
   
    def update_user_status(self,user_id,is_member,user_name,channel_username):  # کاربر را در دیتابیس به‌روزرسانی می‌کنیم.
        self.connect_to_db()
        try:
            self.cursor.execute("""
                INSERT INTO user_status (user_id, is_member, user_name, channel_id)
                VALUES (?, ?, ?, (SELECT channel_id FROM channels WHERE channel_username = ?))
                ON CONFLICT(user_id) DO UPDATE SET is_member=excluded.is_member, user_name=excluded.user_name;
            """, (user_id, int(is_member), user_name, channel_username))
            
            self.connction.commit()
        except Exception as e:
            print(f"Error updating user status: {e}")
        finally:
            self.close()
            
    def is_member_of_channel(self,user_id,channel_username):    # بررسی عضویت کاربر در کانال
        try:
            member_status = self.bot.get_chat_member(f"@{channel_username}", user_id).status
            
            return member_status in ['member', 'administrator', 'creator'] 
        except Exception as e:
            print("عضو گیری انجام نشد")    
    
    def get_channels(self):
        self.connect_to_db()
        try:
            self.cursor.execute(
            """
            SELECT channel_username FROM channels
            """
           )
            channels = self.cursor.fetchall()
        # حذف علامت @ اگر وجود داشته باشد و برگرداندن لیست کانال‌ها
            return [channel[0].lstrip('@') for channel in channels]
        except Exception as e:
            print(f"Error fetching channels: {e}")
            return []
        finally:
           self.close()
    
    def channel_exists(self, channel_username):
        self.connect()
        try:
            self.cursor.execute('SELECT 1 FROM channels WHERE channel_username = ?', (channel_username,))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"خطا در بررسی وجود کانال: {e}")
            return False
        finally:
            self.close()
    
    def is_member_of_all_channels(self,user_id):
        self.connect_to_db()
        channels = self.get_channels()
        for channel in channels:
             if not self.is_member_of_channel(user_id, channel):
                 return False
        return True
    
    def get_channels(self):
    # فرض بر این است که نام کاربری‌های کانال‌ها به درستی در اینجا برگردانده می‌شود
        return ['sepidehtest']  # بدون علامت @

    def get_non_member_channels(self, user_id):
        channels = self.get_channels()
        non_member_channels = [channel for channel in channels if not self.is_member_of_channel(user_id, channel)]
        return non_member_channels
    
    def process_user_message(self, message):
        user_id = message.chat.id
        user_name = message.chat.username

        non_member_channels = self.get_non_member_channels(user_id)
        if non_member_channels:
            markup = InlineKeyboardMarkup()
            for channel in non_member_channels:
                channel_username = channel.lstrip('@')  # حذف علامت @ اگر وجود داشته باشد
                join_button = InlineKeyboardButton(
                text=f"عضویت در {channel_username}", 
                url=f"https://t.me/{channel_username}"
            )
                markup.add(join_button)
            self.bot.send_message(
            user_id, 
            "شما باید عضو کانال‌های زیر شوید تا بتوانید از ربات استفاده کنید:", 
            reply_markup=markup
        )
        else:
            
            self.update_user_status(user_id, 1, user_name, self.channel_username)
            self.bot.send_message(
            user_id, 
            "خوش آمدید! شما می‌توانید از ربات استفاده کنید."
        )
    
    def remove_channel(self, channel_username, admin_id):
        self.connect()
        try:
            self.cursor.execute("DELETE FROM channels WHERE channel_username = ?", (channel_username,))
            self.connction.commit()
            print(f"Channel {channel_username} removed successfully.")
            return True
        except Exception as e:
            print(f"Error removing channel: {e}")
            return False
        finally:
            self.close()        
      
    # def remove_channel(self, channel_username, admin_id):
    #     self.connect_to_db()
    #     try:
    #         # بررسی اینکه درخواست حذف از طرف ادمین است
    #         self.connect()
    #         self.cursor.execute("DELETE FROM channels WHERE channel_username = ?", (channel_username,))
    #         if self.cursor.rowcount > 0:
    #             self.connction.commit()
    #             self.bot.send_message(admin_id, f"کانال {channel_username} با موفقیت حذف شد.")
    #         else:
    #             self.bot.send_message(admin_id, f"کانال {channel_username} یافت نشد.")
    #     except Exception as e:
    #         print(f"خطا در حذف کانال: {e}")
    #         self.bot.send_message(admin_id, "خطایی در حذف کانال رخ داده است.")
    #     finally:
    #         self.close()  
      


# @bot.message_handler(commands=['start'])
# def handle_start_command(message):
    
#     chanel_message.process_user_message(message)

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
    
# @bot.message_handler(func=lambda message: message.text == 'اضافه کردن کانال')
# def request_channel_info(message):
#     user_id = message.chat.id
#     if user_id != admin_id:
#         bot.send_message(user_id, "شما مجاز به استفاده از این دستور نیستید.")
#         return

#     msg = bot.send_message(user_id, "لطفاً نام کاربری کانال را وارد کنید:")
#     bot.register_next_step_handler(msg, process_channel_info)

# def process_channel_info(message):
#     user_id = message.chat.id
#     channel_username = message.text.strip()
#     user_name = message.chat.username

#     if chanel_message.channel_exists(channel_username):
#         bot.send_message(user_id, "این کانال قبلاً ثبت شده است.")
#         return

#     chanel_message.add_channel(channel_username, user_id, user_name)
#     bot.send_message(user_id, f"کانال {channel_username} با موفقیت ثبت شد.")
#     bot.send_message(admin_id, f"کاربر @{user_name} کانالی با نام کاربری {channel_username} ثبت کرده است.")

# admin_id = 1277323739


# @bot.message_handler(commands=['remove_channel'])
# def handle_remove_channel(message):
#     user_id = message.chat.id
#     if user_id != admin_id:
#         bot.send_message(user_id, "شما مجاز به استفاده از این دستور نیستید.")
#         return
    
#     msg = bot.send_message(user_id, "لطفاً نام کاربری کانال را که می‌خواهید حذف کنید وارد کنید:")
#     bot.register_next_step_handler(msg, process_remove_channel)

# def process_remove_channel(message):
#     channel_username = message.text.strip()
#     chanel_message.remove_channel(channel_username, admin_id)
    
    
# bot.polling()