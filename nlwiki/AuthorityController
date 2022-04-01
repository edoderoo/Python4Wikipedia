#20201126 1324
#
# Find pages without {{Autohority control}} that do have something to show
#
# [[Potaro]] had }}}} 
import pywikibot
from pywikibot import pagegenerators

possProp={'P214','P213','P227','P1006','P1048','P1225','P7859'}
addAppendix='{{Appendix|2=\n{{References}}\n}}{{Bibliografische informatie}}\n'
Commit=True
#Commit=False #do not write changes, but show them to test

def templateEnd(txt,start,inside=False):
  i=start+1  
  level=0
  while (txt[i:i+2]!='}}') or (level>0):
    if (txt[i:i+2]=='{{'):
      level+=1
    if (txt[i:i+2]=='}}'):
      level-=1
    i+=1
  if (inside):  
    return i+2
  else:
    return i+2  


def addAC(page):
    doprint=not Commit
    if not Commit: print(page.title())
    if page.text.lower().find('{{authority control}}')>0: 
        if not Commit: print('AC-exists')
        return
    if page.text.lower().find('{{bibliografische informatie}}')>0: 
        if not Commit: print('BI-exists')
        return
    print('start')
    end=0
    prefix=''
    start=page.text.lower().find('{{appendix}}')
    if (start>0):
      if not Commit: 
        print('--->!A')
        doprint=False
      end=templateEnd(page.text,start)  
      #prefix='\n'
    else:   
      start=page.text.lower().find('{{references}}}}')  
      if (start>0):
        if not Commit: 
            print('--->R')    
            doprint=True
        end=start+16    
      else:  
        start=page.text.lower().find('{{appendix')
        if (start>0):
          if not Commit: 
            print('--->!A-')    
            doprint=False
          end=templateEnd(page.text,start,inside=True)
          prefix=''
        else:
          start=page.text.lower().find('{{references')  
          if (start>0):
            if not Commit: 
                print('--->!R-')    
                doprint=False
            end=templateEnd(page.text,start)
            prefix='\n'
          else: #no appendix or reference find first [[categorie:]]
            start=page.text.lower().find('{{defaultsort:')
            if start<0:
              start=page.text.lower().find('[[categorie:')
              if (start<0):
                  print(f'Onverwachte situatie in {page.title()}')  
                  return
            if not Commit: print('--->???')    
            text=page.text[:start]+addAppendix+page.text[start:]   
            #print(text)
            page.put(text,summary='#add_Authority_control')
        
    if (start>0) and (end>start):    
        text=page.text[:end]+prefix+'\n{{Bibliografische informatie}}'+page.text[end:]
        if (Commit):
          page.put(text,summary='#add_Authority_control')
        else:
          if doprint: print(text)
            

def addline(page,wd):
    return('*[[%s]]\n'%page.title())

def allfromcat(thiscat):
    site=pywikibot.Site('nl','wikipedia')
    cat = pywikibot.Category(site,'categorie:'+thiscat)
    gen = pagegenerators.CategorizedPageGenerator(cat,123)
    addtxt=''
    for src_page in gen:
      if ((src_page.text.lower().find('{{authority control}}')>0) or (src_page.text.lower().find('{{bibliografische informatie}}')>0)):
         continue  #text already there
      #print('\r%s' % src_page.title())  
      try:
        wd=pywikibot.ItemPage.fromPage(src_page) 
        wd.get(get_redirect=True)
      except:
        continue
      canadd=False
      for tstclaim in possProp:
        if (tstclaim in wd.claims):
          canadd=True  
          addtxt+=addline(src_page,wd) 
          break
      if (canadd):  
        addAC(src_page)        
        #print(1/0)
    if (addtxt!=''):
        print(addtxt)
        #catpage=pywikibot.Page(site,'Overleg categorie:%s'%thiscat)
        #catreplace(catpage,addtxt)
        
print('--]Start[--')
#allfromcat('Koning van Schotland')
#Commit=False
allfromcat('Werelderfgoed in Polen')
#Commit=False
#page=pywikibot.Page(pywikibot.Site('nl','wikipedia'),'Paleis van Caserta')
#addAC(page)

print('--]Klaar[--')
