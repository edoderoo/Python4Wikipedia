import pywikibot
from pywikibot import pagegenerators as pg

txt2search=f'insource:/et\.al\./'
replFrom='et.al.'
replTo='et al.'
maxresults=1200

print('Begonnen')
site=pywikibot.Site('nl')
for mypage in pg.SearchPageGenerator(txt2search,maxresults,0,site):
   mypage.put(mypage.text.replace(replFrom,replTo),summary=f'vervang {replFrom} in {replTo} #zoek-en-vervang')
print('Klaar')