import numpy as np
import pandas as pd


class NameWork:
    def __init__(self, ratings, movies, Mid, Nid, Pop, Sco):
        self.ratings = ratings
        self.movies = movies
        self.Mid = Mid
        self.Nid = Nid
        self.Pop = Pop
        self.Sco = Sco

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
            s = self.movies['genres'][self.Mid[self.Nid[i]]]  # s = жанры фильма i из фильмов, выбранных пользователем
            k = s.split('|')
            for j in k:
                allg.append(j)
        genres = {"Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western", "(no genres listed)", "IMAX"}
        count = {a: 0 for a in genres}
        for i in allg:
            if(i != "IMAX" and i != "(no genres listed)"):
                count[i] += 1
        return count    # map жанр => колв-во

    def sort(self, id, count):
        k = self.movies['genres'][self.Mid[id]].split('|')
        ans = 0
        for i in k:
            ans += count[i]
        return ans

    def psort(self, inp):
        id = []
        for i in range(25):
            id.append(inp[i])
        id = sorted(id, key=lambda x: self.Pop[x], reverse=True)
        return id

    def gensearch(self, genre):
        films = []
        n = -1
        for i in self.movies['genres']:
            n += 1
            if genre in i.split('|'):
                films.append(self.movies['title'][n])
        v = []
        films = sorted(films, key=lambda x: self.Pop[self.Nid[x.lower()]], reverse=True)
        for i in range(min(15, len(films))):
            v.append(films[i])  # топ 15 фильмов с выбранным жанром по популярности (0-14)
        films = sorted(films, key=lambda x: self.Sco[self.Nid[x.lower()]], reverse=True)
        for i in range(min(15, len(films))):
            v.append(films[i])  # топ 15 фильмов с выбранным жанром по средней оценке (15-29)
        print(len(films))
        return v