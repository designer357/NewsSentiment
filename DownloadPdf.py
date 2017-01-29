__author__ = 'chengmin'
import requests
from bs4 import BeautifulSoup as bs
import urllib


_ANO = '2013/'
_MES = '01/'
_MATERIAS = 'matematica/'
_CONTEXT = 'wp-content/uploads/' + _ANO + _MES
_URL = 'http://www.desconversa.com.br/' + _MATERIAS + _CONTEXT

# functional
r = requests.get(_URL)
print(_URL)
soup = bs(r.text)
urls = []
names = []
for i, link in enumerate(soup.findAll('a')):
    _FULLURL = _URL + link.get('href')
    if _FULLURL.endswith('.pdf'):
        urls.append(_FULLURL)
        names.append(soup.select('a')[i].attrs['href'])

names_urls = zip(names, urls)
print(urls)
for name, url in names_urls:
    print(url)
    rq = urllib.Request(url)
    res = urllib.urlopen(rq)
    pdf = open("pdfs/" + name, 'wb')
    pdf.write(res.read())
    pdf.close()