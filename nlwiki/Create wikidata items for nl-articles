#2020-07-17 11:09
"""
todo
2) avoid brackets in label, move bracket text to description
3) get birthdate etc from infobox
6) start parameters (language, generator: newpages/category/etc)
7) recognise sportseasons
8) recognise uitvoerend artist P175
9) show when no cats have suggestive properties

flowchart on https://drive.google.com/file/d/1xJdGvp4FrLLJj8e3-GILIkF5eZf8obkH/view?usp=sharing
"""
import pywikibot
from pywikibot import pagegenerators as pg
import datetime
import time
from pywikibot.data import api
import sys, getopt
import json
import requests
import urllib

language='nl'
checklabels=['en','de','fr','nl','es','pt','dk','se','ru']
metaclass='Q19361238'
max_new_pages=99525
hours=1
allowed_namespaces = [0]
professionconvert={'Q30185':'Q82955', 'Q4657217':'Q82955'}
countryconvert={'Q55':'Q29999'}
throttleBIG=9000
throttleONE=90
throttleDISAMB=4499
person='Q5'
p31convert={'Q5':person,'Q19660746':person,'Q215627':person,'Q30905655':person}
canbeP31=[person,'Q19660746','Q215627','Q30905655','Q16521','','','','','','','','','','','','','','','','',
'','','','','','','','','','','','','','','','','','']
canbeP17=['Q515','Q16970','Q847017','Q13406463','Q12280','Q123705','Q4167410','Q15383322','Q618779','Q194356','Q1286517','Q23442','Q39715','Q27020041','Q178844','Q860861','Q12039431','Q15991790','Q28147344','Q476028','Q21850100']
canbeP495=['Q11424','Q17329259','Q1580166','Q5398426','Q215380','Q571','Q3305213','Q5185279','Q15416','Q191067','Q7889','Q47461344','Q134556','Q7725634','Q482994','Q20667187','Q506240','Q11032','Q1144661','Q1983062','Q1785271',
'Q2743','Q4830453','Q8436','Q41298','Q7302866','Q3240003','Q2831984','','','','','','','']
canbeP1001=['','']
neglect=['Q3957','Q3624078']
sexe={'Q6581097':'male','Q6581072':'female'}
istaxon=['Q16521','Q28319','Q164280']
labellng=['nl','de','fr','en','pt','es','it','da','se','pl','hr','cs','sk','eo','ro','fy','nn','no']
updatelabelfor=[person,'Q4830453','Q6881511']
sportset=['Q31629','Q349']
months=['Q108','Q109','Q110','Q118','Q119','Q120','Q121','Q122','Q123','Q124','Q125','Q126',]
birthdate_infobox={'nl':'geboortedatum','en':'birth_date','de':'Geburtsdatum'}
monthnamecache=[]
commit=True
printcat=False
maxdeepcat=5
maycreate=True

class Property:
    def __init__(self):
      self.P=None
      self.cat=None
      self.level=9999


