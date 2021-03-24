import numpy as np
import pandas as pd


class NameWork:
    def __init__(self, ratings, movies, Mid, Nid):
        self.ratings = ratings
        self.movies = movies
        self.Mid = Mid
        self.Nid = Nid

    def search(self, string, alrd):
        pure = []
        names = list(map(lambda x: x.lower(), self.movies['title']))
        for i in range(len(string)):           # i = номер символа названия
            for j in range(len(names)):        # j = номер названия
                if len(names[j]) >= len(string) and names[j][i] == string[i]:    # Если i-ная буква j-йного Названия = i-ной букве искомого названия
                    pure.append(names[j])       # j-йное название проходит на следующий этап поиска.

            names.clear()
            for j in pure:
                names.append(j)  # names = pure

            pure.clear()

        ans = [x for x in names if not (x in alrd)]
        return ans

    def favourite(self, films):
        allg = []
        for i in films:
            s = self.movies['genres'][self.Mid[self.Nid[i]]] # s = жанры фильма i из фильмов, выбранных пользователем
            k = s.split('|')
            for j in k:
                allg.append(j)
        genres = {"Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western", "(no genres listed)", "IMAX"}
        count = {a: 0 for a in genres}
        for i in allg:
            count[i] += 1
        return count    # map жанр => колв-во

    def sort(self, id, count):
        k = self.movies['genres'][self.Mid[id]].split('|')
        ans = 0
        for i in k:
            ans += count[i]
        return ans
