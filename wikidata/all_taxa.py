
import pywikibot
from pywikibot import pagegenerators as pg

query = 'select * where{{ select ?item ?itemDescription where {?item wdt:P31 wd:Q16521 . {service wikibase:label {bd:serviceParam wikibase:language "nl"}} }}filter (!bound(?itemDescription))}'
query = 'SELECT ?item ?descr WHERE { ?item wdt:P31 wd:Q16521 . ?item wdt:P171 ?sadf . OPTIONAL {?item schema:description ?descr . FILTER(lang(?descr)="nl") }      FILTER (str(?descr)=\'taxon\') }' #taxons with description=taxon
query = 'select ?item where {?item wdt:P31 wd:Q16521 . }'


query='select ?item where { ?item wdt:P31 wd:Q16521 }'
query='select ?item where { ?taxon wdt:P31 wd:Q16521 . ?taxon wdt:P171 ?item}'
query='SELECT * { ?item schema:description "taxon"@nl }'
mthrtxn_query='select ?item where {?item wdt:P31 wd:Q16521 . ?item wdt:P171 wd:%s OPTIONAL {?item schema:description ?d . FILTER(lang(?d)="nl")} FILTER (str(?d)="taxon") }'


import pywikibot
from pywikibot import pagegenerators
#import pywikibot.data.wikidataquery as wdquery
from pywikibot import pagegenerators as pg

import codecs #used in logfiles, unicoded strings
import sys
import datetime
from datetime import datetime, date, time

