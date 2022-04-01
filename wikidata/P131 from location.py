#20190813 - 0828
import json
import requests
import pywikibot

api_token = '?id=%s&action=get_data&format=json&doit'
api_url_base = 'https://tools.wmflabs.org/pagepile/api.php'

mypile='25394'

def PagePyleGenerator(pile):
 url=api_url_base+api_token%pile
 data = requests.get(url)
 #print(dir(data))
 pile_lng  =json.loads(data.text)['language'] #language
 pile_prj  =json.loads(data.text)['project']  #project
 pile_items=json.loads(data.text)['pages_returned'] #nr of items
 pile_total=json.loads(data.text)['pages_total'] #pages_total

 plsite=pywikibot.Site(pile_lng,pile_prj)
 plrepo=plsite.data_repository()   
 
 pyle=(json.loads(data.text)['pages'])
 for oneitem in pyle:
    if (pile_lng=='wikidata'):
      plwd=pywikibot.ItemPage(plrepo,oneitem)
      plwd.get(get_redirect=True)  
      yield(plwd)
    else:
      plpage=pywikibot.Page(plsite,oneitem)
      yield(plpage)

def DoOnePage(wd):
   if ('P17' in wd.claims) and ('P131' in wd.claims): return; 
   print(f'Item: {wd.title()}') 
   if ('P276' in wd.claims) and (not('P131' in wd.claims)):
     #print('1')
     loc=pywikibot.ItemPage(repo,wd.claims['P276'][0].getTarget().title())
     loc.get()
     if ('P131' in loc.claims):
       #print('2')  
       entity=loc.claims['P131'][0].getTarget()
       if (entity): 
         entTarget=pywikibot.Claim(repo,'P131')  
         entTarget.setTarget(entity)
         wd.addClaim(entTarget,summary=f'set entity from location')
   """
   now add a country, if available in P131
   """
   if ('P131' in wd.claims) and (not('P17' in wd.claims)):
     #print('3')
     entity=pywikibot.ItemPage(repo,wd.claims['P131'][0].getTarget().title())
     entity.get()
     if ('P17' in entity.claims):
       #print('4')
       country=entity.claims['P17'][0].getTarget()
       if (country):
         cntrTarget=pywikibot.Claim(repo,'P17')
         cntrTarget.setTarget(country)
         wd.addClaim(cntrTarget,summary=f'set country from entity') 

print('Start')
repo=pywikibot.Site('wikidata','wikidata').data_repository()
wd=pywikibot.ItemPage(repo,'Q63020335')
wd.get()
for wd in PagePyleGenerator(mypile):
  DoOnePage(wd)
print('Klaar')