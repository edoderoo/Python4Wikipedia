import pywikibot
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date

"""
Things to do:
*fix demonym, to auto-add correct categories
*int\roduce variables, first one to drive clean-up of non-used properties 
*add SparQL lists, alike Lysteria for lists of books/films/etc
*add switches : fill in a value depending on another value : ##switch#P21#Q6581097:voetballer#Q6581072:voetbalspeelster#else:speler##
*fix 'van/de/van de(r)' in a defaultsort
*units dependant on infobox (cm for athlete, nothing for soccer players)
"""

demonymList={
    'Q16':'Canadees','Q17':'Japans',
    'Q20':'Noors','Q21':'Engels','Q22':'Schots','Q25':'Welsh','Q26':'Noord-Iers','Q27':'Iers','Q28':'Hongaars','Q29':'Spaans',
    'Q30':'Amerikaans','Q31':'Belgisch','Q32':'Luxemburgs','Q33':'Fins','Q34':'Zweeds','Q35':'Deens','Q36':'Pools','Q37':'Litouws','Q38':'Italiaans','Q39':'Zwitsers',
    'Q40':'Oostenrijks','Q41':'Grieks','Q43':'Turks','Q45':'Portugees',
    'Q77':'Uruguayaans','Q79':'Egyptisch','Q96':'Mexicaans',
    'Q114':'Keniaans','Q115':'Ethiopisch','Q117':'Ghanees',
    'Q142':'Frans',
    'Q145':'Brits',
    'Q148':'Chinees',
    'Q155':'Braziliaans',
    'Q159':'Russisch',
    'Q183':'Duits','Q184':'Wit-Russisch','Q189':'IJslands',
    'Q191':'Estisch',
    'Q212':'Oekraïens','Q213':'Tsjechisch','Q214':'Slowaaks','Q215':'Sloveens','Q217':'Moldavisch','Q218':'Roemeens','Q219':'Bulgaars',
    'Q221':'Noord-Macedonisch','Q222':'Albanees','Q223':'Groenlands','Q224':'Kroatisch','Q225':'Bosnisch','Q227':'Azerbeidzjaans','Q228':'Andorrees','Q229':'Cypriotisch',
    'Q241':'Cubaans','Q242':'Belizaans',
    'Q252':'Indonesisch','Q258':'Zuid-Afrikaans',
    'Q398':'Bahreins','Q399':'Armeens',
    'Q408':'Australisch','Q414':'Argentijns',
    'Q664':'Nieuw-Zeelands',
    'Q730':'Surinaams','Q739':'Colombiaans','Q766':'Jamaicaans','Q778':'Bahamaans','Q781':'Antiguees','Q786':'Dominikaans',
    'Q801':'Israëlisch','Q884':'Zuid-Koreaans',
    'Q916':'Angolees','Q924':'Tanzaniaans','Q928':'Filipijns','Q953':'Zambiaans',
    'Q1009':'Kameroens','Q1028':'Marokkaans','Q1032':'Nigerees','Q1033':'Nigeriaans', 'Q1041':'Senegalees',
    'Q9676':'Brits', #eiland Man
    'Q15180':'Russisch','Q16635':'Guamees',
    'Q29999':'Nederlands',
    'Q33946':'Tsjecho-Slowaaks','Q36704':'Joegoslavisch',
            }

