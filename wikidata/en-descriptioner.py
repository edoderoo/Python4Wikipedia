import pywikibot
from pywikibot import pagegenerators as pg

def wd_sparql_query(spq):
  wikidatasite=pywikibot.Site('wikidata','wikidata') 
  generator=pg.WikidataSPARQLPageGenerator(spq,site=wikidatasite)
  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect=True)
      yield wd
        
        
#query='select ?item where {?item wdt:P31 wd:Q55488 . ?item wdt:P17 ?land}' #railway station
#query='select ?item where {?item wdt:P31 wd:Q55678 . ?item wdt:P17 ?land}' #railway stop
query='select ?item where {?item wdt:P31 wd:Q784159 . ?item wdt:P17 ?land}' #railway passing loop
repo=pywikibot.Site('wikidata','wikidata').data_repository()

for item in wd_sparql_query(query):
 if (not ('en' in item.descriptions)):   
  countryCode=item.claims['P17'][0].getTarget().title()
  countryItem=pywikibot.ItemPage(repo,countryCode)
  countryItem.get(get_redirect=True)   
  if ('en' in countryItem.labels):   
   countryName=countryItem.labels['en']
   if countryName=='United States of America':
        countryName='the United States of America'
   elif countryName=='United Kingdom':
       countryName='the UK'
   elif countryName=='Netherlands': 
       countryName='the Netherlands'
   areaName=''     
   try: 
     if 'P131' in item.claims:
       areaCode=item.claims['P131'][0].getTarget().title()
       areaItem=pywikibot.ItemPage(repo,areaCode)
       if 'en' in areaItem.labels:
         areaName=areaItem.labels['en']+', '
     data={}
     #data.update({'descriptions':{'en':f'railway station in {areaName}{countryName}'}})
     #item.editEntity(data,summary='auto-description for railway stations in a country') 
     #data.update({'descriptions':{'en':f'railway stop in {areaName}{countryName}'}})
     #item.editEntity(data,summary='auto-description for railway stops in a country') 
     data.update({'descriptions':{'en':f'railway passing loop in {areaName}{countryName}'}})
     item.editEntity(data,summary='auto-description for railway passing loops in a country') 
   except:
     pass


