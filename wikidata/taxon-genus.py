import pywikibot
from pywikibot import pagegenerators as pg
import sys
import time

solve={'en':{'genus of fish':'geslacht van vissen'}},\
      {'en':{'genus of birds':'geslacht van vogels'}},\
      {'en':{'genus of plants':'geslacht van planten'}},\
      {'en':{'genus of plant':'geslacht van planten'}},\
      {'en':{'genus of algae':'geslacht van algen'}},\
      {'en':{'genus of Actinopterygii':'geslacht van straalvinnigen'}},\
      {'en':{'genus of annelids':'geslacht van ringwormen'}},\
      {'en':{'genus of Arachnida':'geslacht van spinachtigen'}},\
      {'en':{'genus of bacteria':'geslacht van bacteriën'}},\
      {'en':{'genus of crustaceans':'geslacht van schaaldieren'}},\
      {'en':{'genus of Diplopoda':'geslacht van Miljoenpoten'}},\
      {'en':{'genus of fishes':'geslacht van vissen'}},\
      {'en':{'genus of fungi':'geslacht van schimmels'}},\
      {'en':{'genus of Gastropoda':'geslacht van slakken'}},\
      {'en':{'genus of insects':'geslacht van insecten'}},\
      {'en':{'genus of molluscs':'geslacht van weekdieren'}},\
      {'en':{'genus of protists':'geslacht van protisten'}},\
      {'en':{'genus of reptiles':'geslacht van reptielen'}},\
      {'en':{'genus of protozoans':'geslacht van protozoa'}},\
      {'en':{'genus of sponges':'geslacht van sponsdieren'}},\
      {'en':{'genus of worms':'geslacht van wormen'}},\
      {'en':{'genus of arachnids':'geslacht van spinachtigen'}},\
      {'en':{'genus of myriapods':'geslacht van duizendpotigen'}},\
      {'en':{'genus of Malacostraca':'geslacht van Malacostraca'}},\
      {'en':{'genus of beetles':'geslacht van kevers'}},\
      {'en':{'genus of Staphylinidae':'geslacht van kortschildkevers'}},\
      {'en':{'genus of Entognatha':'geslacht van zespotigen'}},\
      {'en':{'genus of Hemiptera':'geslacht van halfvleugeligen'}},\
      {'en':{'genus of Maxillopoda':'geslacht van Maxillopoda'}},\
      {'en':{'genus of mammals':'geslacht van zoogdieren'}},\
      {'en':{'genus of cockroaches':'geslacht van kakkerlakken'}},\
      {'en':{'genus of leaf beetles':'geslacht van bladkevers'}},\
      {'en':{'subfamily of molluscs':'onderfamilie van weekdieren'}},\
      {'en':{'family of molluscs':'familie van weekdieren'}},\
      {'en':{'genus of viruses':'geslacht van virussen'}},\
      {'en':{'genus of spiders':'geslacht van spinnen'}},\
      {'en':{'genus of roundworms':'geslacht van rondwormen'}},\
      {'en':{'genus of orthopterans':'geslacht van rechtvleugeligen'}},\
      {'en':{'genus of liverworts':'geslacht van levermossen'}},\
      {'en':{'genus of ':'geslacht van '}},\
      {'en':{'extinct family of reptiles':'uitgestorven familie van reptielen'}},\
















def wd_sparql_query(spq):
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd in generator:
     try:
       wd.get(get_redirect=True)
       yield wd
     except:
       pass


#query='select ?item where {?item wdt:P31 wd:Q16521 ;         wdt:P105 wd:Q34740 .   ?item schema:description \"%s\"@%s .   ?item schema:description \"taxon\"@nl }'  % (descr,lng)   
#print(query)
#for item in wd_sparql_query(query):
#  print(item.title())  
#  dsc={'descriptions':{'nl':newdesc}}
#  try:
#      item.editEntity(dsc,summary='#genus-update')
#  except:
#      pass    
#  #print(1/0)

for item in solve:
  for lng in item:
    #print(lng, item[lng])
    for descr in item[lng]:
        newdesc=item[lng][descr]
        print('%s|%s|%s' % (lng,descr,newdesc))
        query='select ?item where {?item wdt:P31 wd:Q16521 ;         wdt:P105 wd:Q34740 .   ?item schema:description \"%s\"@%s .   ?item schema:description \"taxon\"@nl }'  % (descr,lng)
        for item in wd_sparql_query(query):
          dsc={'descriptions':{'nl':newdesc}}
          try:
            item.editEntity(dsc,summary='#genus-update')
          except Exception as e:
            pass  
            #print(sys.exc_info()[0])  
            print(e)
            time.sleep(10)