lng='nl'
site=pywikibot.Site(lng,'wikipedia')
repo=site.data_repository()
AWLversion='AWL20211103'
cleanup=True
fallback=['nl','en','de','fr']
SaR={'[[:Categorie:':'[[Categorie:',
     'Categorie:Antiguees olympisch deelnemer':'Categorie:Olympisch deelnemer uit Antigua en Barbuda',
     'uit [[Verenigde Staten':'uit de [[Verenigde Staten',
     'uit [[Verenigd K':'uit het [[Verenigd K',
     'Koninkrijk der Nederlanden':'Nederland',
     '(, ':'(',
     'Categorie:Dominicaans atleet':'Categorie:Atleet uit de Dominicaanse Republiek',
     'Categorie:Dominikaans olympisch deelnemer':'Categorie:Olympisch deelnemer uit de Dominicaanse Republiek',
     'op de Olympische Zomerspelen 1928]]':'op de Olympische Zomerspelen 1928|Olympische Zomerspelen van Amsterdam]] in 1928',
     'op de Olympische Zomerspelen 1932]]':'op de Olympische Zomerspelen 1932|Olympische Zomerspelen van Los Angeles]] in 1932',
     'op de Olympische Zomerspelen 1936]]':'op de Olympische Zomerspelen 1936|Olympische Zomerspelen van Berlijn]] in 1936',
     'op de Olympische Zomerspelen 1948]]':'op de Olympische Zomerspelen 1948|Olympische Zomerspelen van Londen]] in 1948',
     'op de Olympische Zomerspelen 1952]]':'op de Olympische Zomerspelen 1952|Olympische Zomerspelen van Helsinki]] in 1952',
     'op de Olympische Zomerspelen 1956]]':'op de Olympische Zomerspelen 1956|Olympische Zomerspelen van Melbourne]] in 1956',
     'op de Olympische Zomerspelen 1960]]':'op de Olympische Zomerspelen 1960|Olympische Zomerspelen van Rome]] in 1960',
     'op de Olympische Zomerspelen 1964]]':'op de Olympische Zomerspelen 1964|Olympische Zomerspelen van Tokio]] in 1964',
     'op de Olympische Zomerspelen 1968]]':'op de Olympische Zomerspelen 1968|Olympische Zomerspelen van Mexico]] in 1968',
     'op de Olympische Zomerspelen 1972]]':'op de Olympische Zomerspelen 1972|Olympische Zomerspelen van München]] in 1972',
     'op de Olympische Zomerspelen 1976]]':'op de Olympische Zomerspelen 1976|Olympische Zomerspelen van Montreal]] in 1976',
     'op de Olympische Zomerspelen 1980]]':'op de Olympische Zomerspelen 1980|Olympische Zomerspelen van Moskou]] in 1980',
     'op de Olympische Zomerspelen 1984]]':'op de Olympische Zomerspelen 1984|Olympische Zomerspelen van Los Angeles]] in 1984',
     'op de Olympische Zomerspelen 1988]]':'op de Olympische Zomerspelen 1988|Olympische Zomerspelen van Seoul]] in 1988',
     '[[Olympische Zomerspelen 1988]]':'Op de [[Olympische Zomerspelen 1988|Olympische Zomerspelen van Seoul]] in 1988',
     'op de Olympische Zomerspelen 1992]]':'op de Olympische Zomerspelen 1992|Olympische Zomerspelen van Barcelona]] in 1992',
     'op de Olympische Zomerspelen 1996]]':'op de Olympische Zomerspelen 1996|Olympische Zomerspelen van Atlanta]] in 1996',
     'op de Olympische Zomerspelen 2000]]':'op de Olympische Zomerspelen 2000|Olympische Zomerspelen van Sydney]] in 2000',
     'op de Olympische Zomerspelen 2004]]':'op de Olympische Zomerspelen 2004|Olympische Zomerspelen van Athene]] in 2004',
     'op de Olympische Zomerspelen 2008]]':'op de Olympische Zomerspelen 2008|Olympische Zomerspelen van Beijing]] in 2008',
     'op de Olympische Zomerspelen 2012]]':'op de Olympische Zomerspelen 2012|Olympische Zomerspelen van Londen]] in 2012',
     'op de Olympische Zomerspelen 2016]]':'op de Olympische Zomerspelen 2016|Olympische Zomerspelen van Rio de Janeiro]] in 2016',
     'op de Olympische Zomerspelen 2020]]':'op de Olympische Zomerspelen 2020|Olympische Zomerspelen van Tokio]] in 2021',
    }

eventconvert={
    'Javelin Throw':'speerwerpen',
    'Javelin Throw (700gr)':'speerwerpen (700gr)',
    'Long Jump':'verspringen',
    'Long Jump ind.':'verspringen ind.',
    'High Jump':'hoogspringen',
    'High Jump ind.':'hoogspringen ind.',
    'Pole Vault':'polsstokspringen',
    'Pole Vault ind.':'polsstokspringen ind.',
    'Decathlon':'tienkamp',
    'Decathlon - U20':'tienkamp - O20',
    'Decathlon - U18':'tienkamp - O18',
    'Heptathlon ind.':'zevenkamp ind.',
    'Heptathlon - U20 ind.':'zevenkamp - U20 ind',
    'Distance Medley':'afstandsestafette',
    'Distance Medley ind.':'afstandsestafette ind.',
    'Hammer Throw':'kogelslingeren',
    '100mH':'100 m horden',
    'Shot Put':'kogelstoten',
    'Shot Put ind.':'kogelstoten ind.',
    'Discus Throw':'discuswerpen',
             }
eventunit={'100m':'s','200m':'s','300m':'s','400m':'s','4x100':'s','Long Jump':'m','Pole Vault':'m','Decathlon':'p','High Jump':'m','100mH':'s',
           '100m ind.':'s','200m ind.':'s','300m ind.':'s','400m ind.':'s','4x100 ind.':'s','Long Jump ind.':'m','Pole Vault ind.':'m','High Jump ind.':'m',
          }
hdrconvert={'Event':'Onderdeel','Result':'Prestatie','Wind':'Wind','Venue':'Plaats','Date':'Datum'}

def monthname(month):
  nl_months=  {1:'januari',2:'februari',3:'maart',4:'april',5:'mei',6:'juni',7:'juli',8:'augustus',9:'september',10:'oktober',11:'november',12:'december'}
  papmonths= {1:'yanüari',2:'febrüari',3:'mart',4:'aprel',5:'mei',6:'yüni',7:'yüli',8:'ougùstùs',9:'sèptèmber',10:'oktober',11:'novèmber',12:'desèmber',}
  months={'nl':nl_months, 'pap':papmonths}
       
  return(months[lng][int(month)])

def get_formatter(wd,ppty):
  URLformat=''
  URLformatter=''  
  if not ppty in wd.claims: return(f'no url for {wd.title()}.{ppty}')  
  value=wd.claims[ppty][0].getTarget()
  if value==None: return('')  
  prop=pywikibot.PropertyPage(repo,ppty)  
  if not ('P1630' in prop.claims): return(f'no P1630 for {prop.title()}')  
  for c in prop.claims['P1630']:
    if (c.rank!='deprecated'):
      URLformat=c.getTarget()
    if (((URLformatter=='') or (c.rank=='preferred')) and (c.rank!='deprecated')):
      URLformatter=URLformat  
  return(URLformatter.replace('$1',value))

