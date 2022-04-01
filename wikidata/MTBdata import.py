import pywikibot
from pywikibot.data import api
import requests
from bs4 import BeautifulSoup


search_for='<a href="https://mtbdata.com/riders/'
searchlink='https://mtbdata.com/riders/'
cyclists = ['Q2066131','Q2309784','Q19799599','Q15117415']
noncyclists=['Q82955','Q937857','Q49757','Q15991218','Q10843263','Q183945','Q10816969','Q1650915','Q33999']
person='Q5'
processedURLs=[]

def findExisting(search_for): #find suspects to connect page to, based on name
  
    def getItems(site, itemtitle):
       params = { 'action' :'wbsearchentities' , 'format' : 'json' , 'language' : 'en', 'type' : 'item', 'search': itemtitle}
       request = api.Request(site=site,parameters=params)
       return request.submit()
    
    ssite = pywikibot.Site("wikidata", "wikidata")
    srepo = ssite.data_repository()
    searchresult = getItems(ssite, search_for)
    result=[]

    for item in searchresult['search']:
       itemID=item['id']
       wd=pywikibot.ItemPage(srepo,item['id'])
       wd.get(get_redirect=True)
       if isPerson(wd):
         if (isCyclist(wd)):  
            if not('P10190' in wd.claims):
               result.append(wd.title())

    if (result==[]):
      searchresult=None  
    else:
      searchresult=result
    return(searchresult)

def isPerson(wd):
    if wd!=None:
       if 'P31' in wd.claims:
         for x in wd.claims['P31']:
            if x!=None:
              if x.getTarget().title()==person: return(True)
    return(False)
    
def isCyclist(wd):
    skiplist=[]
    if wd!=None:
        if 'P106' in wd.claims:
            for x in wd.claims['P106']:
                if x!=None:
                  if (x.getTarget()):  
                    profession=x.getTarget().title()
                    if profession in cyclists: 
                        return(True)
                    else:
                      if (not (profession in (noncyclists))):  
                        skiplist.append(profession)
            #if len(skiplist)>0:
            #    print(skiplist)            
    
def readMTBtxt(filename):
  f=open(filename,'r')
  text=f.read()
  return(text)

def allMTBers(text):
  start=text.find(search_for)
  while start>0:
    text=text[start+len(search_for):]
    i=0
    while text[i]!='\"':
      i+=1
    yield(text[:i])    
    text=text[i:]
    start=text.find(search_for)

def MTBriderName(rider):
  split=rider.find('-')  
  return(rider[split+1:]+' '+rider[:split])
   
def processRider(rider):
    name=MTBriderName(rider)
    sr=findExisting(name)
    if sr:
      if (len(sr)==1):
        print(rider,'\t', name,'\t',sr[0])
        wd=pywikibot.ItemPage(repo,sr[0])
        wd.get(get_redirect=True)
        claim=pywikibot.Claim(repo,'P10190')
        claim.setTarget(rider)
        source=pywikibot.Claim(repo,'P6104',is_reference=True)
        source.setTarget(pywikibot.ItemPage(repo,'Q110280801'))
        claim.addSources([source])
        wd.addClaim(claim,summary='MTBrider id')

def processHTML(mtbText):        
  for rider in allMTBers(mtbText):
    processRider(rider)
  
def processURL(url):
  if url==None: return() #can't be processed, skip
  if (len(url)<20): return() #it can not be a link, or not to mtbdata.com
  if url[:20]!='https://mtbdata.com/': return() #it's a link to another domain
  if url in processedURLs: return()    #url already processed, so skip
  if len(url)>len(searchlink):
    if (url[:len(searchlink)]==searchlink): #it's a riders link
      return()
  print(url)  
  processedURLs.append(url)
  reqs = requests.get(url)
  soup = BeautifulSoup(reqs.text, 'html.parser')
  processHTML(reqs.text)
  urls = []
  for link in soup.find_all('a'):
    processURL(link.get('href'))

    
def processFile(filename):
  #mtbText=readMTBtxt('MTBdata.txt')    
  site=pywikibot.Site('wikidata','wikidata')    
  repo=site.data_repository()
  mtbText=readMTBtxt(filename)      
  processHTML(mtbText)
    
    
print('Start')    
#processURL('https://mtbdata.com/')
site=pywikibot.Site('wikidata','wikidata')    
repo=site.data_repository()
processURL('https://mtbdata.com/ranking/2021/cross-country-olympic/women-elite/2021-12-28')
print('Klaar')        