replacedesc={'nl':['taxon','',]}
taxondescs={
            'family of alga'            :{'nl':u'taxon, familie van algen'},
            'family of algae'           :{'nl':u'taxon, familie van algachtigen'},
            'family of arachnids'       :{'nl':u'taxon, familie van spinachtigen'},
            'family of birds'           :{'nl':u'taxon, familie van vogels'},
            'family of brachiopods'     :{'nl':u'taxon, familie van armpotigen'},
            'family of bryozoans'       :{'nl':u'taxon, familie van mosdiertjes'},
            'family of cnidarians'      :{'nl':u'taxon, familie van neteldieren'},
            'family of crustaceans'     :{'nl':u'taxon, familie van kreeftachtigen'},
            'family of echinoderms'     :{'nl':u'taxon, familie van stekelhuidigen'},
            'family of fishes'          :{'nl':u'taxon, familie van vissen'},
            'family of fungi'           :{'nl':u'taxon, familie van schimmels'},
            'family of gastrotrichs'    :{'nl':u'taxon, familie van buikharigen'},
            'family of insects'         :{'nl':u'taxon, familie van insecten'},
            'family of mammals'         :{'nl':u'taxon, familie van zoogdieren'},
            'family of molluscs'        :{'nl':u'taxon, familie van weekdieren'},
            'family of plants'          :{'nl':u'taxon, familie van planten'},
            'family of prokaryotes'     :{'nl':u'taxon, familie van prokaryoten'},
            'family of reptiles'        :{'nl':u'taxon, familie van reptielen'},
            'family of sea spiders'     :{'nl':u'taxon, familie van zeespinnen'},
            'family of waterbears'      :{'nl':u'taxon, familie van beerdiertjes'},
            'family of worms'           :{'nl':u'taxon, familie van wormen'},
                                     
            'genus of alga'             :{'nl':u'taxon, geslacht van algen'},
            'genus of algae'            :{'nl':u'taxon, geslacht van algachtigen'},
            'genus of amphibians'       :{'nl':u'taxon, geslacht van amfibieën'},
            'genus of arachnids'        :{'nl':u'taxon, geslacht van spinachtigen'},
            'genus of arthropods'       :{'nl':u'taxon, geslacht van duizendpoten'},
            'genus of birds'            :{'nl':u'taxon, geslacht van vogels'},
            'genus of brachiopods'      :{'nl':u'taxon, geslacht van armpotigen'},
            'genus of bryozoans'        :{'nl':u'taxon, geslacht van mosdiertjes'},
            'genus of cnidarian'        :{'nl':u'taxon, geslacht van neteldieren'},
            'genus of cnidarians'       :{'nl':u'taxon, geslacht van neteldieren'},
            'genus of crustaceans'      :{'nl':u'taxon, geslacht van kreeftachtigen'},
            'genus of echinoderms'      :{'nl':u'taxon, geslacht van stekelhuidigen'},
            'genus of fishes'           :{'nl':u'taxon, geslacht van vissen'},
            'genus of fungi'            :{'nl':u'taxon, geslacht van schimmels'},
            'genus of gastrotrichs'     :{'nl':u'taxon, geslacht van buikharigen'},
            'genus of insects'          :{'nl':u'taxon, geslacht van insecten'},
            'genus of mammals'          :{'nl':u'taxon, geslacht van zoogdieren'},
            'genus of molluscs'         :{'nl':u'taxon, geslacht van weekdieren'},
            'genus of myriapods'        :{'nl':u'taxon, geslacht van duizendpotigen'},
            'genus of plants'           :{'nl':u'taxon, geslacht van planten'},
            'genus of prokaryotes'      :{'nl':u'taxon, geslacht van prokaryoten'},
            'genus of reptiles'         :{'nl':u'taxon, geslacht van reptielen'},
            'genus of sea spiders'      :{'nl':u'taxon, geslacht van zeespinnen'},
            'genus of sponges'          :{'nl':u'taxon, geslacht van sponsachtigen'},
            'genus of trilobites'       :{'nl':u'taxon, geslacht van drielobbigen'},
            'genus of viruses'          :{'nl':u'taxon, geslacht van virussen'},
            'genus of waterbears'       :{'nl':u'taxon, geslacht van beerdiertjes'},
            'genus of worms'            :{'nl':u'taxon, geslacht van wormen'},

            'nothospecies of plant'     :{'nl':u'taxon, nothospecies van planten'},
            
            'order of alga'             :{'nl':u'taxon, orde van algen'},
            'order of algae'            :{'nl':u'taxon, orde van algachtigen'},
            'order of amphibians'       :{'nl':u'taxon, orde van amfibieën'},
            'order of arachnids'        :{'nl':u'taxon, orde van spinachtigen'},
            'order of birds'            :{'nl':u'taxon, orde van vogels'},
            'order of brachiopods'      :{'nl':u'taxon, orde van armpotigen'},
            'order of cnidarian'        :{'nl':u'taxon, orde van neteldieren'},
            'order of crustaceans'      :{'nl':u'taxon, orde van kreeftachtigen'},
            'order of fishes'           :{'nl':u'taxon, orde van vissen'},
            'order of fungi'            :{'nl':u'taxon, orde van schimmels'},
            'order of gastrotrichs'     :{'nl':u'taxon, orde van buikharigen'},
            'order of insects'          :{'nl':u'taxon, orde van insecten'},
            'order of mammals'          :{'nl':u'taxon, orde van zoogdieren'},
            'order of molluscs'         :{'nl':u'taxon, orde van weekdieren'},
            'order of plants'           :{'nl':u'taxon, orde van planten'},
            'order of prokaryotes'      :{'nl':u'taxon, orde van prokaryoten'},
            'order of reptiles'         :{'nl':u'taxon, orde van reptielen'},
            'order of sea spiders'      :{'nl':u'taxon, orde zeespinnen'},
            'order of waterbears'       :{'nl':u'taxon, orde van beerdiertjes'},
            'order of worm'             :{'nl':u'taxon, orde van wormen'},
                                     
            'tribe of arachnids'        :{'nl':u'taxon, geslachtengroep van spinachtigen'},
            'tribe of insects'          :{'nl':u'taxon, geslachtengroep van insecten'},
            'tribe of mammals'          :{'nl':u'taxon, geslachtengroep van zoogdieren'},
            'tribe of plants'           :{'nl':u'taxon, geslachtengroep van planten'},
            'tribe of reptiles'         :{'nl':u'taxon, geslachtengroep van reptielen'},
                                     
            'section of plants'         : {'nl':u'taxon, sectie van planten'},

            'series of plants'          : {'nl':u'taxon, reeks van planten'},
            
            'species of alga'           :{'nl':u'taxon, soort van algen'},
            'species of annelid'        :{'nl':u'taxon, soort van ringwormen'},
            'species of amphibian'      :{'nl':u'taxon, soort van amfibieën'},
            'species of arachnid'       :{'nl':u'taxon, soort van spinnen'},
            'species of arachnids'      :{'nl':u'taxon, soort van spinachtigen'},
            'species of arthropods'     :{'nl':u'taxon, soort van duizendpoten'},
            'species of bird'           :{'nl':u'taxon, soort van vogels'},
            'species of brachiopods'    :{'nl':u'taxon, soort van armpotigen'},
            'species of bryozoan'       :{'nl':u'taxon, soort van mosdiertjes'},
            'species of chordates'      :{'nl':u'taxon, soort van chordadieren'},
            'species of cnidarian'      :{'nl':u'taxon, soort van neteldieren'},
            'species of crustacean'     :{'nl':u'taxon, soort van kreefachtigen'},
            'species of ctenophore'     :{'nl':u'taxon, soort van ribkwallen'},
            'species of echinoderm'     :{'nl':u'taxon, soort van paddenstoelen'},
            'species of entoprocts'     :{'nl':u'taxon, soort van kelkwormen'},
            'species of gastrotrichs'   :{'nl':u'taxon, soort van buikharigen'},
            'species of insect'         :{'nl':u'taxon, soort van insecten'},
            'species of fungus'         :{'nl':u'taxon, soort van schimmels'},
            'species of fish'           :{'nl':u'taxon, soort van vissen'},
            'species of mammal'         :{'nl':u'taxon, soort van zoogdieren'},
            'species of mollusc'        :{'nl':u'taxon, soort van weekdieren'},
            'species of myriapod'       :{'nl':u'taxon, soort van duizendpotigen'},
            'species of plant'          :{'nl':u'taxon, soort van planten'},
            'species of prokaryote'     :{'nl':u'taxon, soort van prokaryoten'},
            'species of reptile'        :{'nl':u'taxon, soort van reptielen'},
            'species of rotifers'       :{'nl':u'taxon, soort van raderdieren'},
            'species of sea spiders'    :{'nl':u'taxon, soort van zeespinnen'},
            'species of sponge'         :{'nl':u'taxon, soort van sponsachtigen'},
            'species of waterbears'     :{'nl':u'taxon, soort van beerdiertjes'},
            'species of virus'          :{'nl':u'taxon, soort van virussen'},
            'species of worm'           :{'nl':u'taxon, soort van wormen'},
                                     
            'spider family'             :{'nl':u'taxon, familie van spinachtigen'},
                                     
            'subfamily of arachnids'    :{'nl':u'taxon, onderfamilie van spinachtigen'},
            'subfamily of birds'        :{'nl':u'taxon, onderfamilie van vogels'},
            'subfamily of crustaceans'  :{'nl':u'taxon, onderfamilie van kreeftachtigen'},
            'subfamily of fishes'       :{'nl':u'taxon, onderfamilie van vissen'},
            'subfamily of insects'      :{'nl':u'taxon, onderfamilie van insecten'},
            'subfamily of mammals'      :{'nl':u'taxon, onderfamilie van zoogdieren'},
            'subfamily of molluscs'     :{'nl':u'taxon, onderfamilie van weekdieren'},
            'subfamily of plants'       :{'nl':u'taxon, onderfamilie van planten'},
            'subfamily of reptiles'     :{'nl':u'taxon, onderfamilie van reptielen'},
            'bird'                      :{'nl':u'taxon, vogel'},
            
            'subgenus of insects'       :{'nl':u'taxon, ondergeslacht van insecten'},
            'subgenus of mammals'       :{'nl':u'taxon, ondergeslacht van zoogdieren'},
            'subgenus of plants'        :{'nl':u'taxon, ondergeslacht van planten'},

            'subtribe of insects'       :{'nl':u'taxon, ondertribus van insecten'},
            'subtribe of plants'        :{'nl':u'taxon, ondertribus van planten'},

            'superfamily of insects'    :{'nl':u'taxon, superfamilie van insecten'},
            'superfamily of molluscs'   :{'nl':u'taxon, superfamilie van weekdieren'},
            'superfamily of plants'     :{'nl':u'taxon, superfamilie van planten'},
            
            'variety of algae'          :{'nl':u'taxon, variëteit van algachtigen'},
            'variety of plants'         :{'nl':u'taxon, variëteit van planten'},

            
            'x!y~z':{'nl':''},
           }

