import pywikibot
from pywikibot import pagegenerators as pg
import codecs

site=pywikibot.Site('de','wikipedia')
repo=pywikibot.Site('wikidata','wikidata').data_repository()
template='Personendaten'
parameter='KURZBESCHREIBUNG'
writeWD=True  #not yet, first analyse logfile for what we encounter

shortlist=['Giuseppe Natale Vegezzi','Carl Frank (Orientalist)','Theodor Dieter','Gottlieb Franz Münter','Peter Greil']

def csvprint(mytxt):
    with codecs.open('kurzbesch.csv','a',encoding='utf-8') as logfile:
      logfile.write('%s\n' % mytxt)
    logfile.close;

def all_templates_with(search4template):
  refPage = pywikibot.Page(pywikibot.Link('template:'+search4template,site))
  gen = pg.ReferringPageGenerator(refPage)
  for page in gen:
    if (page.namespace()==0) and('wikibase_item' in page.properties()):
      yield page

def getKurzBeschreibung(page):
  txt=page.text.lower()
  start1=txt.find('{{'+template.lower())
  start2=start1+txt[start1:].find('kurzbeschreibung')
  while txt[start2]!='=':
    start2+=1
  end=start2 
  while(txt[end] not in ['\n']):
    end+=1
  #print(f'{start1}-{start2}-{end}')
  if (start1>0) and (start2>0) and (end>0):
    return(page.text[start2+1:end])  
  return('')
    
def action_one_page(thispage):
  if ('wikibase_item' in thispage.properties()):
   try:
    wd=thispage.data_item()
    wd.get(get_redirect=True)
    if not('de' in wd.descriptions):
        kb=getKurzBeschreibung(thispage)
        if (writeWD):
            wd.editEntity({'descriptions':{'de':kb}},summary='DE kurzbeschreibung vom Personendata')
        csvprint(f'{wd.title()},[{kb}]')
   except:
    pass  

        
def get_shortlist():
    for p in shortlist:
        page=pywikibot.Page(site,p)
        yield(page)
        
        
print(f'Start')    
for onepage in all_templates_with(template):
#for onepage in get_shortlist():    
   action_one_page(onepage) 
print(f'Klaar!')    
