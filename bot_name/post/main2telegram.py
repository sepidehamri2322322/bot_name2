import sys
import telebot
import requests
import re
from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3
from telebot import TeleBot, types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup , KeyboardButton 
from telebot.types import ReplyKeyboardMarkup
# Create a Telegram bot instance using your bot token (replace with your actual token)
bot = telebot.TeleBot("6771369229:AAGAcldhpExOWMtEM8eAz4bDkmbxM5Z9f8U")



button1=InlineKeyboardButton(text="button1" , url="https://google.com")
button2=InlineKeyboardButton(text="button2" , url="https://bing.com")
button3=InlineKeyboardButton(text="button3", callback_data="btn3")
button4=InlineKeyboardButton(text="button4" , callback_data="btn4")
inline_keyboard=InlineKeyboardMarkup(row_width=2)
inline_keyboard.add(button1,button2,button3,button4)


user_ID = []

@bot.message_handler(commands=["start"])
def welcome(message):
  bot.send_message(message.chat.id,"خوش اومدینننننننننن به این ربات",reply_markup=inline_keyboard)

  if message.chat.id not in user_ID:
    user_ID.append(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
   if call.data=="btn4":
        user_info = f"**نام کاربری:** {call.from_user.username}\n**شناسه کاربری:** {call.from_user.id}"
        bot.send_message(call.message.chat.id, user_info)
        # Request phone number
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        itembtn = types.KeyboardButton(text="ممنون بابت ارسال پاسخ", request_contact=True)
        markup.add(itembtn)
        message = bot.send_message(call.message.chat.id, "لطفا مخاطب خود را ارسال کنید:",reply_markup=markup)
        bot.register_next_step_handler(call.message, get_contact)
        
   

   elif call.data == "btn3":
      
        reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        button1 = types.KeyboardButton("اطلاعات دیتابیس")
        button2 = types.KeyboardButton("دکمه 2")
        reply_keyboard.add(button1, button2)
        bot.send_message(call.message.chat.id, "لطفا یکی از دکمه ها را انتخاب کنید", reply_markup=reply_keyboard)

        @bot.message_handler(func=lambda message: True)
        def handle_button_press(message):
           if message.text == "اطلاعات دیتابیس":
              bot.reply_to(message, "دکمه 1 در حال run شدن است")
              # create the databse
              



              # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, hide_keyboard=True)
              bot.send_message(message.chat.id, "Keyboard hidden")
           elif message.text == "دکمه 2":
              bot.reply_to(message, "دکمه 2 در حال run شدن است")
              # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, hide_keyboard=True)
              bot.send_message(message.chat.id, "Keyboard hidden")
           else:
               bot.reply_to(message, f"your message is {message.text}")
    

# create the keyboard

@bot.message_handler(content_types=['contact'])
def get_contact(message):
    # contact = message.contact
    # انجام کاری با اطلاعات مخاطب
    # bot.send_message(message.chat.id, f"Contact received: {contact.first_name} {contact.last_name} {contact.phone_number}")
    if message.contact:
         
        with sqlite3.connect('user.db') as connection:
            cursor = connection.cursor()
            insert_data_query="""  
            INSERT OR IGNORE INTO users(id,first_name,last_name,phone_number)
            VALUES (?, ?, ?, ?)

            """
            data=(
            message.contact.user_id,
            f'{message.contact.first_name}',
            f'{message.contact.last_name}',
            f'{message.contact.phone_number}'
            )
            cursor.execute(insert_data_query, data)
    else:
       bot.message_handler(message.chat.id, "No contact information provided")
# creat database





@bot.message_handler(commands=["admin2024435"])
def update_send(message):
  for id in user_ID:
    
    bot.send_message(id,"محصول موجود شد")


# def procses_name(message):
#   name=message.text
#   bot.send_message(message.chat.id,f"سلام {name } چند سالت هست؟")
#   bot.register_next_step_handler(message,process_job)
#   bot.send_message(message,"لطفا شغل خود را بگویید")

# def process_job(message):
#   job=message.text
#   bot.send_message(message.chat.id,f"{job}شغل خیلی خوبی است")

# gemini


# @bot.message_handler(regexp=r"\b[A-Za-zάέήίόϋώήΰğşçİĞŞÇ]+\b")
# def handle_message(message):
#     # Extract matched names
#     names = re.findall(r"\b[A-Za-zάέήίόϋώήΰğşçİĞŞÇ]+\b", message.text)

#     # Process or respond to the extracted names
#     if names:
#         n1 = [f"سلام به {name}!" for name in names]
#         response_message = "\n".join(n1)
#         bot.reply_to(message, response_message)
#     else:
#         # No names were found in the message
#         pass


# @bot.message_handler(regexp="اخوان|سپیده")
# def handle_message(message):
#   bot.reply_to(message,"اخوان در حال پیام دادن است")



# @bot.message_handler(content_types=["document","audio"])
# def handle_docs_audio(message):
#   if message.audio:
#     bot.reply_to(message,"this is audio file")
#   elif message.document:
#     bot.reply_to(message,"this is document file")

# # Handles all messages for which the lambda returns True
# @bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
# def handle_text_doc(message):
#   bot.reply_to(message, "This is a text file")

# # Which could also be defined as:
# def test_message(message):  
#   return message.document.mime_type == 'text/plain'


# @bot.message_handler(func=lambda msg: msg.text == "😂")
# @bot.message_handler(commands=['hello'])
# def send_something(message):
#     bot.reply_to(message, 'Emoji')


bot.polling()