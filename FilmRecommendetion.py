import numpy as np
import random

class FilmRecommendation:
    def __init__(self, ratings):
        self.ratings = ratings

    def createPR(self, cin):
        Rai = {i: 0 for i in cin}  # Суммарная оценка фильмов пользователя
        Qua = {i: 0 for i in cin}  # Кол-во оценок
        n = -1
        for i in self.ratings['movieId']:  # идём по ratings movieId
            n += 1  # номер строки
            if i in cin:  # Если это ^ фильм пользователя
                Qua[i] += 1  # Увеличиваем кол-во оценок фильма на 1
                Rai[i] += self.ratings['rating'][n]  # прибавляем оценку
        v = []  # массив средних оценок
        for i in cin:  # идём по фильмам пользователя
            v.append(Rai[i] / Qua[i])  # добавляем среднюю оценку в PR
        PR = np.full((611, len(cin)), v)  # создаём PR
        return PR

    def fillPR(self, cin, score):
        # PR = np.full((611, len(cin)), 2.5)  # 610 == кол-во людей ✔
        PR = self.createPR(cin)

        PR[0] = score  # PR[0] = оценки пользователя

        for i in range(len(cin)):
            num = 0  # num - кол во срабатываний цикла j // номер строки с фильмом j
            # i - номер фильма пользователя (первый фильм который выбрал ползователь, второй...)

            for j in self.ratings['movieId']:  # j номер фильма    ✔

                if str(j) == str(cin[i]):  # если фильм j это фильм пользователя

                    PR[self.ratings['userId'][num]][i] = str(self.ratings['rating'][
                                                                 num])  # записываем в пользователя оценившего фильм j его оценку под номером, равным номеру фильма пользователя (i) ✔
                num += 1

        # pr[[user id] [score1,score2,score3...]]
        return PR

    def count_dist(self, PR):
        dis = np.zeros((611, 2))
        for i in range(len(dis)):
            dis[i][0] = np.linalg.norm(PR[0] - PR[i])  # расстояние до
            dis[i][1] = i  # номер человека

        dis = sorted(dis, key=lambda x: x[0])

        # dis = sorted(dis, key=lambda x: random.uniform(1, 100))
        # for i in range(len(dis)):
        #    print(dis[i][0], dis[i][1])
        return dis

        # dis [0(dis U2U), dis to 1, to 2, to 3][0,1,2,3]
        # dis[][0] = ((PR[0][] - PR[][]) ** 2 + same)  ** 0,5

    def get_liked_film(self, num, cin):
        n = -1  # n = номер строки в ratings
        sco = np.zeros((193609 + 1, 2))  # sco[i][0] = сумарная оценка фильма с номером i; sco[i][1] = номер фильма
        for i in range(len(sco)):
            sco[i][1] = i
        qua = np.zeros(193609 + 1)  # кол-во оценок у фильма

        for i in self.ratings['userId']:  # идём по строкам ratings;
            n += 1  # n = номер строки

            if i in num:  # если человек, оценивший фильм, один из ближайших
                sco[self.ratings['movieId'][n]][0] += int(
                    self.ratings['rating'][n])  # добавляем его оценку к фильму который он посмотрел
                qua[self.ratings['movieId'][n]] += 1  # и увеличиваем количество оценок у фильма на 1

        for i in range(len(sco)):  # идём по оценкам
            if (qua[i]) != 0:  # если фильм смотрел кто-то из ближайших
                sco[i][0] = sco[i][0] / qua[i]  # считаем среднюю оценку фильма
        sco = sorted(sco, key=lambda x: x[0], reverse=True)  # сортируем фильмы по средней оценке
        ans = []
        for i in range(100):  # берём 100 фильмов с наивысшей оценкой
            if not (sco[i][1] in cin) and int(qua[int(sco[i][1])]) != 0:  # если пользователь не смотрел фильм
                ans.append(sco[i][1])  # добовляем его в рекомендации
        return ans

    def make_predict(self, cin, score, tst):
        PR = self.fillPR(cin, score)  # PR[[user id] [score1,score2,score3...]]
        dis = self.count_dist(PR)  # dis = [0]-расстояние до человека [1]-id (отсортирован по ближайшим)

        n = 4 + 1  # n - кол-во ближайших людей, оценки которых мы учитываем (-1)

        num = []  # id ближайших n человек
        if tst == -1:
            for i in range(1, min(n, len(dis))):
                num.append(dis[i][1])
        else:
            for i in range(2, min(n + 1, len(dis))):
                num.append(dis[i][1])
        print(num)
        return self.get_liked_film(num, cin)  # возвращает массив номеров фильмов
