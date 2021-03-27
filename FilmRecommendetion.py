import numpy as np
import pandas as pd


class FilmRecommendation:
    def __init__(self, ratings):
        self.ratings = ratings

    def createPR(self, cin, score):
        PR = np.full((611, len(cin)), 2.5)  # 610 == кол-во людей ✔
        # мб заполнять средним балом по фильму
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
        dis = np.zeros((611, 2))
        for i in range(len(dis)):  # номер человека
            n = 0
            for j in range(number_of_films):  # координата
                n += (PR[0][j] - PR[i][j]) ** 2
            dis[i][0] = n ** 0.5
            dis[i][1] = i

        dis = sorted(dis, key=lambda x: x[0])
        return dis

        # dis [0(dis U2U), dis to 1, to 2, to 3][0,1,2,3]
        # dis[][0] = ((PR[0][] - PR[][]) ** 2 + same)  ** 0,5

    def get_liked_film(self, num, cin):
        n = -1  # n = номер строки в ratings
        sco = np.zeros((193609, 2)) # массив с сумарными оценками # наибольший MovieId
        for i in range(len(sco)):
            sco[i][1] = i
        qua = np.zeros(193609)   # кол-во оценок у фильма

        for i in self.ratings['userId']:
            n += 1  # n = номер строки в ratings
            if i in num:    # если человек, оценивший фильм, один из ближайших
                sco[self.ratings['movieId'][n]][0] += int(self.ratings['rating'][n])    # добавляем его оценку
                qua[self.ratings['movieId'][n]] += 1    # и увеличиваем количество оценок у фильма на 1

        for i in range(len(sco)):   # идём по оценкам
            if(qua[i]) != 0:    # если фильм смотрел кто-то из ближайших людей
                sco[i][0] = sco[i][0] / qua[i]  # считаем среднюю оценк фильма
        sco = sorted(sco, key=lambda x: x[0], reverse=True)  # сортируем фильмы по средней оценке
        ans = []
        for i in range(100):    # берём 100 фильмов с наивысшей оценкой
            if not(sco[i][1] in cin):   # если пользователь не смотрел фильм
                ans.append(sco[i][1])   # добовляем его в рекомендации
        return ans

    def make_predict(self, cin, score):
        PR = self.createPR(cin, score)  # PR[[user id] [score1,score2,score3...]]
        dis = self.count_dist(PR, len(cin))  # num = номер ближайшего человека

        n = 5                               # n - кол-во ближайших людей, оценки которых мы учитываем

        num = []
        for i in range(1, min(n, len(dis))):
            num.append(dis[i][1])

        return self.get_liked_film(num, cin)  # возвращает массив номеров фильмов