def getAthletePB(diamondID):
 url='https://www.diamondleague.com/athletes/%s.html'%diamondID
 f=urlopen(url)
 htmltext=f.read().decode('utf-8')
 soup=BeautifulSoup(htmltext)  
 pbtable=soup.find("table", attrs={"class":"personal-bests data"})
 pbevents=[th.get_text() for th in pbtable.find("tr").find_all("th")]   
 identifier='<!--leave for future auto-update [id:DL7156236875035]-->'

 pbresult = []
 for row in pbtable.find_all("tr")[1:]:
    dataset = dict(zip(pbevents, (td.get_text() for td in row.find_all("td"))))
    pbresult.append(dataset)    
    
 wikitable='==Persoonlijke records==\n'
 #outdoortable=f';Outdoor\n{{| class="wikitable"\n!Onderdeel\n!Prestatie\n!Plaats\n!Datum\n|-\n'
 #indoortable =f';Indoor\n{{| class="wikitable"\n!Onderdeel\n!Prestatie\n!Plaats\n!Datum\n|-\n'
 
 outdoortable=f';Outdoor\n{{| class="wikitable"'
 indoortable =f';Indoor\n{{| class="wikitable"'
 for event in pbevents:
   outdoortable += '\n!'+hdrconvert[event]
   indoortable  += '\n!'+hdrconvert[event]
 outdoortable += '\n|-\n'
 indoortable  += '\n|-\n'

    
 hasindoor=hasoutdoor=False
 for item in pbresult:
   itsout=itsin=False 
   for event in pbevents:
     if (event=='Event') and (item[event] in eventunit):
        unit=eventunit[item[event]]
     elif (event!='Result'):
        unit=''
     if event!='Event': 
        unitnow=unit   
     else:
        unitnow=''
     if (item['Event'].find('ind.')==-1): 
      if item[event] in eventconvert:
        item[event] = eventconvert[item[event]]
      outdoortable+='| '+item[event]+unitnow+'\n'
      hasoutdoor=itsout=True
     else: 
      if (item[event] in eventconvert):
        item[event]=eventconvert[item[event]]  
      indoortable+='| '+item[event]+unitnow+'\n'
      hasindoor=itsin=True
   if (itsout): outdoortable+='|-\n'
   if (itsin): indoortable+='|-\n'   
 month=date.today().strftime('%m')   
 monthstr=monthname(month)
 #monthstr=date.today().strftime('%B')
 yearstr =date.today().strftime('%Y')
 if hasindoor or hasoutdoor:
   if hasoutdoor:
     wikitable += outdoortable + '|}\n' 
   if hasindoor:     
        wikitable += indoortable + '|}\n'
   wikitable += f'bijgewerkt {monthstr}-{yearstr}<ref>[{url} Diamondleague]––profiel</ref>{identifier}\n'
 return(wikitable)

def findifs(wd,txt):
    """
    Find all ##if:P1234# constructions
    if P1234 is a claim, the line will stay, else it will be deleted
    """
    p=txt.find('##if:')
    while (p>0):
      end=p+2
      while txt[end:end+1]!='#':
        end+=1
      property=txt[p+5:end]  
      if property in wd.claims:
         txt=txt[:p]+txt[end+1:]
      else:
         while txt[end:end+1]!='\n': #find end of line
            end+=1
         txt=txt[:p]+txt[end+1:]
      p=txt.find('##if:')        
    
    """
    Find all #profiel:Pxxx# constructions
    if P1234 is a valid claim, the line will be filled out based on the URL-formtter of P1234
    """
    p=txt.find('##profiel:')
    while (p>0):
      end=p+2
      while txt[end:end+1]!='#':
        end+=1
      property=txt[p+10:end]  
      if property in wd.claims:
         txt=txt[:p]+txt[end+1:].replace('##format#',get_formatter(wd,property),1)
      else:
         while txt[end:end+1]!='\n': #find end of line
           end+=1
         txt=txt[:p]+txt[end+1:]
      p=txt.find('##profiel:')        
    
    """
    Find all ##loop:Pxxx# constructions
    if P1234 is a valid claim, it will add all linked claims as wikitext-link
    """
    p=txt.find('##loop:')
    while (p>0):
      end=p+2
      while txt[end:end+1]!='#':
        end+=1
      property=txt[p+7:end]
      if property in wd.claims:
        looptxt=''
        for x in range(0,len(wd.claims[property])):
            looptxt+=f'{wd_value(wd,property,True,x)}\n'
        txt=txt[:p]+looptxt+txt[end+1:]
      else:
        while txt[end:end+1]!='\n': #find end of line
          end+=1
        txt=txt[:p]+txt[end+1:]
      p=txt.find('##loop:')  
    return(txt)
    
def demonym(wd,lng):
    
  #return('')  
  if 'P27' in wd.claims:
    countryID=wd.claims['P27'][0].getTarget().title()
    if countryID in demonymList:
        return demonymList[countryID]
    land_bestaat_niet(countryID/0)
    country=pywikibot.ItemPage(repo,countryID)
    country.get(get_redirect=True)
    if ('P1549' in country.claims):
      dmn=country.claims['P1549']
      for dmnclaim in dmn:
        dmnclaim.get()    
        if dmnclaim.has_qualifier:
          qlf=dmnclaim.qualifiers
          if ('P518') in qlf:
            vtod=qlf['P518'][0].getTarget().title()
            if vtod=='Q47088290':  #mannelijk enkelvoud
              pass
            else:
              for x in dir(dmnclaim):
                print(x)
              print(f'claim={dmnclaim}')
              #print(f'vtod={vtod}')
          else:
            pass
            #print(f'qlf={qlf}')
        else:
          print(dmnclaim)  
    return('xXx')
  return('-nd-')

