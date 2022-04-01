import pywikibot
from pywikibot import pagegenerators as pg

maxpages=55
replace_on_page=True
findpages=True

emptychars=' '
stopchars='|]'

def replace_link(page,link,initsavepage):
   savepage=initsavepage
   start=page.text.lower().find('[['+link.lower()+']]')
   stop=start+4+len(link)
   if replace_on_page:
      if stop>start: print('Replace: <%s>' % page.text[start:stop]) 
      if (page.text[start:start+2]=='[[') and (page.text[stop-2:stop]==']]'):
        page.text = page.text[0:start] + page.text[start+2:stop-2]+'<!--'+page.text[start:stop]+' is een doorverwijspagina-->{{dpweg}}' + page.text[stop:]
        savepage=True
   return(page.text,savepage)

def process_one_page(site,page):
  savepage=False
  oneFound = False
  for onelink in page.linkedPages():
    if onelink.isDisambig():
      print('l:%s' % onelink.title())
      page.text,savepage = replace_link(page,onelink.title(),savepage)
      oneFound=True
  if (replace_on_page):
    pass
    #print('New text:\n%s' % page.text)
  if (savepage):
    pywikibot.Page(site,page.title()).put(page.text,summary='#dpweg')
    #print('Page saved!')
  return(oneFound)        


print('Begonnen')
site=pywikibot.Site('nl')
if findpages:
  mygenerator=pg.NewpagesPageGenerator(site,0,maxpages)
  for onepage in mygenerator:
    print('p:%s' % onepage.title())
    if (process_one_page(site,onepage)):
      print('-------------------------------')
else:
  onepage=pywikibot.Page(site,'By George, by Bachman: Songs of George Harrison')  
  process_one_page(site,onepage)  

print('Klaar')    