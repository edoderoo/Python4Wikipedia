#2021-07-22 20:31
import pywikibot
from pywikibot import pagegenerators as pg
from pywikibot.data import api
import urllib.parse
from datetime import datetime
import sys
import string

#import sys, getopt
#import json
#import requests

language='nl'
lngwiki=f'{language}wiki'
site=pywikibot.Site(language,'wikipedia')
targetpage='user:Edoderoo/last-xxx-no-wikidata'
maxpages=250
header='{| class="wikitable sortable"\n|-\n! # !! Artikel !! tool !! TBP !! suspects !! Laatste bewerking !! Categorie\n'
wikitxt=''
footer='|}'
suggestURL=f'https://tools.wmflabs.org/wikidata-todo/duplicity.php?wiki={lngwiki}&norand=1&page='
translated='{{Bronvermelding anderstalige Wikipedia'
testpage='Monteverdi Tiara'
testpage=''
sameImage=False

def findExisting(text,search_for): #find suspects to connect page to, based on name

  global sameImage

  def getItems(site, itemtitle):
   params = { 'action' :'wbsearchentities' , 'format' : 'json' , 'language' : 'en', 'type' : 'item', 'search': itemtitle}
   request = api.Request(site=site,parameters=params)
   return request.submit()

  def firstImage(text):
    """
    def frompos(text,index,offset):
      #print(index,offset)
      res=''
      index=index+offset
      while(text[index:index+1]!='\n') and (text[index:index+2]!=']]') and (index<85):
        #print('. ',res)
        res+=text[index:index+1]
        index+=1
      print(res)
      return(res)

    shorttxt=text.replace(" ","",-1).lower() #remove all spaces to simplify search
    pos=shorttxt.find('afbeelding=')
    if pos>0:
      return(frompos(shorttxt,pos,11))
    pos=shorttxt.find('[[bestand:')
    if pos>0:
      return(frompos(shorttxt,pos,10))
    pass
    """
  def wdImageInText(text,wd):
    if ('P18' in wd.claims):
      for imagename in wd.claims['P18']:
        #print('Image name', imagename.getTarget())
        name=imagename.getTarget().title()
        #print(name)
        name=name.replace('File:','')
        #print(name)
        return(name)


  #firstimage=firstImage(text)  #niet nodig: kijk of de bestandsnaam van wikidata voorkomt in de artikeltekst, dat moet genoeg zijn
  sameImage=False #initially, not found
  ssite = pywikibot.Site("wikidata", "wikidata")
  srepo = site.data_repository()
  searchresult = getItems(ssite, search_for)
  result=[]
  for item in searchresult['search']:
     itemID=item['id']
     wd=pywikibot.ItemPage(srepo,item['id'])
     wd.get(get_redirect=True)
     if (lngwiki in wd.sitelinks):
       if (wd.sitelinks[lngwiki]==search_for):
         return None
     else:
       sameImage=sameImage or wdImageInText(text,wd)
       result.append(f'[[:d:{wd.title()}]]')
  return result

def getnewpages(mysite):
 if (testpage==''):
  for page in pg.WikibaseItemFilterPageGenerator(pg.NewpagesPageGenerator(site=mysite),has_item=False):
    try:
      if (page.exists()):
        yield(page)
    except:
      pass
 else:
  page=pywikibot.Page(site,testpage)
  yield(page)

def findTranslated(ptxt):
  return 'translated'

starttime=datetime.now()
if (len(sys.argv)>1):
  if (sys.argv[1][0:4].lower()=='lng='):
    language=sys.argv[1][4:].lower()
    print(f'Set language to: {language}')
    lngwiki=f'{language}wiki'
    site=pywikibot.Site(language,'wikipedia')
  elif (sys.argv[1][0:4].lower()=='max='):
    maxpages=int(sys.argv[1][4:])
    print(f'Set max suggestions to {maxpages}')
  else:
    print(f'{sys.argv[1]}-{sys.argv[1][0:4].lower()}')
wikitxt=header
counter=0
for page in getnewpages(site):
    #print(page.title())
    TBPtxt=''
    if (page.text.lower().find('{{ne')>-1):
      TBPtxt='ne'
    if (page.text.lower().find('{{wb')>-1):
      TBPtxt='wb'
    if (page.text.lower().find('{{wiu')>-1):
      TBPtxt='wiu'
    if (page.text.lower().find('{{weg')>-1):
      TBPtxt='weg'
    if (page.text.lower().find('{{verwijderen')>-1):
      TBPtxt='weg'
    if (page.text.lower().find('{{reclame')>-1):
      TBPtxt='reclame'
    if (page.text.lower().find('{{auteur')>-1):
      TBPtxt='auteur'
    if (page.text.lower().find('{{samenv')>-1):
      TBPtxt='samenv'
    if (page.text.lower().find('{{nuweg')>-1):
      continue
    if (page.text.lower().find('{{artikelweg')>-1):
      TBPtxt='artweg'
    if (page.text.lower().find('[[categorie:')>0):
      cattxt='√'
    else:
      cattxt=''
    if (page.text.find(translated)>-1):
      searchresult='\'\'\'%s\'\'\'' % findTranslated(page.text)
    else:
      searchresult=findExisting(page.text,page.title())
    params = {'q': '', '': page.title()}
    sugURL=f'[https://tools.wmflabs.org/wikidata-todo/duplicity.php?wiki={lngwiki}&norand=1&page=' + urllib.parse.urlencode(params)[4:] + ' klik]'

    if (searchresult!=None):
      if sameImage:
        TBPtxt='\'\'\'Image\'\'\''
        sameImage=False
      counter+=1
      if (counter>maxpages): break
      wikitxt+=f'|-\n| {counter} || [[{page.title()}]] || {sugURL} || {TBPtxt} || {searchresult} || {page.latest_revision.timestamp}||{cattxt}\n'
endtime=datetime.now()
wikitxt+=footer+f'\n{starttime} – {endtime} '
print(wikitxt)
if (testpage==''):
  pywikibot.Page(site,targetpage).put(wikitxt,f'summary={maxpages} last newest pages still missing wikidata')
