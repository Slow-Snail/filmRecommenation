import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import NameWork
import FilmRecommendetion

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
# ratings['rating'].hist()
# plt.show()

Mid = {movies['movieId'][i]: i for i in range(len(movies['movieId']))}  #  создание ключей по типу "ключ - movieId;; вывод - реальный номер (по счёту)"
Nid = {movies['title'][i].lower(): movies['movieId'][i] for i in range(len(movies['movieId']))} #  ключ - название. вывод - id фильма
Pop = {movies['movieId'][i]: 0 for i in range(len(movies['movieId']))}
for i in ratings['movieId']:
    Pop[i] += 1

#cin = input().split()  # cin это массив индексов просмотренных пользователем фильмов. ✔
#score = input().split()  # оценки пользователя
#string = {input().lower()}

nameWork = NameWork.NameWork(ratings, movies, Mid, Nid)
filmRecommendation = FilmRecommendetion.FilmRecommendation(ratings)
# print(filmRecommendation.make_predict(cin, score)) # Названия подходящих фильмов
# print(nameWork.search(string.lower())) # Названия подходящие под искомое

cin = []
score = []
names = []

while True:
    N = input()
    if N == '-1':
        break
    var = nameWork.search(N.lower(), names)
    var = sorted(var, key=lambda x: Pop[Nid[x]], reverse=True)
    print(var)
    k = int(input())
    if k == -1:
        continue
    k = var[k - 1].lower()
    cin.append(Nid[k])  # ✔
    names.append(k)
    # Защита от дураков (Console only)
    k = input()
    if k.lower() != k.upper():
        print('ERROR! Pls, put a rating!')
        k = input()  # Дважды не повторяю

    score.append(int(k))
    var.sort()

GC = nameWork.favourite(names)    # map жанр => колв-во

print(names)    # ✔ # фильмы, которые выбрал пользователь
print(cin)      # ✔ # массив индексов просмотренных пользователем фильмов
print(score)    # ✔ # оценки пользователя
# id = (filmRecommendation.make_predict(cin, score))  # ✔
id = sorted(filmRecommendation.make_predict(cin, score), key=lambda x:nameWork.sort(x, GC), reverse=True)
ans = []
print(id)
for i in id:
    ans.append(movies['title'][Mid[i]].lower())
print(ans)  # названия рекомендовонных фильмов
