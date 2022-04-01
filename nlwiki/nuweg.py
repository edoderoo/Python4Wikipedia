#20210110 1543

import pywikibot
from pywikibot import pagegenerators
import datetime
from urllib.parse import quote

cat='Categorie:Wikipedia:Nuweg'
pagename='Wikipedia:Te beoordelen pagina\'s/Direct te verwijderen'
pagename='Gebruiker:Edoderoo/nuweg'
site=pywikibot.Site('nl','wikipedia')
page=pywikibot.Page(site,pagename)
allowednamespaces=[0,1,2,3,4,5,6] #main/talk/user/usertalk
commit=True
skiplinks=[
    'Wikipedia:Te beoordelen',
    'Wikipedia:Te beoordelen pagina\'s/Archief/2020',
    'Wikipedia:Richtlijnen voor moderatoren',
    'Wikipedia:Te beoordelen afbeeldingen',
    'Wikipedia:Te beoordelen categorieën',
    'Wikipedia:NUWEG',
    'Wikipedia:NW',
    'Wikipedia:Te beoordelen pagina\'s',
    'Wikipedia:Te beoordelen sjablonen',
    'Wikipedia:Verzoekpagina voor moderatoren/Artikel verplaatsen',
    '',
    '',
    
    ]
edited=False
header='!Artikel!!Genomineerd door!!Aantal edits!! tijd'

def countRevisions(page):
    counter=0
    for rev in page.revisions(content=True):
      counter += 1
    return(counter)    

def findNuwegUser(page):
  print(f'find user for page {page.title()}')  
  user=None
  for rev in page.revisions(content=True):
    if (rev.text.lower().find('{{nuweg')>-1):
      user=rev.user
  return user

def clearRedLinks(page):
    for link in page.linkedPages(namespaces=0):
        if not link.exists():
            pass
            #print(link.title())

def linkIsOnPage(page,linkedname,xxx):
  #print(f'\n\nlinkIsOnPage: {linkedname}-{xxx}')
  if (False):  #oude manier, werkt niet meer door sjabloon {{intern}}
   for link in page.linkedPages(namespaces=allowednamespaces):
     if (link.title() not in skiplinks):  
       pass 
       #print(f'Link: {link.title()}')   
     if link.title().lower()==linkedname.lower():
       print('True')    
       return(True)
  return (page.text.lower().find(linkedname.lower())>0)
  print('False')
  return(False)

def addLinkOnPage(page,linkedname,nuwegUser,nrEdits):
  global edited
  if not linkIsOnPage(page,linkedname,-1):
    nu=datetime.datetime.now()
    nutxt=f'{nu:%Y-%m-%d %H:%M}'  
    """
    if (not edited):
      edited=True
      page.text = page.text[:len(page.text)-2]
    """  
    anchor=page.text.find(header)+len(header)
    newtext = page.text[:anchor]
    newtext += '\n|-\n|{{#ifexist:%s|{{intern|1=title=%s|2=%s}}|[[%s]]}} || (%s) || %s edits || %s' % (quote(linkedname),quote(linkedname),linkedname,linkedname,nuwegUser,nrEdits,nutxt)
    newtext += page.text[anchor:]
  return newtext  

def deleteOneLink(page,pos):
  start=pos
  end=pos
  while page.text[start:start+1]!='\n':
    start-=1
  while page.text[end:end+1]!='\n':
    end+=1

"""
def getLinkDateTime(page,pos):
  start=pos

def deleteLinks(page):
  for link in page.linkedPages(namespaces=allowednamespaces):
    if not link.exists(): #only delete red links
      pass
"""

def allfromcat(thiscat):
    global edited
    cat = pywikibot.Category(site,thiscat)
    gen = pagegenerators.CategorizedPageGenerator(cat,123)
    for src_page in gen:
      print('%s' % src_page.title())  
      if not (linkIsOnPage(page,src_page.title(),src_page.namespace().id)):
          page.text=addLinkOnPage(page,src_page.title(),findNuwegUser(src_page),countRevisions(src_page))
          if page.namespace().id not in allowednamespaces:
              print(f'Namespace #{page.namespace().id} is not yet allowed?')  
    if (commit):
        if edited: page.text+='\n|}'
        page.put(page.text,'++ uit categorie:wikipedia:nuweg')
    else:
        print(page.text)

        
print('Start-')
allfromcat(cat)  
#clearRedLinks(page)
print('Klaar')