class wdSuggest:


  def __init__(self):
    self.wd=None
    self.pagename=None
    self.isa=Property()
    self.sexe=Property()
    self.profession=Property()
    self.adminEntity=Property()
    self.sport=Property()
    self.country=Property()
    self.memberofpolitics=Property()
    self.tijdstip=Property()
    self.performer=Property()
    self.jurisdiction=Property()
    self.searchresult=None
    self.value=0
    self.prospect=None
    self.topcat=None
    self.created=False
    self.attached=False
    self.propertieswritten=0

  def getWD(self):
    try:
      self.wd=pywikibot.ItemPage.fromPage(page)
      self.wd.get(get_redirect=True)
      self.printitem(extratxt='already has wd-item')
    except:
      pass


  def suggestPage(self,page,create=True,addproperties=True):
    ns=page.namespace().id
    try:
       self.getWD()
    except():
      if (not maycreate):
        print(f'skip {page.title()}, will not create')
        return
    if (ns==14): #category
      self.addOneProperty('P31','Q4167836',summary='namespace says it is a category',onlyaddnew=True)  
    elif (ns==10): #template
      self.addOneProperty('P31','Q11266439',summary='namespace says it is a template',onlyaddnew=True)    
    elif (ns==828): #module
      self.addOneProperty('P31','Q15184295',summary='namespace says it is a module',onlyaddnew=True)  
    elif (ns==0): #regular page
      if len(page.text)>9: 
        if page.text[0:9].lower()=='#redirect': return
      if len(page.text)>15: 
        if page.text[0:15].lower()=='#doorverwijzing': return
      print(f'Page: {page.title()}')
      self=wdSuggest()  
      self.pagename=page.title()
      self.aggregateProperties(page)
      try:
        #self.wd=page.data_item();
        self.getWD()
        if addproperties: 
          if (self.addProperties()>0):
            print('properties added')
      except:
        self.wd=None
        self.printitem(extratxt='no wd-item yet')
        if 'disambiguation' in page.properties():
          print('Search 4 disambiguation')
          self.findExisting(page.title(),disamb=True)
          if self.isa.P==None:
            self.isa.P='Q4167410'
            self.isa.cat=None
            self.isa.level=9999
        else:
          self.findExisting(page.title())
        if (self.searchresult==None) and create:
          self.newItem(page.title())
        else:
          self.evaluateResults(addproperties=addproperties)

  def allpropertiesfilled(self):
    if (self.topcat):
      if (printcat): print('All the way!')
      return(True)
    if (self.isa.P and self.sexe.P and self.profession.P and self.adminEntity.P and self.memberofpolitics.P and self.sport.P and self.country.P and self.sport):
      if (printcat): print('Fully filled')
      return(True)
    return(False)  


  def walksubcats(self,cat,level=1,usedcats=[]):
    def checkcat(str):
      start=str.find(':')
      if start>0:
        return(str[start+1:].find(':')<0)
      return(False)
      
    if (checkcat(cat.title())) and (level<maxdeepcat):
      self.findfromcat(cat,True,level)
      usedcats.append(cat.title())
      for x in cat.categories():
        if (printcat): print(f'subc: {x.title()}*-*level={level}')
        if not(x.title() in usedcats) and (checkcat(x.title())):
          self.walksubcats(x,level=level+1,usedcats=usedcats)
    #print(f'Now level: {level} - {usedcats}')

  def aggregateProperties(self,page):
    apcats=[]
    if (printcat): print('xxx')
    for cat in page.categories():
      if (printcat): print(f'page: {cat.title()}')
      self.findfromcat(cat,False,0)
    #while not(self.allpropertiesfilled()):
    if (printcat): print('Not found yet')
    for cat in page.categories():
      if printcat: print(f'redo: {cat.title()}')
      self.walksubcats(cat,level=1,usedcats=apcats)
      if (self.allpropertiesfilled()): 
        if (printcat): print('Fullfilled')
        break
    #self.topcat=True
    if (printcat): print(f'Used cats: {apcats}')

  def compareProperty(self,wdx,P,factor):
   if (not(P in wdx.claims)):
     return(1.0)
   if (self.wd!=None): 
    if (P in self.wd.claims) and (P in wdx.claims):
      for c in self.wd.claims[P]:
        for cc in wdx.claims[P]:
           if c.getTarget()==cc.getTarget():
             return(5*factor) #full hit
      return factor #hmmm
    return(0.1*factor) #unlikely
   else:
    for cc in wdx.claims[P]:
      cct=cc.getTarget().title()
      if P=='P31':
        if self.isa.P==cct:
          if (self.isa.P in istaxon):
            return(throttleBIG+1)
          else:  
            return(5*factor)
      if P=='P641':
        if (self.sport.P==cct):
          return(5*factor)
      if P=='P102':
        if (self.memberofpolitics.P==cct):
          return(5*factor)
      if (P=='P21'):
        if (self.sexe.P==cct):
          return(2*factor)
        else:
          return(factor)
      if (P=='P17'):
        if (self.country.P==cct):
          return(5*factor)
      if (P=='P27'):
        if (self.country.P==cct):
          return(5*factor)
      if P=='P106':  
        if (self.profession.P==cct):
          return(5*factor)
   return(0.1*factor)  

  def Compare(self,wdx):
    uselabel=''
    if (language in wdx.labels):
      uselabel=wdx.labels[language]
    else:
       for tlang in checklabels:
         if tlang in wdx.labels:
           if (uselabel=='') or (uselabel!=self.pagename):
             uselabel=wdx.labels[tlang]
             #print('use: ',tlang)
    if (uselabel==self.pagename):
      cval=100
    else: 
      cval=1
      #print(uselabel,language,cval,self.pagename)
    cval=cval*self.compareProperty(wdx,'P31',9.0)
    cval=cval*self.compareProperty(wdx,'P106',5.0)
    cval=cval*self.compareProperty(wdx,'P27',4.0)
    cval=cval*self.compareProperty(wdx,'P102',2.0)
    cval=cval*self.compareProperty(wdx,'P641',2.0)
    cval=cval*self.compareProperty(wdx,'P21',2.0)
    return cval

  def evaluateResults(self,addproperties=True):
    for xresult in self.searchresult:
      wdx=pywikibot.ItemPage(repo,xresult)
      wdx.get(get_redirect=True)
      value=self.Compare(wdx)
      print(f'--{value}-{xresult}')  
      if (((value>throttleBIG) and (len(self.searchresult)>1)) or ((value>throttleONE) and (len(self.searchresult)==1)))  and (value>self.value) or ((self.isa.P=='Q4167410') and (value>throttleDISAMB)):
        self.value=value
        self.prospect=xresult
    if (self.prospect!=None):
       print(f'Use {self.prospect}')
       self.attachPage(self.pagename)
       if addproperties: 
         self.addProperties()

  def setLabels(self,pagename,src=''):
    label=pagename #later strip ()
    pos=label.find('(')
    if pos>2:
      label=label[:pos-1]
    if ((not(language in labellng)) or (not(self.isa.P in updatelabelfor))):
      self.wd.editLabels({language:label})  #exceptional language not using Latin script, add separately to enforce a label, or label not suitable for multi-language update
    else:
      lbldata={'labels':{}}
      for lng in labellng:
        if (not(lng in self.wd.labels)):
          lbldata['labels'].update({lng:label})
      if lbldata['labels']!={}:
        self.wd.editEntity(lbldata,summary=f'set multiple labels {src}')

  def attachPage(self,pagename):
    if (self.wd==None):
      try:
        self.wd=pywikibot.ItemPage(repo,self.prospect)
        self.wd.get(get_redirect=True)
        self.setLabels(pagename,src='x1')
      except:
        pass
    #print('Now set sitelink!')
    if (not(language+'wiki') in self.wd.sitelinks):
      self.wd.setSitelink(sitelink={'site':language+'wiki','title':pagename},summary='set link')
      self.attached=True
      self.setLabels(pagename,src='x2')  #xxx

  def hasPropertiesFilled(self):
    return((self.isa.P!=None) or (self.sexe.P!=None) or (self.profession.P!=None) or (self.country.P!=None) or (self.memberofpolitics.P!=None) or (self.adminEntity.P!=None) or (self.sport.P!=None) or (self.tijdstip.P!=None))

  def printitem(self,extratxt=''):
   #print(f'Item: {extratxt}')
   if (True):
    if self.isa.P != None:            print(f'Is een..: {self.isa.P}')
    if self.sexe.P!=None:             print(f'Sexe....: {sexe[self.sexe.P]}')
    if self.profession.P!=None:       print(f'Beroep..: {self.profession.P}')
    if self.sport.P!=None:            print(f'Sport...: {self.sport.P}')
    if self.adminEntity.P!=None:      print(f'Gemeente: {self.adminEntity.P}')
    if self.country.P!=None:          print(f'Land....: {self.country.P}')
    if self.memberofpolitics.P!=None: print(f'Partij..: {self.memberofpolitics.P}')
    if self.searchresult!=None:       print(f'Kan.....: {self.searchresult}')

  def checkTopic(self,wdt,prop,target,sourcecat,catlevel):
        #print(f'prop: {prop}-cat: {sourcecat}')
        if (prop in wdt.claims):
         #print(f'{prop} found')   
         for isaclaim in wdt.claims[prop]:
          xt=isaclaim.getTarget()
          if (xt):
           isa=xt.title()
           if isa in ['Q6256']: 
             if (target in countryconvert) and (self.isPerson()) and ((self.country.P==None) or (catlevel<self.country.level)):
               self.country.P=countryconvert[target]
             else:
               self.country.P=target
             self.country.cat=sourcecat
             self.country.level=catlevel
           if ((target in canbeP31) or (target in canbeP17) or (target in canbeP495) or (target in canbeP1001)) and ((self.isa.P==None) or (catlevel<self.isa.level)):  
             if target in p31convert: 
               self.isa.P=p31convert[target]
             else:
               self.isa.P=target
             self.isa.cat=sourcecat
             self.isa.level=catlevel
           if (isa in ['Q515']) and ((self.adminEntity.P==None) or (catlevel<self.adminEntity.level)):
             self.adminEntity.P=target
             self.adminEntity.cat=sourcecat
             self.adminEntity.level=catlevel
           if (isa in ['Q28640']) and ((self.profession.P==None) or (catlevel<self.profession.level)): 
             self.profession.cat=sourcecat
             if target in professionconvert:
               self.profession.P=professionconvert[target]  
             else:    
               self.profession.P=target
             self.profession.level=catlevel  
           if (isa in ['Q7278']) and ((self.memberofpolitics.P==None) or (catlevel<self.memberofpolitics.level)):
             self.memberofpolitics.P=target
             self.memberofpolitics.cat=sourcecat
             self.memberofpolitics.level=catlevel
           if (isa in ['Q3186692']) and (self.tijdstip.P==None):
             try:
               wbt=pywikibot.ItemPage(repo,target)
               wbt.get(get_redirect=True)
               if ('P585') in wbt.claims:
                 self.tijdstip.P=wbt.claims['P585'].getTarget()
             except:
               pass
             self.tijdstip.cat=sourcecat
             self.tijdstip.level=catlevel
           if (target in sexe) and (self.sexe.P==None):
             self.sexe.P=target
             self.sexe.cat=sourcecat
           if (isa in sportset) and (catlevel<self.sport.level):
             self.sport.P=target
             self.sport.cat=sourcecat
             self.sport.level=catlevel

  def findExisting(self,search_for,disamb=False): #find suspects to connect page to, based on name
    def getItems(site, itemtitle):
     params = { 'action' :'wbsearchentities' , 'format' : 'json' , 'language' : 'en', 'type' : 'item', 'search': itemtitle}
     request = api.Request(site=site,parameters=params)
     return request.submit()

    ssite = pywikibot.Site("wikidata", "wikidata")
    srepo = site.data_repository()
    if (disamb):
      searchresult = getItems(ssite, search_for + ' disambiguation')
    else:
      searchresult = getItems(ssite, search_for)
    result=[]
    for item in searchresult['search']:
       itemID=item['id']
       wd=pywikibot.ItemPage(srepo,item['id'])
       wd.get(get_redirect=True)
       result.append(wd.title())
    if (result==[]) or (self.wd!=None):
      self.searchresult=None  
    else:
      self.searchresult=result

  def newItem(self,title): #create a new item, set label-link-properties
    #print('Might create')
    if (self.searchresult==None) and (self.hasPropertiesFilled()):
      print('Will create')  
      self.wd=repo.editEntity({},{},summary='#cwifna')
      self.wd=pywikibot.ItemPage(repo,self.wd['entity']['id'])
      self.wd.get()
      self.attachPage(title)
      self.created=True
      return self.addProperties()

  def isPerson(self):
    if self.wd!=None:
       if 'P31' in self.wd.claims:
         for x in self.wd.claims['P31']:
            if x!=None:
              if x.getTarget()==person: return(True)
    return(self.isa.P==person)


  def addOneProperty(self,P,V,summary='add claim',onlyaddnew=True):
    #print(f'Add {V} to {P}')
    if not self.wd:
      print('Can not add property to no wd-item!')
      return(0)
    if (P=='P17') and (not(self.isa.P in canbeP17)):
      if (not(self.isa.P in canbeP495)) and (self.isa.P):
        print(f'No P17 for {self.isa.P}')
      return(0)
    if (P=='P495') and (not(self.isa.P in canbeP495)): 
      if (not(self.isa.P in canbeP17)) and (self.isa.P): 
        print(f'No P495 for {self.isa.P}')
      return(0)
    if (P=='P1001') and (not(self.isa.P in canbeP1001)):
      if (not(self.isa.P in canbeP1001)) and (self.isa.P):
        print(f'No P1001 for {self.isa.P}')
      return(0)
    if (not((P in self.wd.claims) and onlyaddnew)) and (V!=None) and (not(V in neglect)):
      claim=pywikibot.Claim(repo,P)
      target=pywikibot.ItemPage(repo,V)
      claim.setTarget(target)
      if commit: self.wd.addClaim(claim,summary=summary)
      return(1)
    return(0)  

  def addProperties(self): #add properties to the wd-item
    added=0
    #print('Try to add properties')
    if self.wd==None: return
    #print('Will add properties')
    if (self.isPerson()):
      #print('It is a person')
      added+=self.addOneProperty('P106',self.profession.P,summary=f'P106 from categorie {self.profession.cat}')
      if self.country.P in countryconvert: self.country.P=countryconvert[self.country.P]
      added+=self.addOneProperty('P27',self.country.P,f'country from categorie {self.country.cat}')
      added+=self.addOneProperty('P102',self.memberofpolitics.P,summary=f'add membership of political party from categorie {self.memberofpolitics.cat}')
      added+=self.addOneProperty('P21',self.sexe.P,summary=f'P21 from categorie {self.sexe.cat}')
    else:
      #print('It is not a person')
      added+=self.addOneProperty('P131',self.adminEntity.P,summary=f'add location from category {self.adminEntity.cat}')
      added+=self.addOneProperty('P17',self.country.P,f'country from categorie {self.country.cat}')
      added+=self.addOneProperty('P495',self.country.P,f'country of origin from categorie {self.country.cat}')
      added+=self.addOneProperty('P641',self.sport.P,summary=f'add sport from category {self.sport.cat}')
      added+=self.addOneProperty('P585',self.tijdstip.P,summary=f'add point in time from {self.tijdstip.cat}')
      added+=self.addOneProperty('P1001',self.jurisdiction.P,summary=f'add jurisdiction from {self.jurisdiction.cat}')
    added+=self.addOneProperty('P31',self.isa.P,summary=f'P31 from categorie {self.isa.cat}')
    
    self.profession.P=None  
    self.country.P=None
    self.adminEntity.P=None
    self.memberofpolitics.P=None
    self.tijdstip.P=None
    self.isa.P=None
    self.sexe.P=None
    self.propertieswritten+=added
    return added

  def findfromcat(self,cat,showmissing,level): #loop through categories, derives properties from wd-item from cat
     #print(f'--{cat.title()}')
     if 'wikibase_item' in cat.properties():    
       wdc=cat.data_item()
       wdc.get(get_redirect=True)
       #print(wdc.title())
       for cl in ['P301','P971']:
        if cl in wdc.claims:
         for topic in wdc.claims[cl]:
           if topic.getTarget()!=None: 
             target=topic.getTarget().title()
             wdt=pywikibot.ItemPage(repo,target)
             wdt.get(get_redirect=True)
             self.checkTopic(wdt,'P31',target,wdc.title(),level)
             self.checkTopic(wdt,'P279',target,wdc.title(),level)
       else:
         pass
         #if (showmissing): print(f'Missing P971 on category: {wdc.title()}')

