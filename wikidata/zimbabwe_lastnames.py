import pywikibot
import pywikibot.pagegenerators as pg 

site=pywikibot.Site('sn','wikipedia')
repo=site.data_repository()
catname='Category:Mazita eVanhu'
cat = pywikibot.Category(site,catname)
gen = pg.CategorizedPageGenerator(cat,12)


def onePage(page):
  if ('wikibase_item' in page.properties()):
    wd=page.data_item()
    wd.get(get_redirect=True)
    if (not ('nl' in wd.labels)) and (not('en' in wd.labels)):
      #print(f'labels: {page.title()}')  
      wddata={}
      labels={}
      labels.update({'en':page.title()})
      labels.update({'nl':page.title()})
      wddata.update({'labels':labels})
      descriptions={}
      descriptions.update({'en':'family name'})
      descriptions.update({'nl':'familienaam'})
      wddata.update({'descriptions':descriptions})
      try:
        wd.editEntity(wddata,summary='set labels and descriptions')
      except:
        print(wd.title())    
  
    if (not('P31' in wd.claims)):
      #print(f'claims: {page.title()}')  
      claim=pywikibot.Claim(repo,'P31')
      target=pywikibot.ItemPage(repo,'Q101352')
      claim.setTarget(target)
    
      sourceclaim=pywikibot.Claim(repo,'P248')
      sourcetarget=pywikibot.ItemPage(repo,'Q8571809')
      sourceclaim.setTarget(sourcetarget)
      claim.addSources([sourceclaim])
    
      wd.addClaim(claim,summary='category from Shona Wikipedia')
      #error()

for page in gen:
  onePage(page)
    

print(f'klaar: {page.title()}')    