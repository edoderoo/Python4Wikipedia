import pywikibot
from pywikibot import pagegenerators as pg

query='select ?item where {?item schema:description \"спіс атыкулаў у адным з праектаў Вікімедыя\"@be}'

def wd_sparql_query(spq):
  wikidatasite=pywikibot.Site('wikidata','wikidata') 
  generator=pg.WikidataSPARQLPageGenerator(spq,site=wikidatasite)
  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect=True)
      yield wd

print(query)        
data={}
data.update({'descriptions':{'be':'спіс артыкулаў у адным з праектаў Вікімедыя'}})
for item in wd_sparql_query(query):
  title=item.title()
  if 'be' in item.descriptions: 
    descr=item.descriptions['be']
    if descr=='спіс атыкулаў у адным з праектаў Вікімедыя':
      item.editEntity(data,summary='typo in be-description')    
      #error('')
  else:
    descr='n/a'
    print(title, descr)  