def find_properties(txt):
    i=0
    end=0
    while(i<len(txt)):
      if txt[i:i+2]=='<P':
        end=i
        while txt[end:end+1]!='>':
          end+=1
        yield(txt[i+1:end],'<')  
        i=end
      if txt[i:i+2]=='[P':
        end=i
        while txt[end:end+1]!=']':
          end+=1
        yield(txt[i+1:end],'[')  
        i=end
      if txt[i:i+2]=='!P':
        end=i
        while txt[end:end+1]!='!':
          end+=1
        yield(txt[i+1:end],'!')  
        i=end
      i+=1
      if txt[i:i+7]=='<label>':
        yield('label','')
        i+=7
      if txt[i:i+10]=='<demoniem>':
        yield('demoniem','')
        i+=10
      if txt[i:i+11]=='<templates>':
        yield('templates','')
        i+=11
      if txt[i:i+9]=='<inlinks>':
        yield('inlinks','')
        i+=9
      if txt[i:i+9]=='<sources>':
        yield('sources','')
        i+=9
      if txt[i:i+9]=='<diamond>':
        yield('diamond','')
        i+=9
      if txt[i:i+6]=='##var:':
        i=i+6
        end=i
        while txt[end:end+1]!=':':
          end+=1
        print(f'-var-: <{txt[i:end]}>, {i},{end}')
        yield(txt[i:end],'')    

def fill_in(txt,find,replace):
    return(txt.replace(find,replace,-1))
    
def getUnit(value):
    try:
      wdUnit=value.unit[value.unit.find('Q'):]
      unit=pywikibot.ItemPage(repo,wdUnit)
      unit.get(get_redirect=True)
      return(unit.labels[lng])  
    except Exception as e: 
        print(e)

def wd_value(wd,property,isLinked=False,index=0):
    
  image=pywikibot.page.FilePage(site,'image.png')  
    
  if property in wd.claims:
      value=wd.claims[property][index].getTarget()
      if value==None:
          return('none')
      if (type(value)==type(pywikibot.ItemPage(repo,'Q5'))):
        valuerec=pywikibot.ItemPage(repo,value.title())
        valuerec.get(get_redirect=True)
        if not lng in valuerec.labels:
            print(f'label missing in {valuerec.title()}.{property}')
            error('')
        if ((isLinked) and (lng+'wiki' in valuerec.sitelinks)):
          lbl=valuerec.labels[lng]
          lnk=valuerec.sitelinks[lng+'wiki'].title
          if (lbl[0].lower()==lnk[0].lower()) and (lbl[1:]==lnk[1:]):
            return(f'[[{lnk}]]')
          else:
            return(f'[[{lnk}|{lbl}]]')    
        else:
          return(valuerec.labels[lng])  
      elif (type(value)==type(pywikibot.WbTime(1,1,1))):
        if value.precision==11:
          return(str(value.day)+' '+monthname(value.month)+' '+str(value.year))
        elif value.precision==9:
          return(str(value.year))
        elif value.precision==7: #precision like 20th century : nothing valueble to return
          return('')
        return(f'date-time: precision={value.precision}')
      elif (type(value)==type('str')):
        return(value)
      elif (type(value)==type(pywikibot.WbMonolingualText('nl','nl'))):
          return(value.text)  
      elif (type(value)==type(pywikibot.WbQuantity(0,site=site))):
        if value.unit:
          return(f'{str(value.amount)} {getUnit(value)}')
        return(str(value.amount))
      elif (type(value)==type(pywikibot.page.FilePage(site,'image.png'))): #P18 image on Commons
         return(value.title()[5:])
    
    
      else:
        print(f'unknown type: {type(value)}')
        return('else')
      return value
  elif property=='label':
    try:
      return(wd.labels[lng])  
    except:
      pass
  elif property=='demoniem':
     return(demonym(wd,lng))
  elif property=='templates':
     return(whatlinkshere(lng,wd.labels[lng],[10])) #actually wd.links[wiki+'lng'] 
  elif property=='inlinks':
     return(whatlinkshere(lng,wd.labels[lng],[0]))  #but lemma does not exist yet
  elif property=='sources':
     return(getSources(wd)) 
  elif property=='diamond':
     if ('P3923' in wd.claims):    
       return(getAthletePB(wd.claims['P3923'][0].getTarget()))   
     return('')
  else:
    if (cleanup):
      return('') 
    else:
      return('<'+property+'>')
  return('')
 
def getSourceURLs(wd):
 urls=[]
 for c in wd.claims: 
  claimlist=wd.claims[c]
  for claim in claimlist:
    sources=claim.getSources()
    if sources!=[]: 
      for sourcelist in sources:  
       if ('P854' in sourcelist): 
        for source in sourcelist['P854']:
          url=source.getTarget()
          if (not(url in urls)):
              urls.append(url)
 return(urls)         
  
def getSources(wd):
 sourcelist=''
 count=0
 for sourceURL in getSourceURLs(wd):
   count+=1           
   sourcelist=sourcelist+f'<ref>[{sourceURL} bron {count}]––</ref>\n'         
 return(sourcelist)           
    
