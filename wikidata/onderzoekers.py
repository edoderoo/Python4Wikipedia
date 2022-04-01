import pywikibot
from pywikibot import pagegenerators as pg
import requests

site = pywikibot.Site('wikidata','wikidata')           #Geef aan naar welke site je wilt schrijven
repo = site.data_repository()                     #voor ophalen wikidata-items adhv Qxxxx
baseURL='https://www.researcherid.com/rid/%s'
lng='nl'

def wd_sparql_query(spq):
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd in generator:
     try:
       wd.get(get_redirect=True)
       yield wd
     except:
       pass

def one_profession(lng,Qprof,profession):
  counter=0
  #print(query%Qprof)
  for wditem in wd_sparql_query(query%Qprof):
    if not (lng in wditem.descriptions):
      counter+=1
      one_wd(wditem,lng,profession)

def one_wd(wd,lng,profession):
    try:
      wd.editEntity({'descriptions': {lng:profession}},summary=f'set professions')
    except ValueError:
      pass  
    except:
      pass
    else:
      pass    

query='select ?item ?land where {?item wdt:P31 wd:Q5 . ?item wdt:P106 wd:%s . OPTIONAL{?item wdt:P27 ?land} filter (!bound(?land))}'

print('Begonnen')
counter=0
for wd in wd_sparql_query('select ?item where {?item wdt:P31 wd:Q28640}'):
  if (lng in wd.labels):
    counter+=1
    print(f'{counter}-{wd.title()}-{wd.labels[lng]}')
    one_profession(lng,wd.title(),wd.labels[lng])
print('Klaar')