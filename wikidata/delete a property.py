#20190828 2307

import pywikibot
from pywikibot import pagegenerators as pg
import requests

prop2delete='P5660'

query='select ?item where {?item wdt:%s ?iets}' % prop2delete

def wd_sparql_query(spq):
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd in generator:
     try:
       wd.get(get_redirect=True)
       yield wd
     except:
       pass
x=0
for item in wd_sparql_query(query):
 if (prop2delete in item.claims):
  claim=item.claims[prop2delete][0]
  try:
    item.removeClaims(claim,summary='https://www.wikidata.org/w/index.php?title=Wikidata:Properties_for_deletion&oldid=1004301558')
  except:
    pass
  x=x+1
  y= (12-x)
    
  #print(f'stoppie joppie: {x}/{y}={x/y} - {type(y)}')
