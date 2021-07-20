import numpy as np
import pandas as pd
import telebot as tb
from telebot.types import InlineKeyboardMarkup as kb
from telebot.types import InlineKeyboardButton as bt
import NameWork
import FilmRecommendetion
import Data

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
bot = tb.TeleBot('')  # Токен

Mid = {movies['movieId'][i]: i for i in range(len(movies['movieId']))}  #  создание ключей по типу "ключ - movieId;; вывод - реальный номер (по счёту)"
Nid = {movies['title'][i].lower(): movies['movieId'][i] for i in range(len(movies['movieId']))} #  ключ - название. вывод - id фильма
Pop = {movies['movieId'][i]: 0 for i in range(len(movies['movieId']))}
Sco = {movies['movieId'][i]: 0 for i in range(len(movies['movieId']))}
l = 0
for i in ratings['movieId']:
    Pop[i] += 1
    Sco[i] += ratings['rating'][l]
    l += 1
for i in movies['movieId']:
    if Pop[i]>0:
        Sco[i] = Sco[i]/Pop[i]

nameWork = NameWork.NameWork(ratings, movies, Mid, Nid, Pop, Sco)
filmRecommendation = FilmRecommendetion.FilmRecommendation(ratings)

STC = {}
DMP = {}


@bot.message_handler(content_types=['text'])
def start(message):

    if not (message.from_user.id in DMP):
        DMP[message.from_user.id] = Data
        DMP[message.from_user.id].alrd = []
        DMP[message.from_user.id].score = []
        DMP[message.from_user.id].cin = []

    if not (message.from_user.id in STC) or STC[message.from_user.id] == 0:
        DMP[message.from_user.id] = Data
        DMP[message.from_user.id].alrd = []
        DMP[message.from_user.id].score = []
        DMP[message.from_user.id].cin = []
        branch_kb = kb()
        branch_kb.add(bt(text='Да', callback_data='yes'))
        branch_kb.add(bt(text='Нет', callback_data='no'))
        bot.send_message(message.from_user.id, 'Привет! Я помогу тебе выбрать фильм для просмотра.' +
                                               ' Можешь назвать свои любимые кинокартины?', reply_markup=branch_kb)


    elif STC[message.from_user.id] == 1:
        if 4 > len(message.text) > 1 and check(message.text[1:]) and 16 > int(message.text[1:]) > 0:
            if (message.text[0].lower() == "a" or message.text[0].lower() == "а") and not (DMP[message.from_user.id].vv[int(message.text[1:]) + 14].lower() in DMP[message.from_user.id].alrd):
                DMP[message.from_user.id].alrd.append(DMP[message.from_user.id].vv[int(message.text[1:]) - 1].lower())
                bot.send_message(message.from_user.id, 'Какую оценку ты поставишь этому фильму по десятибалльной шкале?')
                bot.register_next_step_handler(message, scr)
            elif (message.text[0].lower() == "b" or message.text[0].lower() == "в") and not (DMP[message.from_user.id].vv[int(message.text[1:]) + 14].lower() in DMP[message.from_user.id].alrd):
                DMP[message.from_user.id].alrd.append(DMP[message.from_user.id].vv[int(message.text[1:]) + 14].lower())
                bot.send_message(message.from_user.id, 'Какую оценку ты поставишь этому фильму по десятибалльной шкале?')
                bot.register_next_step_handler(message, scr)
            else:
                bot.send_message(message.from_user.id, 'Ошибка, попробуй ещё раз')
        else:
            bot.send_message(message.from_user.id, 'Ошибка, попробуй ещё раз')

    elif STC[message.from_user.id] == 2:
        v = nameWork.search(message.text.lower(), DMP[message.from_user.id].alrd)
        v = sorted(v, key=lambda x: Pop[Nid[x]], reverse=True)
        DMP[message.from_user.id].v = v
        if len(v) == 0:
            bot.send_message(message.from_user.id, 'Ничего не найдено! Попробуй ещё раз или пропусти этот фильм, возможно я просто его не знаю')
        else:
            bot.send_message(message.from_user.id, 'Возможно, вы имели ввиду:')
            for i in range(min(5, len(v))):
                bot.send_message(message.from_user.id, str(i+1)+': '+v[i])
            bot.send_message(message.from_user.id, 'Если среди предложенных фильмов нет того что ты искал' +
                                                   ' - напиши "Нет" или "No"')
            bot.register_next_step_handler(message, choice)


