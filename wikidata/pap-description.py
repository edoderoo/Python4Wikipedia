import pywikibot
from pywikibot import pagegenerators as pg
import random
from datetime import date,timedelta
#import wd_generators.py


#https://pap.wikipedia.org/wiki/Wikipedia:Art%C3%ADkulonan_importante

papberoep={'Q11247470':'komandanteh','Q2252262':'rapper',
           'Q47064':'militar','Q15982795':'bodybuilder','Q378622':'koredó‎','Q333634':'traduktor','Q482980':'outor','Q10871364':'beisbolista','Q26950764':'fundador','Q30461':'presidente','Q4964182':'filósofo',
           'Q169470':'fisiko','Q593644':'kimiko','Q2526255':'direktor di sine','Q11900058':'eksploradó ','Q177220':'kantante','Q639669':'musiko','Q36180':'eskritor','Q487596':'dramaturgo','Q49757':'poeta',
           'Q15214752':'kabaretero','Q774306':'siruhano','Q1028181':'pintor', 'Q937857':'futbolista','Q3391743':'artista plástiko','Q2490358':'coreograf','Q33999':'aktor','Q947873':'presentadó na televishon',
           'Q82955':'politiko','Q132050':'gobernador','Q182436':'bibliotekario','Q2824523':'miembro di direktiva','Q363802':'promotor','Q326653':'akountent','Q101539':'stewardess',}
papnationaliteit={'Q736':'ekuatoriano','Q155':'brasileño',
                  'Q41':'griego','Q40':'oustriako','Q45':'portuges','Q739':'kolombiano','Q16':'kanades','Q148':'chines','Q43':'turko','Q23666':'ingles','Q159':'ruso','Q35':'danes','Q17':'hapones','Q34':'suiso',
                  'Q29999':'hulandes', 'Q38':'italiano', 'Q172579':'italiano','Q739':'kolombiano','Q20':'noruega', 'Q23666':'ingles','Q29':'spaño','Q30':'merikano','Q142':'franses'}
paplanden={'Q189':'Islandia','Q155':'Brazil','Q15180':'Union Sovietiko',
           'Q55':'Hulanda','Q142':'Fransia','Q29':'Spaña','Q145':'Reino Uni','Q183':'Alemania','Q159':'Rusia','Q32':'Luxembourg','Q16':'Canada','Q34':'Suecia','Q17':'Hapon','Q33':'Finlandia',
           'Q43':'Turkia','Q668':'India','Q16957':'Republika Demokratiko Alemán','Q414':'Argentina','Q20':'Noruega','Q45':'Portugal','Q31':'Bélgika','Q258':'Sur Afrika'}

filmquery='select ?item ?land ?jaar where {?item wdt:P31 wd:Q11424 . optional {?item wdt:P495 ?land} . optional {?item wdt:P577 ?jaar}}'
profession_query='select ?item where {?item wdt:P31 wd:Q5 . ?item wdt:P106 wd:%s . ?item wdt:P27 wd:%s }'
profession_query='select ?item where {?item wdt:P31 wd:Q5 . ?item wdt:P106 wd:%s . ?item wdt:P27 wd:%s OPTIONAL {?item rdfs:description ?itemdescription filter (lang(?itemdescription) = "pap").  } filter (!bound(?itemdescription))}'
scifi_art_query='select ?item where {?item wdt:P31 wd:Q13442814 . ?item wdt:P577 "%04d-%02d-%02dT00:00:00Z"^^xsd:dateTime}'

label_languages={'pap','nl','en','de','fr','pt','es','it','dk','sv'}
commit=True  #false will print the query for testing
updatelabel={'Q11446',}


def randomize(inset):
  outset={}
  inlist=[]
  for x in inset:
    inlist.append(x)
  random.shuffle(inlist)
  for x in inlist:
    outset[x]=inset[x]
  return(outset)

#"""
def wd_sparql_query(spq):
  wikidatasite=pywikibot.Site('wikidata','wikidata') 
  generator=pg.WikidataSPARQLPageGenerator(spq,site=wikidatasite)
  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect=True)
      yield wd

