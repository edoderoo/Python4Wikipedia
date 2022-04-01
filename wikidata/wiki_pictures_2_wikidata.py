import pywikibot
from pywikibot import pagegenerators

site=pywikibot.Site('nl','wikipedia')
repo=site.data_repository()
commonssite = pywikibot.Site('commons', 'commons')
skippers=[' ']
endofline=['|','\n']

def findStartEndInfobox(page,infobox):
  start=page.text.lower().find(infobox)
  if start>0:
   end=start     
   level=0      
   while ((page.text[end:end+2]!='}}') or (level>0)):      
     end+=1
     if (page.text[end:end+2]=='{{'):
      level+=1
      #print('level up',level)
     if (page.text[end:end+2]=='}}'):
      level-=1   
      #print('level dn',level)  
   return(start,end)
  else:
   return(-1,-1)

def getImageName(text,name='afbeelding'):
  end=start=text.find(name)
  if (start<0) or (end<0): return('')
  while(text[start:start+1]!='='):
    start+=1

  start+=1  
  while(text[start:start+1] in skippers):
    start+=1;
  end=start  
  while(not(text[end:end+1] in endofline)):
    end+=1
  return(text[start:end])  

def actionBridge(wd,page):
  start,end=findStartEndInfobox(page,'infobox brug')
  #print(start,end)
  imagename=getImageName(page.text[start:end])
  if (imagename!=''):
      imagelink=pywikibot.Link(imagename,source=commonssite,default_namespace=6)
      target=pywikibot.FilePage(imagelink)
      claim=pywikibot.Claim(repo,'P18')
      claim.setTarget(target)
      wd.addClaim(claim,summary='image from nl-wiki')
      print(page.title(),'|',imagename)

def AllFromCat(thiscat):
  cat = pywikibot.Category(site,thiscat)
  gen = pagegenerators.CategorizedPageGenerator(cat,12)
  for src_page in gen:
    yield(src_page) 

print('Start')     
for page in AllFromCat('Brug naar land'):
  #print(page.title())  
  if ('wikibase_item' in page.properties()):
    wd=page.data_item()
    wd.get(get_redirect=True)
    if (not('P18' in wd.claims)):
      actionBridge(wd,page)  
print('Klaar')  
