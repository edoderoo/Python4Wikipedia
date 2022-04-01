import pywikibot
from pywikibot import pagegenerators as pg

#bij een achternaam PQ101352 met voorvoegsel (de Jong, van der Velde, van de Wetering, van Willigenburg, etc)

sqlQuery='select ?item where {?item wdt:P31 wd:Q101352}'
searchfor=['de ','van der ','van de ','van ','in het ']
someitems=['Q21494168','Q1180481','Q7913814']
lang='nl'

def add2list(list,item2add,changed):
  if not(item2add in list):
    list.append(item2add)
    return list,True
  return list,changed  

def wd_sparql_query(spq):
  wikidatasite=pywikibot.Site('wikidata','wikidata') 
  generator=pg.WikidataSPARQLPageGenerator(spq,site=wikidatasite)
  for wd in generator:
    try:
      wd.get(get_redirect=True)
      yield wd
    except:
      pass  

def action_one_item(wd):
  changed=False
  alias=[]
  if lang in wd.aliases:
    for onealias in wd.aliases[lang]:
      alias,changed =add2list(alias,onealias,changed)
  changed=False  
  if lang in wd.labels:
    label=wd.labels[lang]
    for found in searchfor:
      if (label[0:len(found)].lower()==found.lower()):
        alias,changed=add2list(alias,label[len(found):]+' '+found,changed)
        label='   ' #so it won't get another alias
    if (changed):
        newalias=[]
        for onealias in alias:
            newalias.append(onealias)
        data={}
        data.update({'aliases':{lang:newalias}})
        wd.editEntity(data,summary=f'achternaam-alias <{newalias}>')
  return(changed)

print('Begonnen')      
aantal=0
site = pywikibot.Site('wikidata','wikidata')
repo = site.data_repository()

if (False):
    for item in someitems:
      wd=pywikibot.ItemPage(repo,item)
      wd.get()
      if (action_one_item(wd)):
          aantal+=1
          print('x: %d: %s-%s' % (aantal,item.title(),ifany))
else:    
  for item in wd_sparql_query(sqlQuery):
    if (action_one_item(item)):
      ifany=''
      if (lang in item.labels):
        ifany=item.labels[lang]
      print('x: %d: %s-%s' % (aantal,item.title(),ifany))
      aantal+=1
    #if aantal>250: break
    
print('Klaar')    