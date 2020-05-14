import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

from filmfunc import get_credit, get_budget, get_time, format_number

df = pd.DataFrame(columns=['title', 'director', 'producer', 'writer', 'cast', 'time', 'budget', 'box_office'])

file = requests.get('https://en.wikipedia.org/wiki/1976_in_film')
soup = bs(file.text, 'html.parser')

s = [link['href'] for link in soup.select('i a')]

s

s.index('/wiki/7-Man_Army')

s = s[1:54]

s = list(set(s))

for title in s[:40]:

    url = 'https://en.wikipedia.org' + title
    file = requests.get(url)
    soup = bs(file.text, 'html.parser')

    info = soup.find(class_='infobox vevent')
    if info == None: continue

    director = get_credit(info, 'Directed by')
    producer = get_credit(info, 'Produced by')
    writer = get_credit(info, 'Written by') + get_credit(info, 'Screenplay by')
    cast = get_credit(info, 'Starring')
    time = get_time(info)
    budget = get_budget(info, 'Budget')
    box_office = get_budget(info, 'Box office')
    title = info.find('th').text

    res = dict(title=title, director=director, producer=producer, writer=writer, cast=cast, time=time, budget=budget, box_office=box_office)

    df = df.append(res, ignore_index=True)

df
