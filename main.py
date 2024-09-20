import os
import telebot
from dotenv import load_dotenv
from telebot import types
from quiz_data import questions
from messages import message_start, message_help
from http.server import test, SimpleHTTPRequestHandler
import time

load_dotenv()

API_TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot("7180931590:AAHOlMy5dyshIW3dE_9Tft3JXa7PqmMmuEg")

quiz_states = {}

class QuizState:
    def __init__(self, current_question=0, correct_answer=0):
        self.current_question = current_question
        self.correct_answer = correct_answer
        self.start_time = time.time()
@bot.message_handler(commands=["start"])
def start_command_handler(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=message_start
        
    )
    
    
@bot.message_handler(commands=["help"])
def help_command_handler(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=message_help
    )
@bot.message_handler(commands=["start_quiz"])
def start_quiz_command_handler(message):
    user_id = message.chat.id
    quiz_states[user_id] = QuizState()
    send_question(user_id)
def send_question(user_id):
    state = quiz_states[user_id]
    question = questions[state.current_question]
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(question["options"][0], callback_data="0")
    item2 = types.InlineKeyboardButton(question["options"][1], callback_data="1")
    item3 = types.InlineKeyboardButton(question["options"][2], callback_data="2")
    item4 = types.InlineKeyboardButton(question["options"][3], callback_data="3")
    markup.add(item1, item2, item3, item4)
    bot.send_message(
        chat_id=user_id,
        text=question["question"],
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    state = quiz_states[user_id]
    question = questions[state.current_question]
    if int(call.data) == question["correct_option"]:
        state.correct_answer += 1
        bot.send_message(user_id, text="Правильный ответ!")
    else:
        bot.send_message(user_id, text="Вы неправильно ответили!")
    state.current_question += 1
    if state.current_question < len(questions):
        send_question(user_id)
    else:
        end_time = time.time()
        sub_time = round(end_time - state.start_time) 
        bot.send_message(user_id, text=f"Тест завершен, вы ответили на {state.correct_answer} вопросов правильно из {len(questions)} вопросов за {sub_time} секунд")
        del quiz_states[user_id]

bot.polling()

