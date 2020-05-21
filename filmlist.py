import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re

def get_credit(info, credit):
    res = []
    if info.find('th', string=credit) is not None:
        res = info.find('th', string=credit).parent.stripped_strings
    res = list(res)
    res = [i for i in res[1:] if i[0].isupper()]
    return res

def get_time(info):
        if info.find('th', string='Running time') is None: return []
        else:
            res = info.find('th', string='Running time').parent.stripped_strings
            res = list(res)[1]
            if res[0:1].isalpha() == True:
                return []
            else:
                return re.search(r'\d+', res).group()

def get_budget(info, number):
    res = []
    mil = bil = False
    if info.find('th', string=number) is not None:
        res = info.find('th', string=number).parent.stripped_strings
    res = list(res)
    if res == []: return res
    for s in res:
        if 'million' in s: mil = True
        if 'billion' in s: bil = True
    try:
        return format_number(res[1:][0], mil, bil)
    except:
        return []

def format_number(s, mil, bil):
    if s[0] != '$' and s[:3] != 'US$': return []
    n = re.search('[0-9]+([,.][0-9]+)*', s).group()
    if mil == True:
        if '.' in n:
            dec = len(n) - n.index('.') - 1
            n = n.replace('.', '') + '0' * (6 - dec)
        else: n = n + '000000'
    if bil == True:
        if '.' in n:
            dec = len(n) - n.index('.') - 1
            n = n.replace('.', '') + '0' * (9 - dec)
        else: n = n + '000000000'
    if ',' not in n:
        n = '{0:,.0f}'.format(int(n))
    return n

def results(name, awards, year=2020):
    if name in awards.index:
        nom = won = 0
        noms = awards.loc[name].nom[1:-1].split()
        wins = awards.loc[name].won[1:-1].split()
        for y in noms:
            if int(y) < year: nom += 1
        for y in wins:
            if int(y) < year: won += 1
        return nom, won
    else: return 0, 0

def results_person(name, awards, year=2020):
    if name in awards.index:
        nom = won = 0
        nom_entries = awards.filter(like=name, axis=0).nom.values
        noms = ''
        for entry in nom_entries:
            noms = noms + entry[1:-1] + ' '
        noms = noms.split()
        win_entries = awards.filter(like=name, axis=0).won.values
        wins = ''
        for entry in win_entries:
            wins = wins + entry[1:-1] + ' '
        wins = wins.split()
        for y in noms:
            if int(y) < year: nom += 1
        for y in wins:
            if int(y) < year: won += 1
        return nom, won
    else: return 0, 0

def all_results(name, year=2020):
    osc = results(name, oscars, year)
    baf = results(name, baftas, year)
    glo = results(name, globes, year)
    return osc[0]+baf[0]+glo[0], osc[1]+baf[1]+glo[1]

def all_results_person(name, year=2020):
    osc = results_person(name, oscars, year)
    baf = results_person(name, baftas, year)
    glo = results_person(name, globes, year)
    return osc[0]+baf[0]+glo[0], osc[1]+baf[1]+glo[1]

def get_rating(index, credit, year):
    nom = won = 0
    for name in df.iloc[index][credit]:
        rating = all_results_person(name, year)
        nom += rating[0]
        won += rating[1]
    return nom, won


oscars = pd.read_csv('oscar_noms_by_year.csv', index_col='name')
baftas = pd.read_csv('bafta_noms_by_year.csv', index_col='name')
globes = pd.read_csv('globe_noms_by_year.csv', index_col='name')

df = pd.DataFrame(columns=['title', 'director', 'producer', 'writer', 'cast', 'music', 'cinematography', 'editing', 'distribution', 'time', 'language', 'budget', 'box_office'])

file = requests.get('https://en.wikipedia.org/wiki/1989_in_film')
soup = bs(file.text, 'html.parser')

s = [link['href'] for link in soup.select('i a')]

s
s.index('/wiki/DeepStar_Six')
s.index('/wiki/The_Road_to_Ruin_(1934_film)')

s = s[56:485]

s = list(set(s))

for title in s:

    url = 'https://en.wikipedia.org' + title
    file = requests.get(url)
    soup = bs(file.text, 'html.parser')

    info = soup.find(class_='infobox vevent')
    if info == None: continue

    director = get_credit(info, 'Directed by')
    producer = get_credit(info, 'Produced by')
    writer = get_credit(info, 'Written by') + get_credit(info, 'Screenplay by')
    cast = get_credit(info, 'Starring')
    music = get_credit(info, 'Music by')
    cinematography = get_credit(info, 'Cinematography')
    editing = get_credit(info, 'Edited by')
    distribution = get_credit(info, 'Distributed by')
    time = get_time(info)
    language = get_credit(info, 'Language')
    budget = get_budget(info, 'Budget')
    box_office = get_budget(info, 'Box office')
    title = info.find('th').strings
    titlelist = list(title)
    title = ''.join([ i + ' ' for i in titlelist]).strip()

    res = dict(title=title, director=director, producer=producer, writer=writer, cast=cast, music=music, cinematography=cinematography, editing=editing, distribution=distribution, time=time, language=language, budget=budget, box_office=box_office)

    df = df.append(res, ignore_index=True)


df


df.to_pickle('films_1989.pkl')

##############################################################################

dir = df.iloc[4].director
pro = df.iloc[4].cast

def get_rating(index, credit, year):
    nom = won = 0
    for name in df.iloc[index][credit]:
        rating = all_results_person(name, year)
        nom += rating[0]
        won += rating[1]
    return nom, won

get_rating(4, 'cast', 2020)
all_results_person("Tom Berenger", 2020)
all_results_person("Mimi Rogers", 2020)
all_results_person("Lorraine Bracco", 2020)
all_results_person("François Truffaut", 2020)

all_results_person("Jack Nicholson")
oscars.filter(like="Jack Nicholson", axis=0).nom.values


url = 'https://en.wikipedia.org/wiki/Dr._Strangelove'
file = requests.get(url)
soup = bs(file.text, 'html.parser')

info = soup.find(class_='infobox vevent')