debugedo=True
debugedo=False
debug=False

default_query='claim[31:16521]'  #all taxons
default_language = 'nl' 

#global variables
items2do = 0
itemsdone= 0
missing_dict={}


def log_premature(itemno):
  with codecs.open("taxon-description.prelog.csv","a", encoding="utf-8") as logfile:
    logfile.write('%s\n' % (itemno))
  logfile.close
def logme(verbose, formatstring, *parameters):
  with codecs.open("taxon-description.log.csv", "a", encoding="utf-8") as logfile:
    formattedstring = u'%s%s' % (formatstring, '\n')
       
    try:   
      logfile.write(formattedstring % (parameters) )
    except :
      exctype, value = sys.exc_info()[:2]
      print("1) Error writing to logfile on: [%s] [%s]" % (exctype, value))
      verbose = True    #now I want to see what!   
    logfile.close()
  if verbose:
    print(formatstring % (parameters))  


def action_one_item(wditem):
  global items2do
  global itemsdone
  global missing_dict
  
  items2do -= 1
  str1 = '{:>10d}'.format(itemsdone)
  str2 = '{:>10}'.format(wditem.title())
  str3 = '{:>10d}'.format(items2do)
  sys.stdout.write("\r%s%s%s" % (str1, str3, str2))     #print how many items we still have to do ... 
     
  if ('nl' in wditem.descriptions):
    orig_desc = wditem.descriptions['nl']
  else:
    orig_desc = ''  
     
  if ('en' in wditem.descriptions):
    en_desc = wditem.descriptions['en']
    if (en_desc in taxondescs):
      data = {}
      my_dict=taxondescs[en_desc]
      for lang in my_dict:
        if lang in wditem.descriptions:
          if (wditem.descriptions[lang] in replacedesc[lang]):
            data.update({'descriptions':{lang:my_dict[lang]}})
            if debug:
              print('Debug: %s' % data)
            else:
              log_premature(wditem.title())
              wditem.editEntity(data,summary=u'WD-taxon-description.py [[User:Edoderoobot/WD-taxon-description.py|source]]')
              logme(False,'%s|%s|%s|%s|%s|%s',datetime.now().strftime("%Y-%b-%d/%H:%M:%S"),wditem.title(),'nl',orig_desc,my_dict[lang],'taxon-descript')
    else:
      if en_desc in missing_dict:
        missing_dict[en_desc] += 1
      else:
        missing_dict.update({en_desc:1})
    return 1     
    
  return 0

def wd_sparql_generator(query):        
  wikidatasite=pywikibot.Site('wikidata','wikidata') 
  generator=pg.WikidataSPARQLPageGenerator(query,site=wikidatasite)
  
  for wd in generator:
    if (not wd.isRedirectPage()):
     if (wd.exists()):
      wd.get(get_redirect=True)
      yield wd

def main():
  site=pywikibot.Site('wikidata','wikidata')
  repo=site.data_repository()
  print('Start generator|')
  i = 0
  generator = wd_sparql_generator(query)
  for mothertaxon in generator:
    m_query=mthrtxn_query % mothertaxon.title()
    mgen = wd_sparql_generator(m_query)
    for taxon in mgen:
      if ('nl' in taxon.descriptions):
        nl=taxon.descriptions['nl']
      else:
        nl=''
      if ('en' in taxon.descriptions):
        en=taxon.descriptions['en']
      else:
        en=''
      
      if (nl in ['','taxon']) and (en not in ['']):
        i += 1
        print('%d-%s-%40.40s-%40.40s' % (i,taxon.title(),en,nl))
        action_one_item(taxon)
  print('Klaar')
    
main()