def get_one_line(text):
    one_line=''
    for x in text:
      one_line=one_line+x
      if (x=='\n'):
        yield one_line
        one_line=''

def input_from_etherpad():
  inputname='https://etherpad.wikimedia.org/p/pythonfeeder/export/txt'
  httpread=urllib.request.urlopen(inputname)
  contents=httpread.read().decode("utf-8")
  for item in get_one_line(contents):
    yield(item) 

def getnewpages(site):
  for page in pg.NewpagesPageGenerator(site,0,max_new_pages):
   if (page.exists()): #avoid speedy deleted pages
    dt=page.oldest_revision
    timediff=dt.timestamp.today()-dt.timestamp  
    if (timediff<datetime.timedelta(hours/24)): #page less 3 hours old (script runs every 3 hrs)
      if (page.namespace().id in allowed_namespaces):
        if page.exists():
          yield(page)
    else: 
      break

def check_cat(thiscat):
   cat=pywikibot.Category(site,thiscat)     
   gen=pg.CategorizedPageGenerator(cat,99,start=None,total=None,namespaces=None,)
   for page in gen:
      if (page.namespace()==0):
        yield(page)

def getnewpageswithoutwd(site):
    for page in getnewpages(site):
      if (page.namespace().id in allowed_namespaces):
        if (page.exists()): #avoid speedy deleted pages
          dt=page.oldest_revision
          timediff=dt.timestamp.today()-dt.timestamp  
          if (timediff<datetime.timedelta(hours/24)): 
            if ('wikibase_item' in page.properties()):
              pass  
              #print(f'passed {page.title()}')
            else:   
              yield(page)