def whatlinkshere(lng,item,namespaces):
  site=pywikibot.Site(lng,'wikipedia')
  page=pywikibot.Page(site,item)
  result=''
  for found in page.getReferences(namespaces=namespaces):
    start=found.title().find(':')
    if (10 in namespaces):
      result+='{{'+found.title()[start+1:]+'}}\n'
    else:
      result+='[['+found.title()[start+1:]+']]\n'
  return result

def readTemplate(name):
    site=pywikibot.Site(lng,'wikipedia')
    page=pywikibot.Page(site,'gebruiker:Edoderoo/template/'+name)
    try:
      #print('1')  
      glbPage=pywikibot.Page(site,'gebruiker:Edoderoo/template/global')  
      #print('22')  
      globaltxt=glbPage.text  
      #print('333')  
    except:
      globaltxt=''
      print('gebruiker:Edoderoo/template/global not found')
    if (page.exists()):
      return(page.text.replace('<global>',globaltxt))
    else:
      return(name+'does not exist!')  
    

def getTemplate(wd):
  if 'P106' in wd.claims:
    for beroep in wd.claims['P106']:
      beroepID=beroep.getTarget().title()
      if (False): pass
      elif beroepID=='Q2309784' : return readTemplate('wielrenner')
      elif beroepID=='Q15117395': return readTemplate('wielrenner')
      elif beroepID=='Q15117415': return readTemplate('wielrenner')
      elif beroepID=='Q19799599': return readTemplate('wielrenner')
      elif beroepID=='Q937857'  : return readTemplate('voetballer')
      elif beroepID=='Q11513337': return readTemplate('atleet')
      elif beroepID=='Q4009406' : return readTemplate('atleet')
      elif beroepID=='Q13381689': return readTemplate('atleet')
      elif beroepID=='Q13724897': return readTemplate('atleet')
      elif beroepID=='Q15306067': return readTemplate('sporter') #triatleet
      elif beroepID=='Q13381753': return readTemplate('atleet')
      elif beroepID=='Q21141408': return readTemplate('atleet')
      elif beroepID=='Q15972912': return readTemplate('sporter') #moderne vijfkamp
      elif beroepID=='Q10866633': return readTemplate('schaatser')
      elif beroepID=='Q18200514': return readTemplate('schaatser')
      elif beroepID=='Q10843263': return readTemplate('hockeyspeler')
      elif beroepID=='Q10843402': return readTemplate('zwemmer')
      elif beroepID=='Q13141064': return readTemplate('badmintonner')  
      elif beroepID=='Q10833314': return readTemplate('tennisser')
      elif beroepID=='Q13381863': return readTemplate('schermer')
      elif beroepID=='Q11774891': return readTemplate('ijshockeyer')
      elif beroepID=='Q17516936': return readTemplate('curlingspeler')
      elif beroepID=='Q859528'  : return readTemplate('scheidsrechter')
      elif beroepID=='Q3665646' : return readTemplate('basketballer')  
      elif beroepID=='Q15117302': return readTemplate('volleyballer')
      elif beroepID=='Q12840545': return readTemplate('handballer')
      elif beroepID=='Q13382519': return readTemplate('tafeltennisser')
      elif beroepID=='Q10873124': return readTemplate('schaker')
      elif beroepID=='Q13382608': return readTemplate('wintersporter') 
      elif beroepID=='Q4270517' : return readTemplate('wintersporter')
      elif beroepID=='Q4144610' : return readTemplate('wintersporter')
      elif beroepID=='Q13382981': return readTemplate('sporter') #rodelaar
      elif beroepID=='Q16029547': return readTemplate('sporter') #biatleet
      elif beroepID=='Q6665249' : return readTemplate('sporter') 
      elif beroepID=='Q482980'  : return readTemplate('auteur')
      elif beroepID=='Q36180'   : return readTemplate('auteur')
      elif beroepID=='Q4853732' : return readTemplate('auteur')
      elif beroepID=='Q33999'   : return readTemplate('acteur')
      elif beroepID=='Q10800557': return readTemplate('acteur')
      elif beroepID=='Q177220'  : return readTemplate('artiest')
      elif beroepID=='Q82955'   : return readTemplate('politicus')
      elif beroepID=='Q43845'   : return readTemplate('ondernemer')
      elif beroepID=='Q131524'  : return readTemplate('ondernemer')
    print(f'beroep not found: {beroep}')
  if 'P31' in wd.claims:
    for is_a in wd.claims['P31']:
      its_a=is_a.getTarget().title()
      if   its_a=='Q8502': return readTemplate('berg')
      elif its_a=='Q4022': return readTemplate('rivier')  
      elif its_a=='Q23397': return readTemplate('meer')
      elif its_a=='Q1134686': return readTemplate('frazione')  
      elif its_a=='Q16917': return readTemplate('ziekenhuis')
      elif its_a=='': return readTemplate('error') 
      else:
        print('Unknown %s', its_a)
        error('')
  return wd.title()

def standardReplace(input):
    output=input
    for fnd in SaR:
      output=output.replace(fnd,SaR[fnd])  
    return(output)

