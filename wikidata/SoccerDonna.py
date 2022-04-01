#20210301 09:24   SELECT ?item ?sd WHERE { ?item wdt:P4381 ?sd } order by ?sd
import pywikibot
import requests
from pywikibot import pagegenerators as pg
from pywikibot.data import api
from datetime import datetime
import csv


skiptxt=' <\n\r\t'
imgtxt='<img src='
imgend='/>'
Pmentioned='P248'
QsoccerDonna='Q41779610'

playerstart=54200
playerstop=56707
lng='nl'
prndebug=False

soccerProfession={'Q937857'}
soccerSports=[{'Q2736':1},{'Q606060':2}]

countryCONV={'England':'Q21','Norwegen':'Q20','Deutschland':'Q183','Schweden':'Q34','Ungarn':'Q28',
             'Niederlande':'Q29999','Färöer':'Q4628','Bosnien-Herzegowina':'Q225','Spanien':'Q29','Malta':'Q233',
             'Schottland':'Q22','Italien':'Q38','Portugal':'Q45','Tschechien':'Q213','Lettland':'Q211',
             'Belgien' : 'Q31','Frankreich' : 'Q142', 'Litauen' : 'Q37','Österreich':'Q40','Rumänien':'Q218',
             'Montenegro':'Q236','Kosovo':'Q1246','Dänemark':'Q35','Finnland' : 'Q33','Kroatien' : 'Q224','Griechenland':'Q41',
             'Luxemburg':'Q32','Türkei':'Q43','Liechtenstein':'Q347','Nordirland':'Q26','San Marino':'Q238',
             
             'Vereinigte Staaten':'Q30','Kanada':'Q16','Costa Rica':'Q800',
             'Jamaika':'Q766','El Salvador':'Q792',
             'Peru':'Q419', 'Uruguay':'Q77', 'Venezuela':'Q717','Argentinien':'Q414',
             
             'Australien':'Q408',
             'Dominica':'Q784','Singapur':'Q334','Chinese Taipei (Taiwan)':'Q865',
             
             'Ghana':'Q117','Nigeria':'Q1033','Kamerun':'Q1009','Sambia':'Q953',
             'Mexiko':'Q96','Kenia':'Q114','Kongo DR':'Q974','Tansania':'Q924',

             'Russland':'Q159','China':'Q148','Südkorea' : 'Q884','Afghanistan':'Q889','Usbekistan':'Q265',
             
             'Neukaledonien':'Q33788','Nordmazedonien':'Q221','Elfenbeinküste':'Q1008','Philippinen':'Q928','Weißrussland':'Q184',
             'Mauritius':'Q1027','Libanon':'Q822','Simbabwe':'Q954','Albanien':'Q222','Martinique':'Q17054','Syrien':'Q858',
             'Georgien':'Q230','Suriname':'Q730','Namibia':'Q1030','Slowenien':'Q215','Guinea-Bissau':'Q1007','Uganda':'Q1036',
             'Puerto Rico':'Q1183','Burkina Faso':'Q965','Tunesien':'Q948','Haiti':'Q790','Tadschikistan':'Q863','Hongkong':'Q8646',
             
             'Armenien':'Q399','Bangladesch':'Q902','Malaysia':'Q833','Vietnam':'Q881','Gambia':'Q1005','Kirgisistan':'Q813','Mali':'Q912','Angola':'Q916',         

'Indonesien':'Q252','Irak':'Q796','Liberia':'Q1014','Ägypten':'Q79','Aruba':'Q21203','Senegal':'Q1041',
'Indien':'Q668','Osttimor':'Q574','Samoa':'Q683','Kongo':'Q971','Bulgarien':'Q219','Südafrika':'Q258',
'Cayman-Inseln':'Q5785','Guam':'Q16635','Jordanien':'Q810','Guinea':'Q1006','Sierra Leone':'Q1044',
'Barbados':'Q244','Jugoslawien (Bundesrepublik)':'Q838261','Serbien und Montenegro':'Q37024','Réunion':'Q17070','Gabun':'Q1000',
'Nördliche Marianen':'Q16644','Oman':'Q842','Burundi':'Q967','Amerikanische Jungferninseln':'Q11703','Äthiopien':'Q115',
'Grenada':'Q769','Iran':'Q794','St. Kitts und Nevis':'Q204989','Madagaskar':'Q1019',
'Cookinseln':'Q26988','Tahiti':'Q42000','Papua Neu-Guinea':'Q691','Kap Verde':'Q1011',
'Bermuda':'Q23635','Myanmar':'Q836','Pakistan':'Q843','St. Lucia':'Q760',
'Nepal':'Q837','Ruanda':'Q1037','Mosambik':'Q1029','Curacao':'Q25279', 'Nordkorea':'Q423','Ukraine':'Q212',
             'Äquatorialguinea':'Q983','Paraguay':'Q733','Brasilien':'Q155','Wales':'Q25','Bolivien':'Q750', 'Chile':'Q298', 
             'Argentina':'Q414', 'Polen':'Q36','Kolumbien':'Q739','Costa Rica':'Q800',
             'Irland' : 'Q27','Kuba':'Q241','Dominikanische Republik':'Q786','Moldawien':'Q217',
             'Neuseeland' : 'Q664', 
             'Aserbaidschan':'Q227','Ecuador':'Q736',  'Zypern':'Q229','Kasachstan':'Q232','Nordkorea ':'Q423',
             'Thailand':'Q869','Israel':'Q801','Japan':'Q17','Malawi':'Q1020','Andorra':'Q228',
             'Guatemala':'Q774', 'Honduras':'Q783', 'Mexico':'Q96',  'Nicaragua':'Q811', 'Guyana':'Q734','Estland' : 'Q191',  
             'Panama':'Q804','Schweiz':'Q39','Island' :'Q189','Guadeloupe':'Q17012',
             'Algerien':'Q262','Marokko':'Q1028','Slowakei':'Q214','Serbien':'Q403','Trinidad und Tobago':'Q754',
            }

