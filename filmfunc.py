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
