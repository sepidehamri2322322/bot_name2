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


class ChannelManager:
    def __init__(self, db_name, bot):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.bot = bot

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()

    def close(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def connect_to_db(self):
        try:
            self.connect()
            print("Connected to database successfully.")
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_username TEXT NOT NULL UNIQUE,
                    added_by INTEGER,
                    added_by_name TEXT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error connecting to database: {e}")
        finally:
            self.close()

    def add_channel(self, channel_username, added_by, added_by_name):
        self.connect()
        try:
            self.cursor.execute(
                """
                INSERT INTO channels (channel_username, added_by, added_by_name)
                VALUES (?, ?, ?)
                """, (channel_username, added_by, added_by_name)
            )
            self.connection.commit()
            print(f"Channel {channel_username} added successfully.")
        except Exception as e:
            print(f"Error adding channel: {e}")
        finally:
            self.close()

    def get_channels(self):
        self.connect()
        try:
            self.cursor.execute(
                """
                SELECT channel_username FROM channels
                """
            )
            channels = self.cursor.fetchall()
            return [channel[0] for channel in channels]
        except Exception as e:
            print(f"Error fetching channels: {e}")
            return []
        finally:
            self.close()

    def clear_table(self):
        self.connect()
        try:
            if self.cursor:
                self.cursor.execute("DELETE FROM channels")
                self.connection.commit()
                print("Channels table cleared successfully.")
            else:
                print("Cursor not initialized.")
        except sqlite3.Error as e:
            print(f"Error clearing table: {e}")
        finally:
            self.close()

# ایجاد یک نمونه از بات تلگرام با استفاده از توکن بات شما
bot = telebot.TeleBot("توکن بات شما")

db_name = 'telegram_bot.db'

# مقداردهی اولیه ChannelManager با نمونه بات
# db_manager1 = ChannelManager(db_name, bot)
# db_manager1.connect_to_db()  # ایجاد جدول در دیتابیس اگر وجود نداشته باشد
# db_manager1.clear_table()    # پاک کردن جدول کانال‌ها
#     def clear_table(self):
#         try:
#             self.connect_to_db()
#             if self.cursor:
#                 self.cursor.execute("DELETE FROM channels")
#                 self.connection.commit()
#                 print("Channels table cleared successfully.")
#             else:
#                 print("Cursor not initialized.")
#         except sqlite3.Error as e:
#             print(f"Error clearing table: {e}")
#         finally:
#             self.close()

# # ایجاد یک نمونه از بات تلگرام با استفاده از توکن بات شما
# bot = telebot.TeleBot("توکن بات شما")

# db_name = 'telegram_bot.db'
# channel_username = "sepidehtest"
# chanel_message = ChannelManager(db_name, bot)

# # مقداردهی اولیه ChannelAccessManager با نمونه بات
# db_manager1 = ChannelManager(db_name, bot, channel_username)
# db_manager1.clear_table()