import numpy as np
import pandas as pd
import re

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

def split_results_person(name, year=2020):
    osc = results_person(name, oscars, year)
    baf = results_person(name, baftas, year)
    glo = results_person(name, globes, year)
    return dict(o_n=osc[0], b_n=baf[0], g_n=glo[0], o_w=osc[1], b_w=baf[1], g_w=glo[1])


def get_split_rating(index, credit, year):
    res = dict(o_n=0, b_n=0, g_n=0, o_w=0, b_w=0, g_w=0)
    for name in df.iloc[index][credit]:
        rating = split_results_person(name, year)
        for key, value in rating.items():
            res[key] += rating[key]
    return res

def process_budget(b):
    b = list(b)
    b = [ np.nan if x == [] else x for x in b ]
    b = [ float(x.replace(',', '')) if type(x) != float else x for x in b ]
    return pd.Series(b)


def process(df, y):
    cols = pd.MultiIndex.from_product([['director', 'producer', 'cast', 'writer', 'music', 'cinematography', 'editing'], ['o_n', 'b_n', 'g_n', 'o_w', 'b_w', 'g_w']])

    majors = ['Paramount', 'Warner', 'Columbia', 'Disney', 'Universal']

    proc = pd.DataFrame(columns=cols)
    nom = []
    maj = []
    for n in df.index:
        d = {}
        d['director'] = get_split_rating(n, 'director', y)
        d['producer'] = get_split_rating(n, 'producer', y)
        d['cast'] = get_split_rating(n, 'cast', y)
        d['writer'] = get_split_rating(n, 'writer', y)
        d['music'] = get_split_rating(n, 'music', y)
        d['cinematography'] = get_split_rating(n, 'cinematography', y)
        d['editing'] = get_split_rating(n, 'editing', y)
        proc = proc.append(pd.DataFrame.from_dict(d).unstack(), ignore_index=True)

        t = df.iloc[n].title + ' ' + str(y)
        if len(os.query('film == @t').film.values) == 0:
            nom.append(0)
        else:
            nom.append(1)

        m = df.iloc[n].distribution
        if True in [x in i for i in m for x in majors]:
            maj.append(1)
        else:
            maj.append(0)

    proc['major']  = pd.Series(maj)
    t = list(df.time)
    proc['time'] = pd.Series([ np.nan if x == [] else x for x in t ]).apply(float)
    proc['budget'] = process_budget(df.budget)
    proc['box_office'] = process_budget(df.box_office)
    proc['profit'] = proc.box_office - proc.budget
    proc['title'] = df.title
    proc['nom'] = pd.Series(nom)

    return proc


oscars = pd.read_csv('oscar_noms_by_year.csv', index_col='name')
baftas = pd.read_csv('bafta_noms_by_year.csv', index_col='name')
globes = pd.read_csv('globe_noms_by_year.csv', index_col='name')
os = pd.read_pickle('oscar_film_noms.pkl')

start = 1971
df = pd.read_pickle('./years_pickle/films_' + str(start) + '.pkl')
proc = process(df, start)

for y in range(1972, 1990):
    df = pd.read_pickle('./years_pickle/films_' + str(y) + '.pkl')
    procnext = process(df, y)
    proc = pd.concat([proc, procnext])

proc.index = pd.RangeIndex(len(proc.index))


proc.to_pickle('1971-1989_processed.pkl')