def all_links_from(page):
    for x in page.linkedPages():
     if (x.exists()):   
      print(x.title())
      wds=wdSuggest()
      wds.wd=pywikibot.ItemPage(pywikibot.Site('wikidata','wikidata').data_repository(),x.title())
      wds.wd.get(get_redirect=True)
      if (language+'wiki' in wds.wd.sitelinks):
        page=pywikibot.Page(site,wds.wd.sitelinks[language+'wiki'])
        wds.suggestPage(page)  
        
site=pywikibot.Site(language,'wikipedia')
repo=site.data_repository()

def PagePyleGenerator(pile):
 api_token = '?id=%s&action=get_data&format=json&doit'
 api_url_base = 'https://tools.wmflabs.org/pagepile/api.php'

 url=api_url_base+api_token%pile
 data = requests.get(url)
 #print(dir(data))
 pile_lng  =json.loads(data.text)['language'] #language
 pile_prj  =json.loads(data.text)['project']  #project
 pile_items=json.loads(data.text)['pages_returned'] #nr of items
 pile_total=json.loads(data.text)['pages_total'] #pages_total

 plsite=pywikibot.Site(pile_lng,pile_prj)
 plrepo=plsite.data_repository()   
 
 pyle=(json.loads(data.text)['pages'])
 for oneitem in pyle:
    if (pile_lng=='wikidata'):
      plwd=pywikibot.ItemPage(plrepo,oneitem)
      plwd.get(get_redirect=True)  
      yield(plwd)
    else:
      plpage=pywikibot.Page(plsite,oneitem)
      yield(plpage)

