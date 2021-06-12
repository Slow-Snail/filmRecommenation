import numpy as np
import pandas as pd
import NameWork
import FilmRecommendetion

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")


class ConsInt:
    def __init__(self, Mid, Nid, Pop):
        self.Mid = Mid
        self.Nid = Nid
        self.Pop = Pop
        self.nameWork = NameWork.NameWork(ratings, movies, Mid, Nid, Pop)
        self.filmRecommendation = FilmRecommendetion.FilmRecommendation(ratings)

    def control(self):

        cin = []  # массив индексов просмотренных пользователем фильмов.
        score = []  # оценки пользователя
        names = []  # фильмы, которые выбрал пользователь

        while True:
            N = input()
            if N == '-1':
                break
            var = self.nameWork.search(N.lower(), names)
            var = sorted(var, key=lambda x: self.Pop[self.Nid[x]], reverse=True)
            print(var)
            k = int(input())
            if k == -1:
                continue
            k = var[k - 1].lower()
            cin.append(self.Nid[k])  # ✔
            names.append(k)
            # Защита от дураков
            k = input()
            if k.lower() != k.upper():
                print('ERROR! Pls, put a rating!')
                k = input()  # Дважды не повторяю

            score.append(int(k))
            var.sort()  # ??????

        GC = self.nameWork.favourite(names)  # map жанр => колв-во

        print(names)  # ✔ # фильмы, которые выбрал пользователь
        print(cin)  # ✔ # массив индексов просмотренных пользователем фильмов
        print(score)  # ✔ # оценки пользователя
        # id = (filmRecommendation.make_predict(cin, score))  # ✔
        id = sorted(self.filmRecommendation.make_predict(cin, score, -1), key=lambda x: self.nameWork.sort(x, GC),
                    reverse=True)   # Id рекомендованных фильмов
        # id = self.nameWork.psort(id)  # len(psort(id)) == min(25, len(id))
        # не эффективно. мб 25 слишком много для такой базы данных
        ans = []
        print(id)
        for i in id:
            ans.append(movies['title'][self.Mid[i]].lower())    # переводим в названия
        print(ans)  # названия рекомендовонных фильмов
