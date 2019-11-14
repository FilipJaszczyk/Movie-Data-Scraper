from bs4 import BeautifulSoup
import requests
import csv
import json
import codecs

films = []

def getFilms250():
    sourceTop250 = requests.get(
        'https://www.imdb.com/chart/top?ref_=nv_mv_250').text
    soup = BeautifulSoup(sourceTop250, 'lxml')
    counter = 0
    for title_container, rating_container in zip(soup.find_all('td', class_='titleColumn'),
                                                 soup.findAll('td', class_='ratingColumn imdbRating')):
        title = title_container.a.text
        counter += 1
        year = title_container.span.text
        rating = rating_container.strong.text
        film_data = [counter, title, year.strip('()'), rating]
        films.append(film_data)
    return films

def csvFormat(films, userDelimiter):
    with open('new_film_base.csv', 'w', newline='', encoding="utf-8") as file:
        header = ['Position', 'Title', 'Year', 'imdbRanking']
        film_writer = csv.writer(file, delimiter=userDelimiter)
        film_writer.writerow(header)
        film_writer.writerows(films)

def jsonFormat(films):
    with open('new_film_base.json', 'w', encoding='utf-8') as file:
        arr = []
        for position, title, year, rank in films:
            x = {
                "position": position,
                "title": title,
                "year": year,
                "imbdRanking": rank
            }
            arr.append(x)
        movies = {
            "filmsRequested":arr
        }
        json.dump(movies, file, indent=True, ensure_ascii=False)


def handleUserFilm(prompt):
    #While user enters a proper input a function will get list of wanted films
    while True:
        userMessageFilm = input((prompt))
        if userMessageFilm == 'films250':
            getFilms250()
            break
        else:
            print('No such data')
            continue
    return userMessageFilm

def handleUserFormat(prompt):
    while True:
        userMessageFormat = input((prompt))
        if userMessageFormat == 'json':
            jsonFormat(films)
            break
        elif userMessageFormat == 'csv':
            while True:
                delimiter = input('Enter the Delimiter for csv format(";" recommended): ')
                if len(delimiter) > 4:
                    print("delimiter can't be that long")
                    continue
                else:
                    csvFormat(films, delimiter)
                    break
        else:
            print('Format unkown')
            continue

        return userMessageFormat


filmsUser = handleUserFilm('To get Top250 type - films250: ')
formats = handleUserFormat('To get csv format type - csv\nTo get json format type - json ')