def maak_item(qid):
  wd=pywikibot.ItemPage(repo,qid)
  wd.get(get_redirect=True)
  txt=getTemplate(wd)
  if not(lng+'wiki' in wd.sitelinks):
    if not lng in wd.labels:
      error('Add a label first, it will become the title')  
    for p,isLinked in find_properties(txt): 
      value=wd_value(wd,p,isLinked=='[')
      if isLinked=='[':
        txt=fill_in(txt,'['+p+']',value)    
      elif isLinked=='<':
        txt=fill_in(txt,'<'+p+'>',value)
      elif isLinked=='!':
        txt=fill_in(txt,'!'+p+'!',value)
      elif p in ['label','demoniem','templates','inlinks','sources','diamond']:
        txt=fill_in(txt,f'<{p}>',value)
      else:      
        sys.exit(f'unknown: {isLinked}{p}{isLinked}')
        
    txt=txt+f'<!--{AWLversion}-->\n'    
    txt=txt+'<!--'+wd.title()+'-->'
    
    return(standardReplace(findifs(wd,txt)))
  else:
    return(f'{qid} already exists for {lng}') #already exists for this language
    


#print('Start')
#print(maak_item(''))
#print(maak_item(''))
#print(maak_item(''))
#print(maak_item(''))



#Britse wielrensters
#print(maak_item(' Q4892820 '))
#print(maak_item(' Q5126175 '))
#print(maak_item(' Q5349454 '))
#print(maak_item(' Q5478866 '))
#print(maak_item(' Q6698416 '))
#print(maak_item(' Q6761356 '))
#print(maak_item(' Q6369588 '))
#print(maak_item(' Q6377418 '))
#print(maak_item(' Q6572944 '))
#print(maak_item(' Q7405083 '))
#print(maak_item(' Q7982648 '))
#print(maak_item(' Q5648940 '))
#print(maak_item(' Q13126994 '))
#print(maak_item(' Q16727729 '))
#print(maak_item(' Q16212417 '))
#print(maak_item(' Q16885292 '))
#print(maak_item(' Q17465887 '))
#print(maak_item(' Q19661862 '))
#print(maak_item(' Q19867752 '))
#print(maak_item(' Q20090311 '))
#print(maak_item(' Q22957492 '))
#print(maak_item(' Q23661777 '))
#print(maak_item(' Q26236411 '))
#print(maak_item(' Q26252253 '))



####Red Flames - Belgisch nationaal elftal
#print(maak_item('Q98070069')) #Hannah Eurlings
#print(maak_item('Q24937733')) #Charlotte Tison
#print(maak_item('Q3258775')) #Lola Wajnblum
#print(maak_item('Q97749939')) #Jody Vangheluwe
#print(maak_item('Q98067295')) #Zandy Soree
#print(maak_item('Q98071695')) #Jill Janssens
#print(maak_item('Q55596472')) #Constance Brackman
#print(maak_item('Q97763333')) #Marie Detruyer





#EK zwemmen 2018
#print(maak_item('Q33836493')) #Katalin Burián
#print(maak_item('Q17620822')) #Arianna Castiglioni
#print(maak_item('Q18127510')) #Molly Renshaw
#print(maak_item('Q56073311')) #Imogen Clark
#print(maak_item('Q33424890')) #Emilie Beckmann
#print(maak_item('Q14504132')) #Svetlana Tsjimrova
#print(maak_item('Q3721409')) #Elena Di Liddo
#print(maak_item('Q33423877')) #Alys Thomas
#print(maak_item('Q23749166')) #Fantine Lesaffre
#print(maak_item('Q55942657')) #Ilaria Cusinato
#print(maak_item('Q26236434')) #Maria Ugolkova
#print(maak_item('Q19958626')) #Marie Wattel
#print(maak_item('Q23761440')) #Margaux Fabre
#print(maak_item('Q55956362')) #Anouchka Martin
#print(maak_item('Q55180772')) #Assia Touati
#print(maak_item('Q33321250')) #Signe Bro
#print(maak_item('Q25934623')) #Julie Kepp Jensen
#print(maak_item('Q55956363')) #Emily Gantriis
#print(maak_item('Q56043723')) #Kathryn Greenslade
#print(maak_item('Q33323444')) #Holly Hibbott
#print(maak_item('Q33624427')) #Freya Anderson
#print(maak_item('Q56043729')) #Lucy Hope
#print(maak_item('Q56073317')) #Valeria Salamatina
#print(maak_item('Q56253792')) #Anna Jegorova
#print(maak_item('Q20716411')) #Arina Openysjeva
#print(maak_item('Q37118364')) #Anastasia Goezjenkova
#print(maak_item('Q28664966')) #Irina Krivonogova
#print(maak_item('Q56043732')) #Reva Foos
#print(maak_item('Q30329373')) #Isabel Gose
#print(maak_item('Q567102')) #Annika Bruhn
#print(maak_item('Q55776956')) #Marie Pietruschka
#print(maak_item('Q28664863')) #Maria Kameneva
#print(maak_item('Q17640625')) #Vitalina Simonova
#print(maak_item('Q24450795')) #Kathleen Dawson

#print(maak_item('Q106874790')) #Viktória Mihályvári-Farkas
#print(maak_item('Q63184646')) #Ida Hulkko
#print(maak_item('Q65769725')) #Lisa Mamié
#print(maak_item('Q33404688')) #Charlotte Atkinson
#print(maak_item('Q9323051')) #Rozalja Nasretdinova
#print(maak_item('Q7929931')) #Victoria Andrejeva


