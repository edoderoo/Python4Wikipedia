import pywikibot
from pywikibot import pagegenerators as pg

site=pywikibot.Site('nl','wikipedia')
#printtype=['Q5']
printtype=None

def all_templates_with(search4template):
  refPage = pywikibot.Page(pywikibot.Link(search4template,site))
  gen = pg.ReferringPageGenerator(refPage)
  for page in gen:
    if (page.namespace()==0):
      yield page

def all_links_on(this_template):
  page=pywikibot.Page(site,this_template)
  for p in page.linkedPages():
     if (p.exists()):   
        yield p

def check_one_template(which_template):    
 #print(which_template)   
 for page in all_links_on(which_template): #get all pages with this template
   templatefound=False
   #print('--------------------------------------')
   #print(page.title())
   if (page.namespace().id) in [0]:
     #print('Regular page')
     for t in page.templates():
       templatefound= templatefound or (t.title().lower()==which_template.lower())
       #print(f'{t.title().lower()}--{templatefound}')   
     if (not templatefound):
       if ('wikibase_item' in page.properties()):
         wd=page.data_item()
         wd.get(get_redirect=True)
         if ('P31' in wd.claims):
          for claim in wd.claims['P31']:
            if (printtype==None) or (claim.getTarget().title() in printtype):
              print(f'{page.title()}--{which_template}')
   elif (page.namespace().id in [10]):
     if (page.text.find('{{'+which_template[9:]+'}}')==-1): 
       print(page.title())
   else:
     print(page.namespace().id)           

def all_from_cat(thisCat):        
   cat=pywikibot.Category(site,thisCat)     
   gen=pg.CategorizedPageGenerator(cat,99)
   for x in gen:
      ns=x.namespace()
      if (ns==10):
       if (x.text.lower().find('{{navigatie')>=0): 
        check_one_template(x.title())
        
print('Start')   
#all_from_cat('Categorie:Wikipedia:Sjablonen voetbalelftal Nederland')
#all_from_cat('Categorie:Wikipedia:Sjablonen Olympische Spelen')
#all_from_cat('Categorie:Wikipedia:Sjablonen sport')
#check_one_template('sjabloon:Navigatie selectie Ajax (vrouwen)')
check_one_template('Sjabloon:Navigatie selectie Cambuur Leeuwarden')
print('Klaar')
