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