positionCONV={ #https://www.wikidata.org/w/index.php?title=Special%3AWhatLinksHere&target=Q4611891&namespace=0
              'Torwart':'Q201330',
    'Torwart - Defensiv-Allrounder':'Q201330',
'Torwart - Allrounder':'Q201330',
'Torwart - defensives Mittelfeld':'Q201330',
'Torwart - zentrales Mittelfeld':'Q201330',
'Torwart - Mittelstürmer':'Q201330',
'Torwart - Offensiv-Allrounder':'Q201330',

              'Abwehr - rechter Verteidiger':'Q5508224',
              'Abwehr - linker Verteidiger':'Q5508224',
              'Abwehr':'Q336286',
              'Abwehr - Innenverteidigung':'Q336286', 
              'Abwehr - Allrounder':'Q268258',
              'Abwehr - Defensiv-Allrounder':'Q268258',
              'Abwehr - Außenbahn links':'Q5508224',
              'Abwehr - Außenbahn rechts':'Q5508224',
              'Abwehr - Außenbahn (links & rechts)':'Q5508224',
              'Abwehr - linkes Mittelfeld':'Q5508224',
              'Abwehr - defensives Mittelfeld':'Q336286',
'Abwehr - zentrales Mittelfeld':'Q336286',
'Abwehr - Libero':'Q336286',
'Abwehr - Offensiv-Allrounder':'Q336286',
'Abwehr - Manndecker':'Q336286',
'Abwehr - offensives Mittelfeld':'Q336286',
'Abwehr - Mittelstürmer':'Q336286',
'Abwehr - linker Außenstürmer':'Q5508224',
'Abwehr - rechtes Mittelfeld':'Q5508224',
'Abwehr - linkes off. Mittelfeld':'Q5508224',
'Abwehr - rechtes off. Mittelfeld':'Q5508224',
'Abwehr - linkes def. Mittelfeld':'Q5508224',
              'Mittelfeld - Allrounder':'Q6008848',
              'Mittelfeld - Außenbahn links':'Q8025128',
              'Mittelfeld - Außenbahn rechts':'Q8025128',
              'Mittelfeld - rechtes Außenstürmer':'Q6008848',
              'Mittelfeld - rechtes Mittelfeld':'Q8025128',
              'Mittelfeld - linkes Mittelfeld':'Q8025128',
              'Mittelfeld - defensives Mittelfeld':'Q18691898',
              'Mittelfeld - offensives Mittelfeld':'Q193592',
              'Mittelfeld - Offensiv-Allrounder':'Q16501245',
              'Mittelfeld - zentrales Mittelfeld':'Q193592',
              'Mittelfeld - rechter Verteidiger':'Q18691898',
              'Mittelfeld - Innenverteidigung':'Q6008848',
              'Mittelfeld':'Q193592',
              'Mittelfeld - Außenbahn (links & rechts)':'Q2827965',
'Mittelfeld - rechtes off. Mittelfeld':'Q8025128',
'Mittelfeld - Außenstürmer':'Q6008848',
'Mittelfeld - Defensiv-Allrounder':'Q6008848',
'Mittelfeld - Mittelstürmer':'Q6008848',
'Mittelfeld - rechter Außenstürmer':'Q8025128',
'Mittelfeld - rechtes def. Mittelfeld':'Q8025128',
'Mittelfeld - linkes def. Mittelfeld':'Q8025128',
'Mittelfeld - linkes off. Mittelfeld':'Q8025128',
'Mittelfeld - Spielmacher':'Q6008848',
'Mittelfeld - linker Verteidiger':'Q8025128',
'Mittelfeld - linker Außenstürmer':'Q8025128',
              'Sturm':'Q280658',
              'Sturm - Allrounder':'Q193592',
              'Sturm - Mittelstürmer':'Q9731197', 
              'Sturm - Außenbahn':'Q2827965',
              'Sturm - Außenbahn links':'Q2827965',
              'Sturm - Außenbahn rechts':'Q2827965',
              'Sturm - zentrales Mittelfeld':'Q280658',
              'Sturm - Offensiv-Allrounder':'Q193592',
              'Sturm - Außenbahn (links & rechts)':'Q280658',
              'Sturm - Außenstürmer':'Q8025128',
'Sturm - Defensiv-Allrounder':'Q9731197',
'Sturm - rechtes off. Mittelfeld':'Q2827965',
'Sturm - rechter Außenstürmer':'Q2827965',
'Sturm - linker Außenstürmer':'Q2827965',
'Sturm - rechtes Mittelfeld':'Q2827965',
'Sturm - offensives Mittelfeld':'Q9731197',
'Sturm - defensives Mittelfeld':'Q9731197',
'Sturm - Innenverteidigung':'Q280658',
'Sturm - linkes Mittelfeld':'Q2827965',
'Sturm - linkes def. Mittelfeld':'Q2827965',
'Sturm - rechter Verteidiger':'Q2827965',
'Sturm - linkes off. Mittelfeld':'Q2827965',
'Sturm - linker Verteidiger':'Q2827965',
'Sturm - Spielmacher':'Q193592',
}