def choice(message):
    if message.text.lower() == 'нет' or message.text.lower() == 'no':
        bot.send_message(message.from_user.id, 'Напиши несколько первых букв названия фильма, что бы я его нашёл')
    elif 2 > len(message.text) and check(message.text) and 0 < int(message.text) <= min(len(DMP[message.from_user.id].v), 5):
        DMP[message.from_user.id].alrd.append(DMP[message.from_user.id].v[int(message.text)-1].lower())
        DMP[message.from_user.id].cin.append(Nid[DMP[message.from_user.id].v[int(message.text) - 1].lower()])
        bot.send_message(message.from_user.id, 'Какую оценку ты поставишь этому фильму по десятибалльной шкале?')
        bot.register_next_step_handler(message, scr)

    else:
        bot.send_message(message.from_user.id, 'Номер указан неверно, попробуйте ещё раз')
        bot.register_next_step_handler(message, choice)


def scr(message):
    if not(3 > len(message.text) and check(message.text) and 0 <= int(message.text) <= 10):
        bot.send_message(message.from_user.id, 'Оценка за пределами десятибалльной шкалы, введи другую оценку')
        bot.register_next_step_handler(message, scr)
    else:
        DMP[message.from_user.id].score.append(int(message.text)/2)
        last_kb = kb()
        last_kb.add(bt(text='Это всё', callback_data='end'))
        if STC[message.from_user.id] == 2:
            bot.send_message(message.from_user.id,
                         'Введи название следующего фильма или используй кнопку чтобы продолжить', reply_markup=last_kb)
        else:
            DMP[message.from_user.id].cin.append(Nid[DMP[message.from_user.id].alrd[len(DMP[message.from_user.id].alrd)-1].lower()])
            bot.send_message(message.from_user.id,
                        'Введи номер следующего фильма или используй кнопку чтобы продолжить', reply_markup=last_kb)


