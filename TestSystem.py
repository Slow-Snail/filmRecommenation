import numpy as np
import pandas as pd
import NameWork
import FilmRecommendetion
import random

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

class TestSystem:
    def __init__(self,  Mid, Nid, Pop):
        self.Mid = Mid
        self.nameWork = NameWork.NameWork(ratings, movies, Mid, Nid, Pop)
        self.filmRecommendation = FilmRecommendetion.FilmRecommendation(ratings)
        self.Pop = Pop

    def test(self):
        agr = 0  # процент гарантированно верно подобранных фильмов
        dagr = 0  # процент гарантированно верно подобранных фильмов
        p = 0
        k = -1  # номер человека
        f = 0  # номер строки в ratings
        strnum = []  # номера строк, принадлежащих человеку
        while k < 609:  # идём по людям
            k += 1
            while int(ratings['userId'][f]) == k+1:   # пока строка f принадлежит человеку k
                strnum.append(f)  # записываем номер строки
                f += 1  # переходим к следующей строке
                if f == 100836:  # избегаем выхода за границу
                    break
            strnum = sorted(strnum, key=lambda x: random.uniform(1, 100))  # rand sort
            que = []  # номера строк, которые мы используем как дано
            ans = []  # номера строк, которые мы используем для проверки
            for i in range(len(strnum)):
                if i < len(strnum)/2:  # половина сюда, половина туда ¯\_(ツ)_/¯
                    que.append(strnum[i])
                else:
                    ans.append(strnum[i])

            Sco = {ratings['movieId'][strnum[i]]: ratings['rating'][strnum[i]] for i in range(len(strnum))}  # map: id фильма => оценка человека

            cin = []    # массив индексов просмотренных пользователем фильмов
            score = []  # оценки пользователя
            names = []  # фильмы, которые выбрал пользователь

            for i in que:
                cin.append(ratings['movieId'][i])
                score.append(ratings['rating'][i])

            for i in cin:
                names.append(movies['title'][self.Mid[i]].lower())

            GC = self.nameWork.favourite(names)
            # print(self.filmRecommendation.make_predict(cin, score, 1))
            res = sorted(self.filmRecommendation.make_predict(cin, score, 1), key=lambda x: self.nameWork.sort(x, GC),
                        reverse=True)  # аналогично с ConsInt // res = id рекомендованных фильмов
            # res = self.filmRecommendation.make_predict(cin, score, 1)

            uf = []
            for i in ans:
                uf.append(ratings['movieId'][i])    # uf = номера фильмов для проверки
            for i in range(min(25, len(res))):  # в первых 25 рекомендованных фильмах
                p += self.Pop[res[i]]
                if res[i] in uf:  # если мы знаем оценку i-ного фильма
                    if Sco[res[i]] > 3.5:  # и она больше 3.5
                        agr += 4  # i-ный фильм действительно понравился пользователю
                    else:
                        dagr += 4

            print(k)

            strnum.clear()  # новый челоек - новые номера строк
        print('res')
        print(p/610)
        print(agr/610)
        print(dagr/610)
