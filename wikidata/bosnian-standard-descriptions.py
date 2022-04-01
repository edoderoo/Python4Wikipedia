import pywikibot
from pywikibot import pagegenerators as pg
import sys
import time
import codecs

site=pywikibot.Site('wikidata','wikidata')
repo=site.data_repository()
query1='SELECT * WHERE {?item schema:description "Wikinews članak"@bs ; wdt:P31 wd:Q17633526}'
query2='SELECT * WHERE {?item schema:description "Wikimedia:Kategorije"@bs ; wdt:P31 wd:Q4167836}'
query3='SELECT * WHERE {?item schema:description "šablon Wikimedia"@bs ; wdt:P31 wd:Q11266439}'
query4='SELECT * WHERE {?item schema:description "Kategorija Wikipedije"@bs ; wdt:P31 wd:Q4167836}'
query5='SELECT * WHERE {?item schema:description "Asteroid"@bs ; wdt:P31 wd:Q3863}'

def log_skipped(itemno):
  with codecs.open("bosnian.skiplog.csv","a", encoding="utf-8") as logfile:
    logfile.write('%s\n' % (itemno))
  logfile.close

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

def act_one_item(wd):
  newdesc={}
  if 'P31' in wd.claims:
    for P31 in wd.claims['P31']:
      P31title=P31.getTarget().title()
      if (P31title=='Q4167836') or (P31title=='Q24046192') or (P31title=='Q15647814') or (P31title=='Q23894233') or (P31title=='Q56428020') or (P31title=='Q20010800') or (P31title=='Q59542487') or (P31title=='Q59541917'):
        newdesc.update({'bs':'kategorija na Wikimediji'})
      elif P31title=='Q17633526':
        newdesc.update({'bs':'članak na Wikivijestima'})
      elif P31title=='Q11266439':
        newdesc.update({'bs':'šablon na Wikimediji'})
      elif P31title=='Q3863':
        newdesc.update({'bs':'asteroid'})
      else:
        log_skipped(P31title)

  if newdesc!={}:
    try:
      wd.editEntity({'descriptions':newdesc},summary='[-request from [[WD:RBOT]]')
    except:
      print(f'save of {wd.title()} failed')
      #time.sleep(10)
    #print(1/0)

if (len(sys.argv)>1):
  if sys.argv[1]=='1':query=query1
  elif sys.argv[1]=='2':query=query2
  elif sys.argv[1]=='3':query=query3
  elif sys.argv[1]=='4':query=query4
  elif sys.argv[1]=='5':query=query5
  elif sys.argv[1]=='csv':query=''
  else: print(sys.argv[1])

if query!='':
  print(query)
  for item in wd_sparql_query(query):
    act_one_item(item)
else:
  for item in  wd_from_file('/stack/bosnian.csv'):
    act_one_item(item)