#Olympisch kampioenen schermen
#print(maak_item('Q2735040'))
#print(maak_item('Q77727'))
#print(maak_item('Q25771'))
#print(maak_item('Q454570'))
#print(maak_item('Q222007'))
#print(maak_item('Q240984'))
#print(maak_item('Q2603280'))
#print(maak_item('Q4025625'))
#print(maak_item('Q26252'))
#print(maak_item('Q155109'))
#print(maak_item('Q2724865'))
#print(maak_item('Q3796367'))
#print(maak_item('Q1657750'))
#print(maak_item('Q557494'))
#print(maak_item('Q239368'))
#print(maak_item('Q447594'))
#print(maak_item('Q832286'))
#print(maak_item('Q26002'))
#print(maak_item('Q717813'))
#print(maak_item('Q2567325'))
#print(maak_item('Q25959'))
#print(maak_item('Q3291599'))
#print(maak_item('Q3847888'))
#print(maak_item('Q2360198'))
#print(maak_item('Q2360198'))
#print(maak_item('Q1642898'))
#print(maak_item('Q497165'))
#print(maak_item('Q3881434'))
#print(maak_item('Q432388'))
#print(maak_item('Q543557'))
#print(maak_item('Q26241'))
#print(maak_item('Q77719'))
#print(maak_item('Q2447879'))
#print(maak_item('Q464553'))
#print(maak_item('Q95165'))
#print(maak_item('Q1642880'))
#print(maak_item('Q2360225'))
#print(maak_item('Q2735605'))
#print(maak_item('Q2383335'))


#print(maak_item('Q56736494'))  #Maryse Perreault
#print(maak_item('Q11399474'))  #Miyoshi Katō
#print(maak_item('Q8070385'))   #Zhang Yanmei
#print(maak_item('Q8070385'))   #Zhang Yanmei
#print(maak_item('Q6078198'))   #Isabelle Charest
#print(maak_item('Q43634313'))  #Marinella Canclini
#print(maak_item('Q19519519')) #Vicki Whitelaw
#print(maak_item('Q51193326')) #Rosalisa Lapomarda
#print(maak_item('Q434958')) #Elena Tchalykh
#print(maak_item('Q8072829')) #Zita Urbonaite
#print(maak_item('Q41560129')) #Katia Longhin
#print(maak_item('Q20707170')) #Jorunn Kvalø
#print(maak_item('Q1450948')) #Valentina Polkhanova
#print(maak_item('Q23892874')) #Sara Felloni
#print(maak_item('Q4962422')) #Madeleine Lindberg
#print(maak_item('Q19757564')) #Oksana Saprykina
#print(maak_item('Q3766280')) #Giovanna Troldi
#print(maak_item('Q28873224')) #Goulnara Ivanova
#print(maak_item('Q28873565')) #Sonia Rocca
#print(maak_item('Q3419787')) #Rasa Mazeikyte
#print(maak_item('Q55343158')) #Mandy Hampel
#print(maak_item('Q55111813')) #Yuliya Murenka

#wimbledon doubles
#print(maak_item('Q434577')) #Patricia Canning Todd
#print(maak_item('Q299610')) #Peggy Michel
#print(maak_item('Q429375')) #Phyllis Mudford King

#GOUD op de Spelen
#print(maak_item('Q268500')) #Maureen Caird
#print(maak_item('Q264031')) #Chryste Gaines
#print(maak_item('Q265187')) #Janina Koroltsjik
#print(maak_item('Q267935')) #Madeline Manning
#print(maak_item('Q268767')) #Benita Fitzgerald
#print(maak_item('Q273679')) #Mary Peters
#print(maak_item('Q272669')) #Jearl Miles-Clark
#print(maak_item('Q270976')) #Christina Brehmer
#print(maak_item('Q290589')) #Maicel Malone
#print(maak_item('Q299733')) #Ellen Streidt

#print(maak_item('Q435765')) #Mildrette Netter
#print(maak_item('Q442645')) #Rochelle Stevens
#print(maak_item('Q443248')) #Dagmar Käsling
#print(maak_item('Q443195')) #Carlette Guidry
#print(maak_item('Q443521')) #Doris Maletzki
#print(maak_item('Q438321')) #Carla Bodendorf
#print(maak_item('Q444287')) #Brigitte Rohde
#print(maak_item('Q450975')) #Barbara Ferrell
#print(maak_item('Q450168')) #Christiane Krause
#print(maak_item('Q458425')) #Nina Zjoeskova
#print(maak_item('Q458171')) #Irina Nazarova
#print(maak_item('Q458725')) #Lillie Leatherwood
#print(maak_item('Q456852')) #Sherri Howard

### vrouwen - gendergap ###
#print(maak_item('Q16596904')) #Fabiana Santos, bobsleester uit Brazilië
#print(maak_item('Q16187938')) #Sally Mayara da Silva, bobsleester uit Brazilië
#print(maak_item('Q15831609 ')) #Joselane Santos, freestyleskiester uit Brazilië
#print(maak_item('Q2160288  ')) #Isadora Williams, Braziliaans kunstschaatsster
#print(maak_item('Q3292113 ')) #Marie-Madeleine Dienesch, frans politica
#print(maak_item('Q3144735 ')) #Hélène Conway-Mouret, frans politica
#print(maak_item('Q3144821 ')) #Hélène Missoffe, frans politica
#print(maak_item('Q51034552 ')) #Braziliaans alpine-skieer
#print(maak_item('Q49479895 ')) #wintersporter
#print(maak_item('Q58368255 ')) #Aurélie Monvoisin - shorttrack
#print(maak_item('Q58368749')) #Kristen Santos - schaatser/shorttrack
#print(maak_item('Q86628178 ')) #Braziliaans autocoureur
#print(maak_item('Q4664139 ')) #Brits autocoureur
#print(maak_item('Q86756577 ')) #Spaans autocoureur
#print(maak_item('Q86744623 ')) # Spaans autocoureur
#print(maak_item('Q61335619 ')) # Noors-Zweeds autocoureur
#print(maak_item('Q49479895 ')) #langlaufer

