#2020-06-24 10:58
#Find articles with no commonscat-template, while wikidata has a commonscat defined

import pywikibot
from pywikibot import pagegenerators

sjabloon='CommonscatMistHier'

def action(page,wd):
  if not('{{commonscat' in page.text.lower()):  
    retval='*[[%s]]––%s\n' % (page.title(),wd.claims.get('P373')[0].getTarget())
    #print(retval)
    return(retval)

def catreplace(cat,txt):
    start=cat.text.find(sjabloon)
    end=cat.text.find('<!--'+sjabloon+'-->')
    #print(f'Start: {start}\nEnd..: {end}\n\n')
    if ((start<0) or (end<0) or (len(cat.text)==0)):
        cat.text+='\n==Missende Commons-categorieen==\n{{%s}}\n<!--%s-->'%(sjabloon,sjabloon)
        start=cat.text.find(sjabloon)
        end=cat.text.find('<!--'+sjabloon+'-->')
    newcattxt=cat.text[:start+len(sjabloon)+3]+txt+cat.text[end:]
    #print(newcattxt)
    cat.put(newcattxt,summary='Missende commons-cat bijgewerkt')

def allfromcat(thiscat):
    site=pywikibot.Site('nl','wikipedia')
    cat = pywikibot.Category(site,'categorie:'+thiscat)
    gen = pagegenerators.CategorizedPageGenerator(cat,123)
    addtxt=''
    for src_page in gen:
      #print('\r%s' % src_page.title())  
      try:
        wd=pywikibot.ItemPage.fromPage(src_page) 
        wd.get(get_redirect=True)
        if ('P373' in wd.claims):
          addtxt+=action(src_page,wd) 
      except:
        pass
    if (addtxt!=''):
        #print(addtxt)
        catpage=pywikibot.Page(site,'Overleg categorie:%s'%thiscat)
        catreplace(catpage,addtxt)

def allfromtemplate():
    site=pywikibot.Site('nl','wikipedia')
    page=pywikibot.Page(site,f'sjabloon:{sjabloon}')
    #gen = pagegenerators.NamespaceFilterPageGenerator(pagegenerators.ReferringPageGenerator(page),namespaces=[15])
    gen = pagegenerators.NamespaceFilterPageGenerator(page.getReferences(),namespaces=[15])
    for onepage in gen:
       start=onepage.title().find(':') 
       allfromcat(onepage.title()[start+1:])
        
print('Start')    
allfromtemplate()
#allfromcat('Roemeens schrijver')    
#allfromcat('Nederlands nieuwslezer')
print('Klaar')