def pageIDgenerator():
  pageids=[

   ]
  for x in pageids:
     yield x



""" #one category/pagepile/newpages
if (True):
 language='nl'
 pagesdone=0
 site=pywikibot.Site(language,'wikipedia')
 gen=check_cat('Nederlandse korfbalcompetitie')
 #site=pywikibot.Site('wikidata','wikidata')
 gen=PagePyleGenerator('30447') #wd-soccer players
 #gen=getnewpageswithoutwd(site)
 #gen=getnewpages(site)
 for page in gen:
   wds=wdSuggest()
   wds.suggestPage(page)
   if (wds.propertieswritten>0) or (wds.created) or (wds.attached): 
     pagesdone+=1
   if pagesdone>1: break
    
""" #one category


""" #pageID
if (True):
 site=pywikibot.Site('nl','wikipedia')
 #print('OK')
 for page in pg.PagesFromPageidGenerator(pageIDgenerator(),site=site):
  #print(page)
  wds=wdSuggest()
  wds.suggestPage(page)   
""" #pageID


""" #one single page
site=pywikibot.Site('nl','wikipedia')
page=pywikibot.Page(site,'Grendel Games')
wds=wdSuggest()
wds.suggestPage(page)
""" #one single page


""" #all without claims
page=pywikibot.Page(pywikibot.Site('wikidata','wikidata'),'Wikidata:Database reports/without claims by site/nlwiki')
all_links_from(page)
""" #all without claims


