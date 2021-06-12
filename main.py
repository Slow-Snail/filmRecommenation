import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ConsInt
import TestSystem

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
# ratings['rating'].hist()
# plt.show()

Mid = {movies['movieId'][i]: i for i in range(len(movies['movieId']))}  #  создание ключей по типу "ключ - movieId;; вывод - реальный номер (по счёту)"
Nid = {movies['title'][i].lower(): movies['movieId'][i] for i in range(len(movies['movieId']))} #  ключ - название. вывод - id фильма
Pop = {movies['movieId'][i]: 0 for i in range(len(movies['movieId']))}
for i in ratings['movieId']:
    Pop[i] += 1

def choice():
    k = input()
    if k == "1":
        print('launching the program...')
        consInt.control()
        return
    if k == "-1":
        print('starting testing...')
        testSysytem.test()
        print('testing completed.')
        return
    else:
        print('Error, invalid key! Try again... (1 or -1)')
        choice()

consInt = ConsInt.ConsInt(Mid, Nid, Pop)
testSysytem = TestSystem.TestSystem(Mid, Nid, Pop)
choice()

# print(filmRecommendation.make_predict(cin, score)) # Названия подходящих фильмов
# print(nameWork.search(string.lower())) # Названия подходящие под искомое
