import numpy as np
import pandas as pd


class FilmRecommendation:
    def __init__(self, ratings):
        self.ratings = ratings

    def createPR(self, cin, score):
        PR = np.zeros((611, len(cin)))  # 610 == кол-во людей ✔
        # заполнение массива 2.5, мб заполнять средним балом по фильму
        for i in range(len(PR)):
            for j in range(len(PR[i])):
                PR[i][j] = 2.5

        PR[0] = score  # PR[0] = оценки пользователя

        for i in range(len(cin)):
            num = 0  # num - кол во срабатываний цикла j // номер строки с фильмом j
            # i - номер фильма пользователя (первый фильм который выбрал ползователь, второй...)

            for j in self.ratings['movieId']:  # j номер фильма    ✔

                if str(j) == str(cin[i]):  # если фильм j это фильм пользователя

                    PR[self.ratings['userId'][num]][i] = str(self.ratings['rating'][num])  # записываем в пользователя оценившего фильм j его оценку под номером, равным номеру фильма пользователя (i) ✔
                num += 1

        # pr[[user id] [score1,score2,score3...]]
        return PR

    def count_dist(self, PR, number_of_films):
        dis = np.zeros(611)  # ✔
        for i in range(len(dis)):  # номер человека
            n = 0
            for j in range(number_of_films):  # координата
                n += (PR[0][j] - PR[i][j]) ** 2
            dis[i] = n ** 0.5
        min = 10000;
        num = 0;
        for i in range(1, len(dis)):
            if min > dis[i]:
                min = dis[i]
                num = i
        return num
        # dis [0(dis U2U), dis to 1, to 2, to 3]
        # dis[] = ((PR[0][] - PR[][]) ** 2 + same)  ** 0,5

    def get_liked_film(self, num, cin):
        aspirant = []
        n = -1
        for i in self.ratings['userId']:
            n += 1  # n = номер строки
            if num == i and self.ratings['rating'][n] > 4:
                b = 1
                for j in cin:
                    if str(self.ratings['movieId'][n]) == j:
                        b = 0
                if b:
                    aspirant.append(self.ratings['movieId'][n])
        return aspirant

    def make_predict(self, cin, score):
        PR = self.createPR(cin, score)  # PR[[user id] [score1,score2,score3...]]
        num = self.count_dist(PR, len(cin))  # num = номер ближайшего человека
        # ans = []
        return self.get_liked_film(num, cin)  # возвращает массив номеров фильмов