def check(s):
    for i in s:
        if not(i=='0' or i=='1' or i=='2' or i=='3' or i=='4' or i=='5' or i=='6' or i == '7' or i == '8' or i == '9'):
            return False
    return True


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if not (call.message.chat.id in DMP):
        DMP[call.message.chat.id] = Data
        DMP[call.message.chat.id].alrd = []
        DMP[call.message.chat.id].score = []
        DMP[call.message.chat.id].cin = []

    if call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Напиши несколько первых букв названия фильма, что бы я его нашёл')
        DMP[call.message.chat.id].alrd = []
        DMP[call.message.chat.id].score = []
        DMP[call.message.chat.id].cin = []
        STC[call.message.chat.id] = 2

    if call.data == 'no':


        genre_kb = kb()
        genre_kb.add(bt(text='Боевик', callback_data='Action'))  # 1828
        genre_kb.add(bt(text='Приключенческий', callback_data='Adventure'))  # 1263
        genre_kb.add(bt(text='Анимация', callback_data='Animation'))  # 611
        genre_kb.add(bt(text='Детский', callback_data='Children'))  # 664
        genre_kb.add(bt(text='Комедия', callback_data='Comedy'))  # 3756
        genre_kb.add(bt(text='Криминальный', callback_data='Crime'))  # 1199
        genre_kb.add(bt(text='Документальный', callback_data='Documentary'))  # 440
        genre_kb.add(bt(text='Драма', callback_data='Drama'))  # 4361
        genre_kb.add(bt(text='Фантастика', callback_data='Fantasy'))  # 779
        genre_kb.add(bt(text='Нуар', callback_data='Film-Noir'))  # 87
        genre_kb.add(bt(text='Ужасы', callback_data='Horror'))  # 978
        genre_kb.add(bt(text='Мюзикл', callback_data='Musical'))  # 334
        genre_kb.add(bt(text='Мистика', callback_data='Mystery'))  # 573
        genre_kb.add(bt(text='Романтика', callback_data='Romance'))  # 1596
        genre_kb.add(bt(text='Научная фантастика', callback_data='Sci-Fi'))  # 980
        genre_kb.add(bt(text='Триллер', callback_data='Thriller'))  # 1894
        genre_kb.add(bt(text='Фильмы про войну', callback_data='War'))  # 382
        genre_kb.add(bt(text='Вестерн', callback_data='Western'))  # 167
        bot.send_message(call.message.chat.id, 'Тогда давай сначала определимся с жанром, который тебе интересен.',
                         reply_markup=genre_kb)
    if call.data == "Action" or call.data == "Adventure" or call.data == "Animation" or call.data == "Children" or call.data == "Comedy" or call.data == "Crime" or call.data == "Documentary" or call.data == "Drama" or call.data == "Fantasy" or call.data == "Film-Noir" or call.data == "Horror" or call.data == "Musical" or call.data == "Mystery" or call.data == "Romance" or call.data == "Sci-Fi" or call.data == "Thriller" or call.data == "War" or call.data == "Western":
        vv = nameWork.gensearch(call.data)
        # 0-14 - 15 фильмов по популярности, 15-29 - 15 фильмов по рейтингу (могут совпадать)
        DMP[call.message.chat.id].vv = vv
        bot.send_message(call.message.chat.id, 'Вот список популярных фильмов этого жанра: \n\nА1: '+vv[0]+'\nА2: '+vv[1]+'\nА3: '+vv[2]+'\nА4: '+vv[3]+'\nА5: '+vv[4]+'\nА6: '+vv[5]+'\nА7: '+vv[6]+'\nА8: '+vv[7]+'\nА9: '+vv[8]+'\nА10: '+vv[9]+'\nА11: '+vv[10]+'\nА12: '+vv[11]+'\nА13: '+vv[12]+'\nА14: '+vv[13]+'\nА15: '+vv[14]
                         + '\n\nА это список высокооцененных фильмов:\n\nB1: '+vv[15]+'\nB2: '+vv[16]+'\nB3: '+vv[17]+'\nB4: '+vv[18]+'\nB5: '+vv[19]+'\nB6: '+vv[20]+'\nB7: '+vv[21]+'\nB8: '+vv[22]+'\nB9: '+vv[23]+'\nB10: '+vv[24]+'\nB11: '+vv[25]+'\nB12: '+vv[26]+'\nB13: '+vv[27]+'\nB14: '+vv[28]+'\nB15: '+vv[29]
                         + '\n\nЕсли ты смотрел какой-то из этих фильмов - напиши мне его номер \n(Примеры номеров:' +
                         '"A3"; "B11")\nЕсли ты уже выбрал фильмы - напиши "Это всё"')
        STC[call.message.chat.id] = 1
        DMP[call.message.chat.id].alrd = []
        DMP[call.message.chat.id].score = []
        DMP[call.message.chat.id].cin = []

    if call.data == 'end':
        if len(DMP[call.message.chat.id].alrd) > 0:
            bot.send_message(call.message.chat.id, 'Вам должны понравиться эти фильмы:')
            GC = nameWork.favourite(DMP[call.message.chat.id].alrd)
            id = sorted(filmRecommendation.make_predict(DMP[call.message.chat.id].cin,
                                                        DMP[call.message.chat.id].score, -1),
                        key=lambda x: nameWork.sort(x, GC), reverse=True)
            print(DMP[call.message.chat.id].alrd)  # фильмы, которые выбрал пользователь
            print(DMP[call.message.chat.id].cin)  # массив индексов просмотренных пользователем фильмов
            print(DMP[call.message.chat.id].score)  # оценки пользователя
            print(id)
            for i in range(min(10, len(id))):
                bot.send_message(call.message.chat.id, movies['title'][Mid[id[i]]])
        STC[call.message.chat.id] = 0


bot.polling()