def wd_from_file(usefilename):
  repo=pywikibot.Site('wikidata','wikidata').data_repository()
  csvfile=open(usefilename,'r')
  for alllines in csvfile:
    qitem=alllines[alllines.find('Q'):alllines.find(',')]
    if (len(qitem)>0):
      try:
        wditem=pywikibot.ItemPage(repo,qitem)
        wditem.get(get_redirect=True)
        yield wditem
      except:
        pass

def itemTitle(item):
  try:
    return item.title()
  except:
    pass
  return('')

def getLabel(item):
  for lang in label_languages:
    if lang in item.labels:
       return(item.labels[lang])
  return None

def act_one_person(item):
    tmplabel=tmpdesc={}
    ldaBeroep=None
    ldaNationaliteit=None
    if 'P106' in item.claims:
        beroep=item.claims['P106'][0].getTarget()
        if beroep: beroep.get(get_redirect=True)
        #if 'pap' in beroep.labels:
        #    print('beroep: %s' %(beroep.labels['pap']))
        if itemTitle(beroep) in papberoep:
          ldaBeroep=papberoep[itemTitle(beroep)]
    if 'P27' in item.claims:
        nationaliteit=item.claims['P27'][0].getTarget()
        if nationaliteit: 
          nationaliteit.get(get_redirect=True)
          if itemTitle(nationaliteit) in papnationaliteit:
            ldaNationaliteit=papnationaliteit[itemTitle(nationaliteit)]
        #if 'pap' in nationaliteit.labels:
        #    print('land  : %s'%(nationaliteit.labels['pap']))
    if (not('pap' in item.labels)):
      newlabel=getLabel(item)
      if newlabel:
        tmplabel={'pap':newlabel}
    if ((not('pap' in item.descriptions)) and (ldaNationaliteit and ldaBeroep)): #  or (('pap' in item.descriptions) and (item.descriptions['pap'].find('xxxspaño')>0)) :
      tmpdesc={'pap':f'{ldaBeroep} {ldaNationaliteit}'}
    return tmplabel,tmpdesc

def act_one_query(repo,query):
  for item in wd_sparql_query(query):
    act_one_item(repo,item)

def its_from_a_country(repo,item,lng,simple,complete):
  tmpdesc={}
  landclaim=None
  if ('P17' in item.claims):
    #print('P17')
    landclaim=itemTitel(item.claims['P17'][0].getTarget())
  elif ('P495' in item.claims):
    #print('P495')
    landclaim=itemTitle(item.claims['P495'][0].getTarget())
  elif ('P8047' in item.claims):
    #print('P8047')
    landclaim=itemTitle(item.claims['P8047'][0].getTarget())

  if landclaim!=None:
    try:
      land=pywikibot.ItemPage(repo,landclaim)
      land.get(get_redirect=True)
      if lng in land.labels:
        tmpdesc.update({lng:'%s %s'%(complete,land.labels[lng])})
      else:
        landclaim=None
    except:
      landclaim=None
  if landclaim==None:
    tmpdesc.update({lng:simple})
  #print('from a country: ',tmpdesc)
  return tmpdesc

def its_in_an_administrative_entity(repo,item,lng,withoutP131,withP131):
  tmpdesc={}
  if not 'P131' in item.claims:
    tmpdesc.update({lng:withoutP131})
    return(tmpdesc)
  entity=itemTitle(item.claims['P131'][0].getTarget())
  if entity!=None:
    try:
      entityItem=pywikibot.ItemPage(repo,entity)
      entityItem.get(get_redirect=True)
      if lng in entityItem.labels:
       tmpdesc.update({lng:f'{withP131} {entityItem.labels[lng]}'})
      else:
       tmpdesc.update({lng:withoutP131})
    except:
      tmpdesc.update({lng:withoutP131})
  return(tmpdesc)