#WK indoor-atletiek
#print(maak_item('Q166195')) #Georganne Moline
#print(maak_item('Q23306222')) #Quanera Hayes
#print(maak_item('Q461285')) #Anita Márton
#print(maak_item('Q19879200')) #Vashti Cunningham
#print(maak_item('Q16855061')) #Kemi Adekoya
#print(maak_item('Q9188807')) #Chanelle Price
#print(maak_item('Q14621729')) #Joanna Atkins
#print(maak_item('Q15965378')) #Cassandra Tate
#print(maak_item('Q274796')) #Éloyse Lesueur
#print(maak_item('Q15719309')) #Kamila Lićwinko
#print(maak_item('Q13581118')) #Jekaterina Koneva
#print(maak_item('Q439715')) #Shana Cox
#print(maak_item('Q441119')) #Perri Shakes-Drayton
#print(maak_item('Q443605')) #Kalkidan Gezahegne
#print(maak_item('Q442156')) #Natallja Safronnikava
#print(maak_item('Q434700')) #Ashia Hansen
#print(maak_item('Q264937')) #Irina Korzhanenko
#print(maak_item('Q264937')) #	Juliet Campbell
#print(maak_item('Q436568')) #Anjanette Kirkland
#print(maak_item('Q458670')) #Dawn Burrell
#print(maak_item('Q434934')) #Pavla Hamácková
#print(maak_item('Q270779')) #Larisa Peleshenko
#print(maak_item('Q284782')) #Natalya Sazanovich
#print(maak_item('Q445585')) #Anastasija Reiberger
#print(maak_item('Q2463047')) #Ekaterini Koffa
#print(maak_item('Q272669')) #Jearl Miles-Clark
#print(maak_item('Q238219')) #Fiona May
#print(maak_item('Q508020')) #Tatyana Alekseyeva
#print(maak_item('Q61460')) #Alina Astafei
#print(maak_item('Q181644')) #Aliuska Lopez
#print(maak_item('Q456778')) #Melinda Gainsford-Taylor
#print(maak_item('Q3180291')) #Joetta Clark
#print(maak_item('Q457558')) #Liliana Năstase
#print(maak_item('Q3293011')) #Marieta Ilcu
#print(maak_item('Q469883')) #Julie Baumann
#print(maak_item('Q537671')) #Sandra Seuser
#print(maak_item('Q879772')) #Katrin Schreiter
#print(maak_item('Q537562')) #Annett Hesselbarth
#print(maak_item('Q290785')) #Sui Xinmei
#print(maak_item('Q456088')) #Larisa Berezjna
#print(maak_item('Q3292214')) #Marie-Pierre Duros
#print(maak_item('Q444754')) #Diane Dixon
#print(maak_item('Q3572109')) #Jelizaveta Chernisjova
#print(maak_item('Q452519')) #Giuliana Salce

#atletiek wereldrecord
#print(maak_item('Q3154318')) #Irene Jelagat
#print(maak_item('Q433832')) #Mercy Cherono
#print(maak_item('Q16224285')) #Gudaf Tsegay
#print(maak_item('Q25350692')) #Chrishuna Williams

#Nederlands record atletiek
#print(maak_item('Q109474570')) #Debby van der Schilt
#print(maak_item('Q109474582')) #Lisanne Schol
#print(maak_item('Q107098036')) #Irene van der Reijken
#print(maak_item('')) #Lilian van der Ham
#print(maak_item('')) #Hilly Gankema
#print(maak_item('Q109474655')) #Conny Vermazen
#print(maak_item('')) #Ria Buiten
#print(maak_item('')) #Leonie Ton

#WorldCup schaatsen
#print(maak_item('Q104531511')) #Maddison Pearman
#print(maak_item('Q104531510')) #Alexa Scott
#print(maak_item('Q16015545')) #Ine ter Laak-Spijk
#print(maak_item('Q57314856')) #Andrea Bouma
#print(maak_item('Q16015346')) #Nel Zwier
#print(maak_item('Q19958448')) #Sharika Nelvis

#print(maak_item('Q17523965')) #Kelsey-Lee Roberts
#print(maak_item('Q51885429')) #Ruth Chepngetich
#print(maak_item('Q52676973')) #Liang Rui


#print(maak_item('Q110472248')) #Saskia Egas - HEMA
#print(maak_item('Q64524978')) #amandine fouquenet 3e frans kampioenschap
#print(maak_item('Q109424589')) #Line Burquier frans kampioene
#print(maak_item('Q110490708')) #Harriet Harnden, Brits nat. kamp.
#print(maak_item('Q110489040')) #Kristýna Zemanová, cz nat.kamp.
#print(maak_item('Q27947817')) #Li Xuesong
#print(maak_item('')) #

print(maak_item('Q7380460')) #
#print(maak_item('')) #
#print(maak_item('')) #
#print(maak_item('')) #

