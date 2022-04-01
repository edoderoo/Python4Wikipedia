import pywikibot
from pywikibot import pagegenerators as pg

def wd_sparql_query(spq):
  wikidatasite=pywikibot.Site('wikidata','wikidata') 
  generator=pg.WikidataSPARQLPageGenerator(spq,site=wikidatasite)
  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect=True)
      yield wd

descr={'nl':'schilderij van %s', 
       'en':'painting by %s',
       'de':'Gemälde von %s',
       'fr':'tableau de %s',
       'pt':'pintura de %s',
       'sv':'målning av %s',
       'hu':'%s festménye',
       'es':'cuadro de %s',
       'da':'maleri af %s',
       'ca':'quadre de %s',
       'it':'pittura di %s',
       'eo':'pentraĵo de %s',
       'ast':'pintura de %s',
       'gl':'pintura de %s',
       'io':'pikturo da %s',
       'oc':'pintura de %s',
       'nb':'maleri av %s',
       'nn':'måleri av %s',
       'en-gb':'painting by %s',
       'ro':'pictură de %s',
       'pl':'obraz %s',
       'pap':'pintura di %s',
       '':'',
       '':'',
       '':'',
       '':'',
       '':'',
       '':'',
       }
        
query='select ?item ?artist where {?item wdt:P31 wd:Q3305213 . ?item wdt:P170 ?artist}'
lng='en'
lbllng={'en','de','fr','nl','it','pt','es','dk','se','no'}

def make_description(lng,item,artist):
   if (lng) in artist.labels:
      return({lng:descr[lng] % artist.labels[lng]}) 
   #for xlng in descr:
   if (True): 
     xlng='en'
     if (xlng in artist.labels):
       return({lng:descr[lng] % artist.labels[xlng]})     
   return ({})   

print('Start!')
failed=done=0
for item in wd_sparql_query(query):
  artistlbl=None
  artist=item.claims.get('P170')[0].getTarget()
  if (artist):
    artist.get(get_redirect=True)
    description={}
    for lng in descr:
     if (lng!='') and (descr[lng]!=''):   
      if (not(lng in item.descriptions)):
        description.update(make_description(lng,item,artist))
        #print(lng)
    if (description!={}):
      #print(f'{item.title()} – {description}')
      print(f'{item.title()}')
      try:
        item.editEntity({'descriptions':description},summary='add missing descriptions for this painting')
        done+=1
      except Exception as errmsg: 
        print('Error: ',errmsg)
        failed+=1
      #xxx=(1/(500-done)) #notbremse
      #print(xxx,deler)
print('Klaar!')        
