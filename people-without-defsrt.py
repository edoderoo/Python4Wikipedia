
import pywikibot
from pywikibot import pagegenerators

mysite='nl'
mycat='Nederlands persoon'

site=pywikibot.Site(mysite)
cat=pywikibot.Category(site,mycat)
gen=pagegenerators.CategorizedPageGenerator(cat,12)
for page in gen:
  if (page.defaultsort() == None):
    if 'wikibase_item' in page.properties(): 
      wditem = page.data_item()
      wditem.get(get_redirect=True)
      if ('P31' in wditem.claims):
        for claim in wditem.claims.get('P31'):
          if (claim.getTarget().title()=='Q5'):  #if it's not a person, we just don't care about the sorting
            print(page.title())
  