site=pywikibot.Site(lng,'wikipedia')
repo=site.data_repository()

def wd_sparql_query(spq):
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd in generator:
     try:
       wd.get(get_redirect=True)
       yield wd
     except:
       pass

def stripNoise(text):
    i=0
    while (text[i:i+1] in skiptxt) and (i<len(text)):
        i+=1
        if (text[i:i+1] in '<'):
          i=2+i+text[i:].find('>')  
    text=text[i:].strip()    
    i=len(text)
    if (text[i-1:i] in '>'):
       while (not(text[i-1:i] in '<')) and (i>=0):
          i-=1
       i-=2
    text=text[:i]
    i=text.find(imgtxt)
    if (i>-1):
       #print(text) 
       end=i+text[i:].find(imgend) 
       if (end>-1):
            text=text[:i].strip()+','+text[3+end:].strip()
            text=text.replace('<br />','')
            #print(f'{text}-{i}-{end}')
    text=text.replace('\r\n','')
    text=text.replace('\t','')
    return(text)


class soccerPlayer():
  donnaID=None
  name=None
  birthname=None
  nationality=None
  dob=None
  placeofbirth=None
  height=None
  position=None
  footpreference=None
  contractend=None
  wd=None
  text=None
  searchresult=None
    
  def __init__(self,id,online=True):
    try:
      if (online):
        baseURL='https://www.soccerdonna.de/de/demi-derksen/profil/spieler_%d.html'
        #print(1/0)  #leave SoccerDonna alone now we have CSV-file data 
        f = requests.get((baseURL)%(id))
        self.text=f.text 
      else:
        self.text='Intentionally skipped'
        #print('Intentionally skipped')
    except:
      self.text='error reading website'  
    self.wd=None
    if (prndebug): print(f'Initialised self.wd to {self.wd}')
    for player in wd_sparql_query('select ?item where {?item wdt:P4381 \'%s\'}' % id):
        self.wd=player #find existing item with SoccerDonna-id filled
        print('found one...')
    self.donnaID=id
    if (prndebug): print(f'Initialised donna {self.donnaID} - {self.wd}')

  def getSome(self,some):
    start=self.text.find('%s:</td>'%some)
    start2=self.text[start:].find('<td>')
    end=self.text[start+start2:].find('</td>')
    if (end>0) and (start2>0) and (end>0):
      return(stripNoise(self.text[4+start+start2:start+start2+end]))
    else:
      return('')
    
  def getName(self):
    if not self.name:
      start=15+self.text.find('Das Profil von ')
      end=start+self.text[start:].find('</p>')
      if (start>14) and (end>start):
        self.name=self.text[start:end]
    if not self.name:
        return(None)
    if self.name.strip()=='':
        return(None)
    return(self.name)

  def getPosition(self):
    if not self.position:
      self.position=self.getSome('Position')
    if (self.position=='-'): 
      return('')
    else:
      return(self.position)
  def getHeight(self):
    if not self.height:
      self.height=self.getSome('Gr&ouml;sse')
    return(self.height)  
  def getPOB(self):
    if not self.placeofbirth:
      self.placeofbirth=self.getSome('Geburtsort')
    return(self.placeofbirth)
  def getDOB(self):
    if not self.dob:       
      try:  
        datestr=self.getSome('Geburtsdatum')
        if len(datestr)==10:
          self.dob=datetime.strptime(datestr, '%d.%m.%Y')
        elif (len(datestr)==7):
          self.dob=datetime.strptime(datestr, '%m.%Y')  
        elif len(datestr)==4:
          self.dob=datetime.strptime(datestr, '%Y')
      except:  
        self.dob=None
    return(self.dob)
  def getNAT(self):
    if not self.nationality:
      self.nationality=self.getSome('Nationalit&auml;t')
    return(self.nationality)
  def getBirthName(self):
    if not self.birthname:
      self.birthname=self.getSome('Geburtsname')
    return(self.birthname)  
  def getEndContract(self):
    if not self.contractend:
      self.contractend=self.getSome('Vertrag bis')
    return(self.contractend)  
  def getFoot(self):
    if not self.footpreference:
      self.footpreference=self.getSome('Fuß')
    return(self.footpreference)
    
  def print(self):
    print('–––––––––––––––––––––––––––––––––––––––––––––––')
    if (self.wd): print('id.............: [%s]' % self.wd.title())
    print('ID.............: [%s]' % self.donnaID)
    print('Name...........: [%s]' % self.getName())
    print('Birth name.....: [%s]' % self.getBirthName())
    print('Nationaliteit..: [%s]' % self.getNAT())
    print('Date of Birth..: [%s]' % self.getDOB())
    print('Place Of Birth.: [%s]' % self.getPOB())
    print('Height.........: [%s]' % self.getHeight())
    print('Position.......: [%s]' % self.getPosition())
    print('Foot preference: [%s]' % self.getFoot())
    print('Contract end...: [%s]' % self.getEndContract())

  def addName(self,name2add):  
    #print(f'Try to add: {name2add}')
    data={}
    if (name2add=='') or (name2add is None): 
        #print(f'No name 2 add, quit: {name2add}')
        return
    if (lng in self.wd.labels):
        if (name2add==self.wd.labels[lng]):
            #print(f'No need to add, label already set: {name2add}')
            return  #nothing to add, it's already there
    else:
        data={'labels':{lng:name2add}}
        self.wd.labels[lng]=name2add
    aliases=[]
    if (lng in self.wd.aliases):
        if (name2add in self.wd.aliases[lng]):
            #print(f'Alias already there, so quit: {name2add}')
            return #it's in the aliases already
        aliases=self.wd.aliases[lng]  
    #print(f'Old aliases: {aliases}')
    aliases.append(name2add)
    #print(f'New alises: {aliases}')
    data.update({'aliases':{lng:aliases}})
    #print(f'data: {data}')
    self.wd.editEntity(data,summary='#aliasSD from SoccerDonna')
    print(f'Added: {name2add}')
    
  def addHeight(self):
    if not self.wd:
        self.findme()
    if self.wd:    
      if (not 'P2048' in self.wd.claims) and (self.getHeight()):
        print('Add height')
        srcclaim=pywikibot.Claim(repo,Pmentioned,is_reference=True)
        srcclaim.setTarget(pywikibot.ItemPage(repo,QsoccerDonna))
        value2add=float(self.getHeight().replace(',','.'))
        #print(f'Will add {value2add}')
        target=pywikibot.WbQuantity(value2add,pywikibot.ItemPage(repo,'Q11573'),0.001,site=site)
        claim=pywikibot.Claim(repo,'P2048')
        claim.setTarget(target)
        claim.addSources([srcclaim])
        self.wd.addClaim(claim,summary='height from SoccerDonna #heightSD')
        
  def addPosition(self):
    if not self.wd:
        self.findme()
    if self.wd:
      if (not 'P413' in self.wd.claims) and (self.getPosition()):    
        print('Add position')
        if not (self.getPosition() in positionCONV):
            print(f'Add {self.getPosition()} to positionCONV')
            print(124/0)
        claim=pywikibot.Claim(repo,'P413')
        target=pywikibot.ItemPage(repo,positionCONV[self.getPosition()])
        claim.setTarget(target)
        srcclaim=pywikibot.Claim(repo,Pmentioned,is_reference=True)
        srcclaim.setTarget(pywikibot.ItemPage(repo,QsoccerDonna))
        claim.addSources([srcclaim])
        self.wd.addClaim(claim,summary='position from SoccerDonna #positSD')

  def addCountry(self):
    if not self.wd:
        self.findme()
    if self.wd:     
     for cntry in self.getNAT().split(','):
      if (not ('P27' in self.wd.claims) and (cntry)):
        print('Add nationality')
        if not (cntry in countryCONV):
          print(f'Add {cntry} to countryCONV')
          print(123/0)
        claim=pywikibot.Claim(repo,'P27')    
        target=pywikibot.ItemPage(repo,countryCONV[cntry])
        claim.setTarget(target)
        srcclaim=pywikibot.Claim(repo,Pmentioned,is_reference=True)
        srcclaim.setTarget(pywikibot.ItemPage(repo,QsoccerDonna))
        claim.addSources([srcclaim])
        self.wd.addClaim(claim,summary='country from SoccerDonna #cntrSD')
        
  def addBirthDate(self):      
    if not self.wd:
        self.findme()
    if self.wd:
        if (not('P569' in self.wd.claims)) and (self.dob):
            claim=pywikibot.Claim(repo,'P569')
            target=pywikibot.WbTime(self.dob.year,self.dob.month,self.dob.day)
            claim.setTarget(target)
            srcclaim=pywikibot.Claim(repo,Pmentioned,is_reference=True)
            srcclaim.setTarget(pywikibot.ItemPage(repo,QsoccerDonna))
            claim.addSources([srcclaim])
            self.wd.addClaim(claim,summary='add birthdate from SoccerDonna #dobSD')

  def setDonnaID(self):
    if not ('P4381' in self.wd.claims):
      claim=pywikibot.Claim(repo,'P4381')
      claim.setTarget('%s'%self.donnaID)
      srcclaim=pywikibot.Claim(repo,'P6104',is_reference=True)
      srcclaim.setTarget(pywikibot.ItemPage(repo,'Q96324312'))
      claim.addSources([srcclaim])
      self.wd.addClaim(claim,summary='#set_SoccerDonnaID')
    
  def setDefaults(self):
    if (self.wd):
      if (not('P31' in self.wd.claims)):
        claim=pywikibot.Claim(repo,'P31')
        target=pywikibot.ItemPage(repo,'Q5')
        claim.setTarget(target)
        self.wd.addClaim(claim,summary='soccer player must be human')
      if (not('P106' in self.wd.claims)):
        claim=pywikibot.Claim(repo,'P106')
        target=pywikibot.ItemPage(repo,'Q937857')
        claim.setTarget(target)
        self.wd.addClaim(claim,summary='soccer player, profession=association football player')
      if (not('P21' in self.wd.claims)):  
        claim=pywikibot.Claim(repo,'P21')
        target=pywikibot.ItemPage(repo,'Q6581072')
        claim.setTarget(target)
        self.wd.addClaim(claim,summary='soccerdonna, so female')
    
  def labels(self):
    labdesali={}
    if prndebug: print(f'labels....: {self.wd}')
    if (self.wd==None): print('None detected')
    if not self.wd:
        if prndebug: print('findme')
        self.findme()
    if (not self.wd):
      if prndebug: print('will create now')  
      if self.getName():  #only create new item if it has a name  
        if prndebug: print('beast mode on...')    
        #x=5784239/0 #would create new item, not correct yet!!!
        self.wd=repo.editEntity({},{},summary='#newFemaleSoccerPlayer-from-SoccerDonna-profile')
        self.wd=pywikibot.ItemPage(repo,self.wd['entity']['id'])
        self.wd.get()
        self.setDonnaID()
        self.setDefaults()
        self.wd.get()
        if prndebug: print(f'new item created: {self.wd.title()}')
      else:
        pass
        x=542/0  #no name, can not add!
        
    self.addName(self.getName())
    self.addName(self.getBirthName())
    if not (lng in self.wd.labels):
      labdesali.update({'labels':{lng:self.getName()}}) #set label to standard name
    if (labdesali!=''):
      self.wd.editEntity(labdesali,summary='#SoccerDonna')
    
  def update(self):
    if (self.getName()): 
      if prndebug: print('Update...')  
      self.labels()
      self.addCountry()
      self.addPosition()
      self.addHeight()  
      self.addBirthDate()
    
  def findme(self):
    def getItems(site, itemtitle):
       params = { 'action' :'wbsearchentities' , 'format' : 'json' , 'language' : 'en', 'type' : 'item', 'search': itemtitle}
       request = api.Request(site=site,parameters=params)
       return request.submit()

    def oneAcceptable(onewd):
       if prndebug: print('Check if acceptable......') 
       acceptable=0
       if ('P31' in onewd.claims):
         acceptable=acceptable+100
         if onewd.claims.get('P31')[0].getTarget().title()!='Q5':
            print(f'{onewd.title()} is not a human P31!=Q5')
            return False
         acceptable=acceptable+1000 #a human,  
         print(f'human!: {acceptable}')   
       if ('P27' in onewd.claims):
         same_nationality=False
         acceptable=acceptable+100   
         for nationality in onewd.claims.get('P27'):
           for country in self.getNAT().split(','):
             print(f'Check country: {country}')
             if (country not in ['','-']):
              if (nationality.getTarget()):
               same_nationality=same_nationality or (nationality.getTarget().title()==countryCONV[country])
         if (not same_nationality):   
           print(f'{onewd.title()} is from another country: {acceptable}')    
           return False  
         else:
           acceptable+=2000
           print(f'Land=OK: {acceptable}')
       if ('P106' in onewd.claims):
         for beroep in onewd.claims.get('P106'):
           if (beroep.getTarget()):
            if beroep.getTarget().title() in soccerProfession:
               acceptable+=3000 
               print(f'Right profession!: {acceptable}')
       if ('P641' in onewd.claims):
         for sport in onewd.claims.get('P641'):
            if sport.getTarget().title() in soccerSports:
                acceptable+=soccerSports[sport.getTarget().title()]*1000
                print(f'Sport found: {acceptable}')

       if ('P569' in onewd.claims):
         probe_date=onewd.claims.get('P569')[0].getTarget()
         if (probe_date) and self.dob:
          if (probe_date.year==self.dob.year):
            acceptable+=1000
            if probe_date.month==self.dob.month:
                acceptable+=1000
                if probe_date.day==self.dob.day:
                    acceptable+=1000
                    print(f'Exact same birthdate: {acceptable}')
       for labellng in onewd.labels:
         if (onewd.labels[labellng]==self.getName()):
            acceptable+=1000
            print(f'Same name: {acceptable}')
            break
    
       print(f'probability: {acceptable}')  
       return(acceptable>5000)  
        
    print('try to find items')
    ssite = pywikibot.Site("wikidata", "wikidata")
    srepo = site.data_repository()
    searchresult = getItems(ssite, self.getName())
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
    
    print('Some items found...')
    if (self.searchresult):
      for oneresult in self.searchresult:
        print(f'Try {oneresult}')
        onewd=pywikibot.ItemPage(repo,oneresult)
        onewd.get(get_redirect=True)
        if (oneAcceptable(onewd)):
           print(f'{self.getName()} must be {onewd.title()}')                                      
           self.wd=onewd 
           self.setDonnaID()
           return
    #not found, item might be created

  def add2csv(self):
   if (self.donnaID):
    with open('soccerdonna-20210527.csv','a') as donnacsv:
      donna=csv.writer(donnacsv)
      if (self.wd):
        Qid=self.wd.title()
      else:
        Qid=None
      donna.writerow(['%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (Qid,self.donnaID,self.name,self.birthname,self.nationality,self.dob,self.placeofbirth,self.height,self.position,self.footpreference,self.contractend)])
    
    
def processCSV():
    unique=[]  
    with open('soccerdonna-20210527.csv') as donnacsv:
      donnareader=csv.reader(donnacsv,delimiter='|')
      linecounter=0
      for row in donnareader:
        z=0    
        for x in row:
          for y in x.split('|'):
            if (y=='None'): y=None
            z+=1
            if (z==1): 
                donna=soccerPlayer(0,online=False)
                if prndebug: print(f'Here: {donna.wd}')
                #print(f'Try to read {y}')  
                try:
                  if prndebug: print(f'Read donna {y}')  
                  donna.wd=pywikibot.ItemPage(repo,y)  
                  donna.wd.get(get_redirect=True)
                  #print('Read succesfully')  
                except:
                  donna.Qid=None  
                  donna.wd=None
            if (z==2): donna.donnaID=y
            if (z==3): donna.name=y    
            if (z==4): donna.birthname=y    
            if (z==5): donna.nationality=y    
            if (z==6): 
                       if (y!=None) and (y!='') and (y!='None'):
                         donna.dob=datetime.strptime(y, '%Y-%m-%d %H:%M:%S')
                       else:
                         donna.dob=None
            if (z==7): donna.placeofbirth=y    
            if (z==8): 
                       if y=='-':
                         donna.height=None    
                       else:
                         donna.height=y
            if (z==9): donna.position=y    
            if (z==10): donna.footpreference=y    
            if (z==11): donna.contractend=y 
            if (z==12): print(76543/0)  #I want to know about his!
        cntry=donna.getPosition()
        if not (cntry in positionCONV):
            if (cntry!='') and (not (cntry in unique)):
              unique.append(cntry)  
              print(cntry)
        #donna.print()  
        #donna.addCountry()
        donna.update()
        linecounter+=1
        #if linecounter>1125: x=5748390/0

"""
print('Start!')    
#processCSV()
#print('OK!')
"""        

#""" #csv-start
#fill a range into the csv-file
for id in range(playerstart,playerstop): 
    player=soccerPlayer(id)
    print('---[%s]---' % player.getName())
    player.print()
    #player.update()
    player.add2csv()

#"""    #csv-end
"""
id=44184
id=14477 #nicky van den abeele
id=20574 #vita van der linden
id=17925 #toni payne
#id=8410  #iina salmi
id=2732  #sari van veenendaal
id=30744 #lize kop
id=38284 #Jolet Lommen
id=2959  #Emma Delves
id=21205 #
id=32107
id=45356 #Qid=Q88236247 Jaed Vuyfhuis / Vyfhuis
id=317   #Qid=Q186567 Ashleigh Connor

player=soccerPlayer(13339,online=True)
print('---[%s]---' % player.getName())
player.print()
player.update()
"""
"""
query='select ?item where {?item wdt:P4381 ?soccerdonna . optional{?item wdt:P569 ?coc} filter (!bound(?coc))}'    
i=0
for itemid in wd_sparql_query(query):
  i=i+1
  id=int(itemid.claims.get('P4380')[0].getTarget())
  print(f'read in id={id}')  
  player=soccerPlayer(id)
  print('------------------------------------')
  player.print()
  player.update()
  #print(f.text)
  x=(4/(i-110)) 
"""

print('Done!')

