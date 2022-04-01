import pywikibot
from pywikibot import pagegenerators as pg

srclng='nl'
addition={'nl':'(voornaam)','en':'(first name)','de':'(Vorname)','fr':'(prénom)'}

def wd_sparql_query(spq):
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd in generator:
     try:
       wd.get(get_redirect=True)
       yield wd
     except:
       pass

firstnames={'Q11879590','Q12308941','Q202444'}

site = pywikibot.Site(srclng,'wikipedia')           #Geef aan naar welke site je wilt schrijven
repo = site.data_repository()                     #voor ophalen wikidata-items adhv Qxxxx
query='select ?item where {?item wdt:P31 wd:%s}'

def addAlias(wd,newAlias):
  aliasList=[]
  if (srclng in wd.aliases):
   for oneAlias in wd.aliases[srclng]:
    if (oneAlias in aliasList):
      return
    else:
      aliasList.append(oneAlias)
  if (newAlias in aliasList):
    return
  else:
    aliasList.append(newAlias)  
  data={}
  data.update({'aliases':{srclng:aliasList}})
  wd.editEntity(data,summary='add alias for (firstname)')  

def hasAlias(wd,findAlias):
 if (srclng in wd.aliases):   
   for oneAlias in wd.aliases[srclng]:
    if oneAlias==findAlias:
     return(True)
 return(False)  

def allItems():
 count=0
 for qqq in firstnames:
  q=query % qqq
  for item in wd_sparql_query(q):
    oneItem(item) 
    count+=1
    #if ((count % 13)==0): count=10/0
    
def oneItem(item):
  if (srclng in item.labels):
    alias=item.labels[srclng]+' '+addition[srclng]
    if not hasAlias(item,alias):
      addAlias(item,alias)

def testRun():    
 petra=pywikibot.ItemPage(repo,'Q1474819')
 petra.get(get_redirect=True)
 oneItem(petra)

allItems()