def act_one_item(repo,item):
    global commit

    isa=None
    newdesc={}
    newlabel={}
    if 'P31' in item.claims:
      if (not('pap' in item.labels)):
        if itemTitle((item.claims['P31'][0].getTarget()) in updatelabel):
          tstlabel=getLabel(item)
          if tstlabel:
            newlabel.update({'pap':tstlabel})
      isa=itemTitle(item.claims['P31'][0].getTarget())
      if isa=='Q5':         #person
        tmplab,tmpdesc=act_one_person(item)
        newlabel.update(tmplab)
        newdesc.update(tmpdesc)
      elif isa=='Q13442814':  #scientific article
        if (not('pap' in item.descriptions)):
          newdesc.update({'pap':'artikulo sientifíko'})
      elif isa=='Q11879590': #vrouwelijke voornaam
        if (not('pap' in item.descriptions)):
          newdesc.update({'pap':'di prome nomber femenino'})
      elif isa=='Q12308941': #mannelijke voornaam
        if (not('pap' in item.descriptions)):
          newdesc.update({'pap':'di prome nomber maskulino'})
      elif isa=='Q13406463': #wikimedia lijst
        if (not('pap' in item.descriptions)):
          newdesc.update({'pap':'lista di Wikimedia'})
        if (not('cs' in item.descriptions)):
          newdesc.update({'cs':'seznam na projektech Wikimedia'})
        if (not('sk' in item.descriptions)):
          newdesc.update({'sk':'zoznamový článok na projektu Wikimedia'})
      elif isa=='Q11446': #schip
        if (not('pap' in item.descriptions)) or (('pap' in item.descriptions) and (item.descriptions['pap'] in {'','barku'})):
          newdesc=its_from_a_country(repo,item,'pap','barku','barku den')
      elif isa=='Q123705': #buurt of wijk
        if (not('pap' in item.descriptions)) or (('pap' in item.descriptions) and (item.descriptions['pap'] in {'','bisindario'})):
          newdesc=its_in_an_administrative_entity(repo,item,'pap','bisindario','bisindario den')
      elif isa=='Q23442': #
        if (not('pap' in item.descriptions) or (('pap' in item.descriptions) and (item.descriptions['pap'] in {'','Isla'}))):
          newdesc=its_in_an_administrative_entity(repo,item,'pap','Isla','Isla den')
      elif isa=='': #
        pass
    lda={}
    if (newdesc!={}):
      lda.update({'descriptions':newdesc})
    if (newlabel!={}):
      lda.update({'labels':newlabel})

    if (lda!={}):
          print(itemTitle(item),lda)
          try:
            if commit:
              item.editEntity(lda,summary='label and description @ pap-wiki')
            else:
              print('no commit',itemTitle(item))
          except:
            pass

def alle_beroepen():
  repo=pywikibot.Site('wikidata','wikidata').data_repository()
  for prof in randomize(papberoep):
    for cntr in randomize(papnationaliteit):
      query=profession_query%(prof,cntr)
      act_one_query(repo,query)

def scifi_articles():
  dayloop=date.today()
  while dayloop>=date(2021,3,1):
    dayloop = dayloop-timedelta(days=1)
    query=scifi_art_query%(dayloop.year,dayloop.month,dayloop.day)
    print(query)
    act_one_query(query)

def act_one_file(filename):
  for item in wd_from_file(filename):
    act_one_item(repo,item)

def test_one_item(itemcode):
  global commit

  commit=False
  site=pywikibot.Site('wikidata','wikidata')
  repo=site.data_repository()
  item=pywikibot.ItemPage(repo, itemcode)
  item.get(get_redirect=True)
  act_one_item(repo,item)
  #print(f'label      : {lab}\nDescription: {desc}')

print('Start')
site=pywikibot.Site('wikidata','wikidata')
repo=site.data_repository()
#act_one_query(repo,'select ?item ?d where {?item wdt:P31 wd:Q23442 . OPTIONAL {?item rdfs:description ?d filter (lang(?d) = "pap").  } filter (!bound(?d))}')
alle_beroepen()
#test_one_item('Q130025')
#act_one_file('/stack/lijsten.csv')
print('Klaar')
