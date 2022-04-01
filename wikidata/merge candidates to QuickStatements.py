import pywikibot
from pywikibot import pagegenerators as pg
lng='nl'
into=[]


def wd_sparql_query(spq):
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd,wd2 in generator:
     try:
       wd.get(get_redirect=True)
       wd2.get(get_redirect=True)
       yield wd,wd2
     except:
       pass

query='SELECT DISTINCT ?item ?otheritem ?sitelink WHERE {  ?sitelink schema:about ?item, ?otheritem.  ?sitelink schema:isPartOf <https://nl.wikipedia.org/>.  filter(?item != ?otheritem)}'
findother=''

for item in wd_sparql_query(query):
  print(item.title())
print('Klaar')
