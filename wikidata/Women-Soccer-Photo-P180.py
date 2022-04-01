import pywikibot
from pywikibot import pagegenerators as pg
import requests 
import json

def wd_sparql_query(spq):
   print(spq)
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd in generator:
     try:
       wd.get(get_redirect=True)
       yield wd
     except:
       pass

def getEndPoint(pageid):
    url=f'https://commons.wikimedia.org/wiki/Special:EntityData/M{pageid}.json'
    data=requests.get(url)
    if (data):
      st=json.loads(data.text)
      return(st['entities'])
    return None

def getCommonsStructuredData(pageid):
  endp=getEndPoint(pageid)  
  if endp:
    if (f'M{pageid}' in endp):
      retval=endp[f'M{pageid}']    
    else:
      return(None)
    if ("statements" in retval):
      return retval["statements"]
    else:
      return None
  return None

def getCommonsProperty(pageid,property):
  comSD=getCommonsStructuredData(pageid)
  if comSD:
    if (property in comSD):
      return comSD[property][0]['mainsnak']['datavalue']['value']['id']
    else:
      return None

def CommonsPropertyHasProperty(pageid,property,title):
  comSD=getCommonsStructuredData(pageid)
  if comSD:
    if (property in comSD):
      for i in (0,len(comSD[property])-1):
        try:
          P180=comSD[property][i]['mainsnak']['datavalue']['value']['id']
        except:
          P180='Q5'
        if P180==title:
            return True
        else: #check if target redirects to title
          wdP180=pywikibot.ItemPage(repo,P180)
          wdP180.get(get_redirect=True)
          if wdP180.title()==title:
            return True
      return False
    else:
      return False


occupation='Q937857' #voetballer
query='select ?item ?photo where {?item wdt:P106 wd:%s . ?item wdt:P21 wd:Q6581072 . ?item wdt:P18 ?photo}' % occupation
#print(query)
commonssite=pywikibot.Site('commons','commons')
site=pywikibot.Site('wikidata','wikidata')
repo=site.data_repository()

def checkOneWD(wd):
    target=wd.claims['P18'][0].getTarget().title()
    page=pywikibot.Page(commonssite,target)
    #print(getCommonsStructuredData(page.pageid))
    if not(CommonsPropertyHasProperty(page.pageid,'P180',wd.title())):
      if 'nl' in wd.labels:
        lng='nl'
      elif 'en' in wd.labels:
        lng='en'
      elif 'de' in wd.labels:
        lng='de'
      else:
        for lng in wd.labels:
          pass
      if ('P27' in wd.claims):
        cntry=wd.claims['P27'][0].getTarget().title()
        wdCntry=pywikibot.ItemPage(repo,cntry)
        wdCntry.get(get_redirect=True)
        countryname=wdCntry.labels['nl']
      else:
        countryname=''
      txt=f'|-\n|[[:d:{wd.title()}]] || {wd.labels[lng]} || [[commons:{target}]] || {countryname}\n'
      print(txt)
      return(txt)
    return('')

def testOne(itemid):
    one=pywikibot.ItemPage(repo,itemid)
    one.get(get_redirect=True)
    checkOneWD(one)

print('Start')
txt='{| class="wikitable sortable"\n|-\n! wd-Item !! Name !! photo !! land \n'
for wd in wd_sparql_query(query):
  txt+=checkOneWD(wd)
txt+='\n|}'
xsite=pywikibot.Site('nl','wikipedia')
page=pywikibot.Page(xsite,'Gebruiker:Edoderoo/voetbalplaatjes')
page.put(txt,comment='plaatjes zonder P180')
print('Klaar')
