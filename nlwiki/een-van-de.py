import pywikibot
from pywikibot import pagegenerators as pg
searchNreplace={
    'zijn één van de ':'is een van de ',
    'is één van de ':'is een van de ',
    '\'één van de ':'\'een van de ',
    '\"één van de ':'\"een van de ',
    'Één van de ':'Een van de ',
    ' één van de ':' een van de ',
    '(één van de ':'(een van de ',
   }
skiplist=['nummer één van de ','één van de twee']
skips=['Lijst van personen overleden in januari 2019','Vestia (woningcorporatie)','Kapitein Zeppos','Nederlandse Grondwet','The least we can do is wave to each other','Heuvelse kerk','Lijst van personen overleden in januari 2019','Jeanet van der Laan','Lijst van personen overleden in januari 2019','Top 2000 (Nederland)']
todolist=[
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
         ]

def fixApage(page):
 if (not (page.title in skips)) and page.exists():
  for txt2search in searchNreplace:
    replacetxt=searchNreplace[txt2search] 
    #print(txt2search,replacetxt)
    pos=page.text.find(txt2search)
    if (pos>10) and (page.text[pos-6:pos+4]=='nummer één'):
      print('%s: found'%txt2search)
      return
    #else:
    #  print(pos,'[%s]'%page.text[pos-6:pos+4])
    page.text=page.text.replace(txt2search,replacetxt)
  page.put(page.text,summary='zie de TaalUnie: https://taaladvies.net/een-of-een-van-de/')  
    
def DoAllPages(site):
  print('Start')    
  for page in site.search(txt2search):
    if (page.text.find(txt2search)>0):
      print(page.title())
      fixApage(page)
  print('Klaar')

def TodoList(site):
 for pagename in todolist:
  if (pagename!=''):  
   print(pagename) 
   page=pywikibot.Page(site,pagename)
   fixApage(page)


site=pywikibot.Site('nl','wikipedia')
#page=pywikibot.Page(site,'Boogschieten op de Olympische Zomerspelen 2016 – Mannen (individueel)')
#fixApage(page)
#DoAllPages(site)
TodoList(site)
print('Klaar!')
