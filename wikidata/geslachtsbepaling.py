import pywikibot

male='Q6581097'
female='Q6581072'

maletxt={' hij ',' hem ','hij was ','was hij ','hij maakte ','maakte hij ','hij werkte ','hij werd ','hij wordt ','heeft hij ','kwam hij ','hij kwam ','is hij ',' acteur ',' acteur.','[[acteur]]','|acteur]]','hij zijn ','hij is ','stond hij ',' zoon van '}
femaletxt={' zij ',' haar ','zij kwam ',' kwam zij ','ze kwam ','kwam ze ','heeft ze ','heeft zij ',' ze wordt ','zij werkte ','zij werd ','ze werd ','zij maakte ','maakte zij ','was ze ','ze was ','was zij ','zij was ','is zij ','is ze ','actrice ','actrice.','actrice]]','zij haar ','ze is ','stond ze ',' dochter van ',' werkt zij ',}


def addQ5(wd):
  if not 'P31' in wd.claims:  
    claim=pywikibot.Claim(repo,'P31')
    target=pywikibot.ItemPage(repo,'Q5')
    claim.setTarget(target)
    wd.addClaim(claim,summary='must be person')

def addSexe(wd,sexe):
  addQ5(wd)  
  if not 'P21' in wd.claims:  
    claim=pywikibot.Claim(repo,'P21')  
    target=pywikibot.ItemPage(repo,sexe)
    claim.setTarget(target)
    wd.addClaim(claim,summary='deduct gender from page.text')
    
def prepare_text(text):    
  text=text.lower()
  end=text.find('[[categorie:')  
  if end==-1:
    return(text)
  return(text[:end])

def eenpagina(page):
  man=0
  vrouw=0  
  if ('wikibase_item' in page.properties()):
    wd=page.data_item()
    wd.get(get_redirect=True) 
    if ('P31' in wd.claims):
      isa=wd.claims['P31'][0].getTarget().title()
      if isa!='Q5': return  #not a person, not undefined, don't add anything!

    page.text=prepare_text(page.text)
    for txt in maletxt:
      if page.text.find(txt)>0:
        if debug: print(txt)
        man+=1
    for txt in femaletxt:
      if page.text.find(txt)>0: 
        if debug: print(txt)
        vrouw+=1
    if (man>0) and (vrouw>0):
      print('-/-/-/-/-/->',page.title(),'both?',man,vrouw);  
    if (man==0) and (vrouw>0):
      print(page.title(),'Vrouw!',man,vrouw)
      addSexe(wd,female)
    if (vrouw==0) and (man>0):
      print(page.title(),'Man!',vrouw,man)
      addSexe(wd,male)
    if (man==0) and (vrouw==0):
      print('------------>',page.title(),'undefined!')  
        
debug=False
debug=True
mylist={
    '','','','','','',
    '','','','','',
    '','','','','',
    '','','','',''
    ,'','','','','',
    '','','','','',
    '','','','','','',''

}        
print('Start')    
site=pywikibot.Site('nl','wikipedia')
repo=site.data_repository()
for title in mylist:
 if (title!=''):   
  page=pywikibot.Page(site,title)
  eenpagina(page)
print('Klaar')
