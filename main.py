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

while 1 == 1:
    N = input()
    if N == '-1':
        break
    var = nameWork.search(N.lower(), names)
    var = sorted(var, key=lambda x: Pop[Nid[x]], reverse=True)
    print(var)
    K = int(input())
    if K == -1:
        continue
    K = var[K-1].lower()
    cin.append(Nid[K])  # ✔
    names.append(K)
    # Защита от дураков (Console only)
    K = input()
    if(K.lower() != K.upper()):
        print('ERROR! Pls, put a rating!')
        K = input()  # Дважды не повторяю

    score.append(int(K))
    var.sort()

#  [59784, 87222, 149406, 76093, 112175]
#  [5, 5, 4, 5, 4]

GC = nameWork.favourite(names)    # map жанр => колв-во

print(names)    # ✔
print(cin)      # ✔
print(score)    # ✔
print(filmRecommendation.make_predict(cin, score))  # ✔
id = sorted(filmRecommendation.make_predict(cin, score), key=lambda x:nameWork.sort(x, GC), reverse=True)
ans = []
for i in id:
    ans.append(movies['title'][Mid[i]].lower())
print(ans)
# PR = np.zeros((611, len(cin)))  # 610 == кол-во людей ✔
# dis = np.zeros(611)    # ✔
# aspirant = []
#
#
# def inp():
#
#     # заполнение массива 2.5, мб заполнять средним балом по фильму
#     for i in range(len(PR)):
#         for j in range(len(PR[i])):
#             PR[i][j] = 2.5
#
#     PR[0] = score #PR[0] = оценки пользователя
#
#
#
#     for i in range(len(cin)):
#         num = 0 #num - кол во срабатываний цикла j // номер строки с фильмом j
#                 #i - номер фильма пользователя (первый фильм который выбрал ползователь, второй...)
#
#         for j in ratings['movieId']: #j номер фильма    ✔
#
#             if str(j) == cin[i]: #если фильм j это фильм пользователя
#
#
#                 PR[ratings['userId'][num]][i] = str(ratings['rating'][num]) #записываем в пользователя оценившего фильм j его оценку под номером, равным номеру фильма пользователя (i) ✔
#             num +=1
#
#      #pr[[user id] [score1,score2,score3...]]
#
# def count():
#     for i in range(len(dis)): #номер человека
#         n = 0
#         for j in range(len(cin)):    #координата
#             n += (PR[0][j] - PR[i][j]) ** 2
#         dis[i] = n ** 0.5
#     min = 10000;
#     num = 0;
#     for i in range(1, len(dis)):
#         if min > dis[i]:
#             min = dis[i]
#             num = i
#     return (num)
#     #dis [nothing, dis to 1, to 2, to 3]
#     #dis[] = ((PR[0][] - PR[][]) ** 2 + same)  ** 0,5
#
# def selection (num):
#     n = -1
#     for i in ratings['userId']:
#         n += 1
#         if num == i and ratings['rating'][n] > 4:
#             aspirant.append(ratings['movieId'][n])
#
# def sort():
#     pass
#
#
#
# inp()   # ✔
# selection(count())  # ✔
# sort()
