#20200604-1948
import pywikibot
from pywikibot import pagegenerators as pg

#village in Russia


language='en'
descrStart='village in '
descrEnd=', Russia'
find='village in Russia'

language='nl'
descrStart='dorp in '
descrEnd=', Russia'
find='dorp in Rusland'

language='de'
descrStart='Dorf in '
descrEnd=', Russland'
find='Dorf in Russland'


query='SELECT * { ?item schema:description "%s"@%s }' %(find,language)
counter=-1
backuplanguage='en'

def wd_sparql_query(spq):
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd in generator:
     try:
       wd.get(get_redirect=True)
       yield wd
     except:
       pass

site = pywikibot.Site('wikidata','wikidata')           #Geef aan naar welke site je wilt schrijven
repo = site.data_repository()                     #voor ophalen wikidata-items adhv Qxxxx

print('Start')
for item in wd_sparql_query(query):
    p131label=None
    if (item.descriptions[language]==find):  #avoid database lag, item might be just changed
      if ('P131' in item.claims):
        itisin=item.claims['P131'][0].getTarget().title()
        wd=pywikibot.ItemPage(repo,itisin)
        wd.get(get_redirect=True)
        if language in wd.labels:
          p131label=wd.labels[language]
        else:
          if (backuplanguage in wd.labels):
            p131label=wd.labels[backuplanguage]
          else:  
            if ('P131' in wd.claims):
              itisin=wd.claims['P131'][0].getTarget().title()
              wd=pywikibot.ItemPage(repo,itisin)
              wd.get(get_redirect=True)
              if language in wd.labels:
                p131label=wd.labels[language]
              else:
                if (backuplanguage in wd.labels):
                  p131label=wd.labels[backuplanguage]  
                else:    
                  print(f'No label in {item.title()}')
        if (p131label):
            item.editEntity({'descriptions': {language:f'{descrStart}{p131label}{descrEnd}'}},summary=f'Update {language}-label for Russian village')
            x=1/(counter)
            counter-=1
      else:
        print(f'No P131 in {item.title()}')
print('All done') 