#"""#small handmade list
def handmade_list():
 site=pywikibot.Site('nl','wikipedia')
 for x in [ 
 ]:
   if (x!=''):
     wds=wdSuggest()
     page=pywikibot.Page(site,x)  
     #print(f'Will suggest {x}')   
     wds.suggestPage(page)   
#""" #small handmade list

def main(argv):
  try:
    opts,args = getopt.getopt(argv,'gvhcl',['gen','verbose','help','cat','lang','etherpad'])
    print(opts)
    print('-------')
    print(args)
    gen=None
    if (len(args)>=3) or True:
      param1=sys.argv[1].lower()
      if param1=='etherpad': 
        maycreate=False
        gen=input_from_etherpad()
        print('Input from etherpad!')
      if len(args)>1: 
        param2=sys.argv[2].lower()
      else:
        param2=None
      print(param1)
      print(param2)
      if not gen: gen=handmade_list()
      for item in gen:
        if (item) and (item!=''):
          print(item.title())
          wds=wdSuggest()
          try:
            page=pywikibot.Page(site,item)
            wds.suggestPage(page)
          except:
            pass
  except getopt.GetoptError as err:
    print(f'xxx: {err}')
  


if __name__ == "__main__":
  print('Start')
  main(sys.argv[1:])
  print('Klaar')
else:
  print('Niks')  
