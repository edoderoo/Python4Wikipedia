#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# (C) Edoderoo/Edoderoobot (meta.wikimedia.org), 2016–2019
# Distributed under the terms of the CC-BY-SA 3.0 licence.

#Q13005188 mandal 

import pywikibot
from pywikibot import pagegenerators as pg
from pywikibot.data import api
import codecs
import sys
import datetime
#import wd_generators.py
from datetime import datetime, date, time, timedelta


debugedo=True   #use one item, just to test
debugedo=False  #use wd-query, process a lot

#demoniem = P1549
geborenCLAIM =     'P569'
gestorvenCLAIM=    'P570'
is_eenCLAIM=       'P31'
genderCLAIM =      'P21'
countryCLAIM =     'P17'
female_genderPROP ='Q6581072'
male_genderPROP =  'Q6581097'
gelegen_inCLAIM=   'P131'
beroepCLAIM=       'P106'
items2do = 0    #global parameter to print progress 
commit=False    #no changes online, only to the logfiles
commit=True     #write changes to the database
CheckFilled=True
NoCheckFilled=False
SkipFilled=True
ReplaceContents=False
MultiLanguage=True
mailstart=datetime.now().strftime("%Y-%b-%d    ––>[%H:%M]<––" )
mailmessage='<default message>'
totaledits=0

lng_canbeused = ['en','de','fr','it','es','pt','ca','dk','cs','hr','nl','ro','sh','vi','eo','simple','eu','zea','li','fy','oc','af','nb','no','pl','si','sv','wa',]
default_query = 'claim[31:5] and claim[106] and claim[27] and link[nlwiki]'  # people with an occupation, a country and a page on nl-wiki
default_query = 'link[nlwiki]'   # just go along all nl-wiki articles, and see by P31 what you can do
update_label_allowed=[
  'Q5',      #human
  'Q318',    #galaxy
  'Q523',    #ster
  'Q532 ',   #dorp/village
  'Q3863',   #planetoide
  'Q6243',   #veranderlijke ster
  'Q7187',   #gen
  'Q7366',   #lied
  'Q7889',   #computerspel
  'Q8054',   #proteine
  'Q8502',   #berg
  'Q9842',   #basisschool
  'Q11032',  #newspaper - krant
  'Q12280',  #brug
  'Q13632',  #planetaire nevel
  'Q16521',  #taxon
  'Q30198',  #moeras
  'Q30612',  #klinisch onderzoek
#  'Q39614', #begraafplaats
  'Q44539',  #tempel
  'Q44559',  #exoplaneet
  'Q49008',  #priemgetal
  'Q54050',  #heuvel
  'Q79007',  #straat
  'Q83373',  #quasar
  'Q95074',  #personage
  'Q101352', #last name
  'Q106658', #landkreis
  'Q115518', #planetaire nevel
  'Q123705', #wijk
  'Q130019', #koolstofster
  'Q134556', #music single
  'Q178122', #aria
  'Q182832', #concert
  'Q191067', #redactieel artikel
  'Q202444', #first name
  'Q204107', #cluster van sterrenstelsels
  'Q204194'  #absorptienevel
  'Q207628', #compositie
  'Q215380', #musicband
  'Q222910', #music album
  'Q253019', #ortsteil
  'Q272447', #moleculaire wolk
  'Q277338', #pseudogen
  'Q569500', #wijkgezondheidscentrum
  'Q620615', #mobile app
  'Q737498', #wetenschappelijk tijdschrift 
  'Q486972', #nederzetting
  'Q482994', #music album
  'Q726242', #RRLYR-ster
  'Q732577', #publicatie
  'Q1149652', #district in India
  'Q1153690', #lange periode variabele ster    
  'Q1260524', #time of day
  'Q1332364', #roterende ellipsoide ster
  'Q1348589', #maankrater
  'Q1457376', #overlappende dubbelster
  'Q1690211', #openbare wasplaats
  'Q2065704', #tingrett
  'Q2247863', #hardlopende ster
  'Q2557101', #LINER
  'Q4502142', #visueel kunstwerk
  'Q5633421', #scientific magazine
  'Q7302866', #nummer van een CD
  'Q13005188', #mandal in India
  'Q13442814', #scientific article
  'Q15917122', #rotating variable ster
  'Q19389637', #biografisch artikel
  'Q20741022', #model digital camera
  'Q21014462', #cel lijn
  'Q2116450', #havezate
  'Q21278897', #wiktionary redirect
  'Q21573182', #natuurmoment in Duitsland
  'Q23925393', #douar, Marokkaans bestuurlijkg gebied
  #'Q26703203', #stolperstein
  'Q50386450', #opera-personage
  'Q53764738', #chinees karakter
  'Q56436498', #dorp in India
  'Q58034280', #bijgebouw
  'Q66619666', #rode reuzentak-ster
  'Q67206691', #infraroodbron
  'Q71963409', #comact group of galaxy
  'Q72802508', #emissielijn-sterrenstelsel
  'Q72803426', #horizontale tak
  'Q72803622', #emissie-lijn-ster
  'Q88965416', #Zweedse schooleenheid
  'Q97695005', #Irish Townsend
                      ]
run_lng = 'nl'
txt2skip = '|skip!|'
output2screen = False
prelog = True
prelog = False   #if set to True, it will write an extra logfile containing the item before it is processed, helpful in case of an error on unknown items
skiplog= True

all_types_list=[
                'Q16970',  #kerkgebouw
                'Q34763',  #schiereiland
                'Q95074',  #personage
                'Q2912397' #eendaagse wielerwedstrijd
                'Q23442',  #eiland
                'Q23397',  #meer
                'Q102496', #parochie
                'Q273057', #discografie
                'Q207628', #compositie
                'Q571',    #boek
                'Q134556', #single
               ]

simple_set_byP131=[
            'Q24764','Q70208','Q127448','Q203300','Q262166','Q262166','Q378508','Q484170','Q493522','Q612229','Q640364','Q659103','Q667509','Q747074','Q755707','Q856076','Q856079','Q955655','Q1054813',
            'Q13218690', 'Q15127838', 'Q2261863', 'Q494721',#steden
            'Q1363145','Q1500350','Q1500352','Q1530824','Q1840161','Q2661988','Q2590631','Q2460358','Q1849719','Q2989398','Q3327873','Q3685462','Q5154047','Q6784672','Q16739079','Q20538317',
            'Q23925393', #marokkaanse douar 
            'Q23012917', 'Q2225692','Q4174776','Q13100073','Q23827464','Q3558970','Q15630849','Q21672098', #dorpen
            'Q188509', #buitenwijk
            'Q9842',  #basisschool
            'Q3914', #school
            'Q355304', #watergang
            'Q54050',#heuvel
            'Q166735',#broekbos
            '','','','','','','','','','','','','','',
           ]              

labelSkipBrackets=['Q318',
  'Q318',    #galaxy
  'Q523',    #ster
  'Q3863',   #planetoide
  'Q6243',   #veranderlijke ster
  'Q7187',   #gen
  'Q7366',   #lied
  'Q7889',   #computerspel
  'Q8054',   #proteine
  'Q13632',  #planetaire nevel
  'Q16521',  #taxon
  'Q30612',  #klinisch onderzoek
  'Q115518', #planetaire nevel
  'Q130019', #koolstofster
  'Q134556', #music single
  'Q178122', #aria
  'Q191067', #redactieel artikel
  'Q204107', #cluster van sterrenstelsels
  'Q204194'  #absorptienevel
  'Q222910', #music album
  'Q272447', #moleculaire wolk
  'Q277338', #pseudogen
  'Q482994', #music album
  'Q726242', #RRLYR-ster
  'Q732577', #publicatie
  'Q1153690', #lange periode variabele ster    
  'Q1332364', #roterende ellipsoide ster
  'Q1348589', #maankrater
  'Q1457376', #overlappende dubbelster
  'Q2247863', #hardlopende ster
  'Q5633421', #scientific magazine
  'Q13442814', #scientific article
  'Q15917122', #rotating variable ster
  'Q19389637', #biografisch artikel
  'Q20741022', #model digital camera
  'Q21014462', #cel lijn
  'Q66619666', #rode reuzentak-ster
  'Q67206691', #infraroodbron
  'Q71963409', #comact group of galaxy
  'Q72802508', #emissielijn-sterrenstelsel
  'Q72803622', #emissie-lijn-ster
  'Q88965416', #Zweedse schooleenheid
]

scientist={'nl':'onderzoeker','en':'scientist'}

def sendmail(changemail,totalreads,totaledits):
  global mailmessage
  global mailstart
  mailend=datetime.now().strftime("%Y-%b-%d    ––>[%H:%M]<––" )
    
  if mailmessage=='hourly':
    subj='hourly--Set-nl-Description--hourly'
  else:
    subj='Set-nl-Description'    
        
  mailtxt=f'Start: {mailstart}\nType:{mailmessage}\nEnd: {mailend}\n\n{changemail}\nEdits: {totaledits}\nItems: {totalreads}'
  mailuser=pywikibot.User(pywikibot.Site('nl'),'Edoderoo')
  mailuser.send_email(subject=subj, text=mailtxt)

def log_premature(itemno):
  with codecs.open("NL-omschrijving.prelog.csv","a", encoding="utf-8") as logfile:
    logfile.write('%s\n' % (itemno))
  logfile.close

def log_skipped(itemno):
  with codecs.open("NL-omschrijving.skiplog.csv","a", encoding="utf-8") as logfile:
    logfile.write('%s\n' % (itemno))
  logfile.close
  
  
def logme(verbose, formatstring, *parameters):
  with codecs.open("NL-omschrijving.log.csv", "a", encoding="utf-8") as logfile:
    formattedstring = u'%s%s' % (formatstring, '\n')

    outputstr = (formatstring % (parameters))
    if ((outputstr[:7]=='Unknown') and (outputstr.find('|')==0)):   #Unknown error, no extra parameter, do not log
      pass
    else:  
       try:   
         logfile.write(formattedstring % (parameters) )
       except :
         exctype, value = sys.exc_info()[:2]
         print("1) Error writing to logfile on: [%s] [%s]" % (exctype, value))
         verbose = True    #now I want to see what!   
       logfile.close()
  if verbose:
    print(formatstring % (parameters))  

def log_unknown(verbose, formatstring, *parameters):    
  if False:
    with codecs.open("NL-omschrijving.missing.csv", "a", encoding="utf-8") as logfile:
     formattedstring = u'%s%s' % (formatstring, '\n')
    
     try:   
       logfile.write(formattedstring % (parameters))
     except :
       print("2) Error writing to logfile on")   
       verbose = True    #now I want to see what!
    logfile.close()
    if verbose:
     print(formatstring % (parameters))  

def get_property_id(findProperty):
 switcher={ 'date of birth' : 'P569',
            'is a' : is_eenCLAIM,
            'occupation' : beroepCLAIM,
            'country of citizenship' : 'P27'
          }
 return switcher.get(findProperty,'zxx')

def nameofcitizenship(CountryName,Occupation) :
           switcher = {
             'Koninkrijk der Nederlanden'     : 'Nederlands',
             'Nederland'                      : 'Nederlands',
             'Frankrijk'                      : 'Frans', 
             'Verenigde Staten van Amerika'   : 'Amerikaans', 
             'Spanje'                         : 'Spaans' ,
             'Verenigd Koninkrijk'            : 'Brits',
             'Duitsland'                      : 'Duits',
             'Rusland'                        : 'Russisch' ,
             'Polen'                          : 'Pools',
             'Luxemburg'                      : 'Luxemburgs',
             'Duitse Democratische Republiek' : 'Oost-Duits',
             'India'                          : 'Indiaas',
             'Turkije'                        : 'Turks',
             'Finland'                        : 'Fins',
             'Volksrepubliek China'           : 'Chinees',
             'Japan'       : 'Japans',
             'Zweden'      : 'Zweeds',
             'Canada'      : 'Canadees',
             'Colombia'    : 'Colombiaans',
             'Hongarije'   : 'Hongaars',
             'Argentinië'  : 'Argentijns',
             'Noorwegen'   : 'Noors',
             'Sovjet-Unie' : 'Russisch',
             'Spanje'      : 'Spaans',
             'Portugal'    : 'Portugees',
             u'Denemarken' : 'Deens',
             '' : '',
             u'Italië' : 'Italiaans' ,
             u'België' : 'Belgisch' ,
           }
           demonym = switcher.get(CountryName,"")
           if demonym=="": 
             return Occupation+' uit '+CountryName
           else:
             return demonym.strip()+' '+Occupation

def get_lng_description(language, wikidataitem):
  if language in wikidataitem.descriptions:
    return wikidataitem.descriptions[language]
  else:
    return('')

def get_lng_label(language,wikidataitem):
  if language in wikidataitem.labels:
    return wikidataitem.labels[language]
  else:
    return('')

def make_yeardatestr(thisdate):    
    #import pdb; pdb.set_trace();
    if not(thisdate is None): 
      if thisdate.precision<9 : return('') #not a full year specified  9=only year, 11=dd-mm-yy
      if thisdate.year<0:
          return(str(abs(thisdate.year))+'v Chr')
      else :
          return(str(thisdate.year))
    else :
      return ('')


def get_female_label_form(wditem,lng,male_form):
  female = male_form
  if ('P2521' in wditem.claims):
    for tryclaim in wditem.claims['P2521']:
      if tryclaim.target.language==lng:
        female = tryclaim.target.text
  return (female)
  
def is_female(wditem):
  if genderCLAIM in wditem.claims:
    LNKgender = wditem.claims.get(genderCLAIM)[0].getTarget()
    return (LNKgender.title()==female_genderPROP)
  return(False)
  
def its_a_firstname(lng,repo,wd):
  
  if (is_eenCLAIM in wd.claims):
    for p31 in wd.claims[is_eenCLAIM]:
      title=p31.getTarget().title()
      if (title=='Q3409032'): return('zowel mannelijke als vrouwelijke voornaam','') #both male/female first name
      if (title=='Q11879590'): return('vrouwelijke voornaam','')
      if (title=='Q12308941'): return('mannelijke voornaam','')       

  if ('en' in wd.descriptions):
   if (wd.descriptions['en']==u'female given name'): return('vrouwelijke voornaam','')
   if (wd.descriptions['en']==u'male given name'): return('mannelijke voornaam','')
   
  if ('de' in wd.descriptions):
   if (wd.descriptions['de']==u'weiblicher Vorname'): return('vrouwelijke voornaam','')
   if (wd.descriptions['de']==u'männlicher Vorname'): return('mannelijke voornaam','')
   
  if ('fr' in wd.descriptions): 
   if (wd.descriptions['fr'] ==u'prénom féminin'): return('vrouwelijke voornaam','')
   if (wd.descriptions['fr'] ==u'prénom masculin'): return('mannelijke voornaam','')
   if (wd.descriptions['fr'] ==u'prénom épicène'): return('zowel mannelijke als vrouwelijke voornaam','')

  if ('pl' in wd.descriptions): 
   if (wd.descriptions['pl'] ==u'imię żeńskie'): return('vrouwelijke voornaam','')
   if (wd.descriptions['pl'] ==u'imię męskie'): return('mannelijke voornaam','')
   if (wd.descriptions['pl'] ==u'xxx'): return('zowel mannelijke als vrouwelijke voornaam','')
   
  if ('it' in wd.descriptions): 
   if (wd.descriptions['it'] ==u'prenome femminile'): return('vrouwelijke voornaam','')
   if (wd.descriptions['it'] ==u'prenome maschile'): return('mannelijke voornaam','')
   if (wd.descriptions['it'] ==u'xxx'): return('zowel mannelijke als vrouwelijke voornaam','')

  if ('hy' in wd.descriptions): 
   if (wd.descriptions['hy'] ==u'իգական անձնանուն'): return('vrouwelijke voornaam','')
   if (wd.descriptions['hy'] ==u'արական անձնանուն'): return('mannelijke voornaam','')
   if (wd.descriptions['hy'] ==u'xxx'): return('zowel mannelijke als vrouwelijke voornaam','')

  if ('nb' in wd.descriptions): 
   if (wd.descriptions['nb'] ==u'kvinnenavn'): return('vrouwelijke voornaam','')
   if (wd.descriptions['nb'] ==u'mannlig fornavn'): return('mannelijke voornaam','')
   if (wd.descriptions['nb'] ==u'xxx'): return('zowel mannelijke als vrouwelijke voornaam','')
  
  return ('voornaam','')
  
def wd_sparql_query(spq):
  wikidatasite=pywikibot.Site('wikidata','wikidata') 
  generator=pg.WikidataSPARQLPageGenerator(spq,site=wikidatasite)
  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect=True)
      yield wd
  
def wd_from_file(usefilename):
  repo=pywikibot.Site('wikidata','wikidata').data_repository()
  csvfile=open(usefilename,'r')
  for alllines in csvfile:
    qitem=alllines[alllines.find('Q'):alllines.find(',')]
    if (len(qitem)>0):
      try:
        wditem=pywikibot.ItemPage(repo,qitem)
        wditem.get(get_redirect=True)
        yield wditem
      except:
        pass  

def wd_user_edits(username,ucsite,totaledits):
  repo=pywikibot.Site('wikidata','wikidata').data_repository()
  useredits=pg.UserContributionsGenerator(username,site=ucsite,total=totaledits,namespaces=[0])      
  for oneedit in useredits:
    oneedit.get(get_redirect=True)
    if (oneedit.exists()):
      wd=pywikibot.ItemPage(repo,oneedit.title())
      wd.get(get_redirect=True)
      if (wd.exists()):
        yield wd
  
  
"""
For a person, we take the occupation and country of citizenship, e.g. "association football player from Germany", 'presentator from Italy', "accountant from the United States", 'politician from Ukraine', etc
"""             

def check_scientist(lng,WDIperson,missing):
    my_description=''
    
    if ('P496' in WDIperson.claims):
      my_description=scientist[lng]
      missing=''
    #print(f'xxx: {my_description}––{missing}')
    return(my_description,missing)

def its_a_person(lng, repo, WDIperson):
    missing = u'' 
    update_desc = False
    if lng in WDIperson.descriptions:
       update_desc = (WDIperson.descriptions[lng].lower() in ['','person','persoon','sporter','politicus','politica','mens']) or \
                     (WDIperson.descriptions[lng].lower().find('n/a') > 0) or \
                     (WDIperson.descriptions[lng].lower().find('sporter') > 0) or \
                     (WDIperson.descriptions[lng].lower().find('dramaturgino') > 0) or \
                     (WDIperson.descriptions[lng].lower().find('scenografino') > 0) or \
                     (WDIperson.descriptions[lng].find('(-)')>0) 

    LNKinstance_of = WDIperson.claims.get(is_eenCLAIM)[0].getTarget()
    if not(LNKinstance_of is None): 
      WDIinstance =  pywikibot.ItemPage(repo,LNKinstance_of.title())
      WDIinstance.get(get_redirect=True)
      prnInstance=get_lng_label(lng,WDIinstance)
    else :
      prnInstance = u'1 n/a: '+WDIperson.title()+' '
      return(check_scientist(lng,WDIperson,txt2skip))

    prnOccupation = u'2 n/a '
    if beroepCLAIM in WDIperson.claims:   #beroep
        LNKoccupation = WDIperson.claims.get(beroepCLAIM)[0].getTarget()
        try :
          WDIoccupation = pywikibot.ItemPage(repo,LNKoccupation.title())
          WDIoccupation.get(get_redirect=True)
          if (lng in WDIoccupation.labels) : 
            if (is_female(WDIperson)):
              prnOccupation = get_female_label_form(WDIoccupation,lng,WDIoccupation.labels[lng])
            else:
              prnOccupation = WDIoccupation.labels[lng]
          else : 
            prnOccupation = u'3 n/a'
            missing = txt2skip
        except :
          missing = WDIperson.title()
          prnOccupation = u'4 n/a'
          print("Except :-(")
    else :
      return(check_scientist(lng,WDIperson,txt2skip))

    if 'P27' in WDIperson.claims:  #country of origin
        prnCountry = u'n/a = '
        LNKcountry = WDIperson.claims.get('P27')[0].getTarget()
        try :
          WDIcountry = pywikibot.ItemPage(repo,LNKcountry.title())
          WDIcountry.get(get_redirect=True)
          if (lng in WDIcountry.labels): 
            prnCountry = WDIcountry.labels[lng]
          else : 
            missing = WDIcountry.title()
        except :
          missing = WDIperson.title()
    else :
      return(check_scientist(lng,WDIperson,txt2skip)) 

    geboortejaarstr = '?'
    if (geborenCLAIM in WDIperson.claims):
      geboortejaarstr=make_yeardatestr(WDIperson.claims.get(geborenCLAIM)[0].getTarget())    
    
    if (gestorvenCLAIM in WDIperson.claims):
      sterfdatum = WDIperson.claims.get(gestorvenCLAIM)[0].getTarget()
      if not(sterfdatum is None): 
        levenjaarstr = ' ('+geboortejaarstr+'-'+make_yeardatestr(sterfdatum)+')'
      else:
        levenjaarstr = ' ('+geboortejaarstr+'-?)'
    else:
      geboortejaarstr=''
      levenjaarstr=''

    my_description = nameofcitizenship(prnCountry,prnOccupation)+levenjaarstr
    if (my_description==''):
      if 'P496' in wd.claims: #ORCID-id
        my_description='onderzoeker'
        missing=''
      return(check_scientist(lng,WDIperson,txt2skip))
    return(my_description,missing)

def its_a_generalthing(lng,repo,wditem,shortstr,longdescrstr,myclaim,MultiLng,force):
  if (lng in wditem.descriptions) and (not force):
    if (get_lng_description(lng,wditem)!=shortstr):
      return('',txt2skip)
  claimstr=''
  try:
    if (myclaim in wditem.claims):
      LNKitem=wditem.claims.get(myclaim)[0].getTarget()
      if not (LNKitem is None):
        WDIitem = pywikibot.ItemPage(repo,LNKitem.title())
        WDIitem.get(get_redirect=True)
        if MultiLng: 
          claimstr,skipper=get_label(lng,WDIitem)
        else:
          claimstr=get_lng_label(lng,WDIitem)
        #claimstr=get_lng_label(lng,WDIitem)
        #if lng in WDIitem.labels:
        #  claimstr=WDIitem.labels[lng]
        #elif MultiLng:
        #  for trylng in lng_canbeused:
        #    if (claimstr=='') and (trylng in WDIitem.labels):
        #       claimstr = WDIitem.labels[trylng]
  except:
    pass
  if claimstr=='':
    return(shortstr,'')
  else:
    return(('%s %s' % (longdescrstr,claimstr)),'')

def it_was_a_generalthing(lng,repo,wditem,shortstr,longdescrstr,myclaim,oneLng):
  claimstr=u''
  try:
    if oneLng:
      if (myclaim in wditem.claims):
        LNKitem=wditem.claims.get(myclaim)[0].getTarget()
        if not (LNKitem is None):
          WDIitem = pywikibot.ItemPage(repo,LNKitem.title())
          WDIitem.get(get_redirect=True)
          if lng in WDIitem.labels:
            claimstr=WDIitem.labels[lng]
          else:
            for trylng in lng_canbeused:
              if (claimstr=='') and (trylng in WDIitem.labels):
                 claimstr = WDIitem.labels[trylng]
    else:
      claimstr,missing=get_label(lng,wditem)
  except:
    pass
    
  if claimstr=='':
    return(shortstr,'')
  else:
    return(('%s%s' % (longdescrstr,claimstr)),'')

def get_label_txt(lng,repo,wdi,property,array=0,fallback=False):
  try:
   if property in wdi.claims:
    if (len(wdi.claims[property])>array):
     lnkProperty=wdi.claims.get(property)[array].getTarget()
     if not (lnkProperty is None):
      propwdi=pywikibot.ItemPage(repo,lnkProperty.title())
      propwdi.get(get_redirect=True)
      if (propwdi.exists()):
       if (lng in propwdi.labels):
        return(propwdi.labels[lng])
       elif (fallback):
         for fallbacklng in lng_canbeused:
           if fallbacklng in propwdi.labels:
             return(propwdi.labels[fallbacklng])
  except:
    print('get_label failed')
  return('')

def its_a_headquarted_thing(lng,repo,wdi,thing):
  where=get_label_txt(lng,repo,wdi,'P159',fallback=True)
  if (where!=''):
    return(f'{thing} {where}','')
  else:
    return('',wdi.title())

def its_something_in_an_entity(lng,repo,wdi,something):
  prnEntity = ''
  prnCountry = ''

  if (gelegen_inCLAIM in wdi.claims):
    try:
      LNKentity = wdi.claims.get(gelegen_inCLAIM)[0].getTarget()
      WDIentity = pywikibot.ItemPage(repo,LNKentity.title())
      WDIentity.get(get_redirect=True)
      if (lng in WDIentity.labels):
        prnEntity = WDIentity.labels[lng]
      else:
        return('',txt2skip)
    except :
      missing = wdi.title()

  if countryCLAIM in wdi.claims:  
    try :
      LNKcountry = wdi.claims.get(countryCLAIM)[0].getTarget()
      if (LNKcountry!=None):
       WDIcountry = pywikibot.ItemPage(repo,LNKcountry.title())
       WDIcountry.get(get_redirect=True)
       if (lng in WDIcountry.labels): 
        prnCountry = WDIcountry.labels[lng]
       else : 
        prnCountry = u''
        missing = WDIcountry.title()
    except :
      missing = wdi.title()
    
  else:
    if (prnEntity!=''): #no country in item, take from P131
      if (countryCLAIM in WDIentity.claims):
        print(f'xxx: {WDIentity.title()}')
        LNKcountry = WDIentity.claims.get(countryCLAIM)[0].getTarget()
        if (LNKcountry != None):
          WDIcountry = pywikibot.ItemPage(repo,LNKcountry.title())
          WDIcountry.get(get_redirect=True)
          prnCountry = get_lng_label(lng,WDIcountry);
    else:
      return('',txt2skip)

  if (prnCountry!='') and (prnEntity!=''):
    return('%s %s, %s' % (something, prnEntity, prnCountry),'')  
  elif (prnCountry!=''):
    return('%s %s' % (something, prnCountry),'')
  elif (prnEntity!=''):
    return('%s %s' % (something, prnEntity),'')
  else:
    return('',txt2skip)  

    
def its_something_in_a_country(lng,repo,wdi,something,skipiffilled):
    prnCountry = u'unknown'
    if (skipiffilled):
     if (lng in wdi.descriptions):
      if (get_lng_description(lng,wdi) != ''):
        return(get_lng_description(lng,wdi),txt2skip)
    missing = u''
    if countryCLAIM in wdi.claims:  
      LNKcountry = wdi.claims.get(countryCLAIM)[0].getTarget()
      try :
        WDIcountry = pywikibot.ItemPage(repo,LNKcountry.title())
        WDIcountry.get(get_redirect=True)
        if (lng in WDIcountry.labels): 
          prnCountry = WDIcountry.labels[lng]
        else : 
          prnCountry = u'n/a = '
          missing = WDIcountry.title()
      except :
        missing = wdi.title()
    elif 'P495' in wdi.claims :
      LNKcountry = wdi.claims.get('P495')[0].getTarget()
      try :
        WDIcountry = pywikibot.ItemPage(repo,LNKcountry.title())
        WDIcountry.get(get_redirect=True)
        if (lng in WDIcountry.labels): 
          prnCountry = WDIcountry.labels[lng]
        else : 
          prnCountry = u'n/a = '
          missing = WDIcountry.title()
      except :
        missing = wdi.title()
    else:
      return('' ,txt2skip) 
    return(something.strip()+ ' '+prnCountry,missing)      
        
def its_canton_of_France(lng,repo,wdi):
  current_desc = ''
  missing = ''
  my_description = 'kanton in Frankrijk'
  current_desc = get_lng_description(lng,wdi)
  if (current_desc==''): 
    if gelegen_inCLAIM in wdi.claims:
      LNKcommunity = wdi.claims.get(gelegen_inCLAIM)[0].getTarget()
      WDIcommunity = pywikibot.ItemPage(repo,LNKcommunity.title())
      WDIcommunity.get(get_redirect=True)
      if lng in WDIcommunity.labels:
        my_description = 'kanton in '+WDIcommunity.labels[lng]+', Frankrijk'
  else:
    missing = txt2skip  
  return(my_description,missing)
        
def its_a_mountain(lng,repo,wdi):
    return(its_something_in_a_country(lng,repo,wdi,'berg in',True))      
      
def its_disambigue(lng,repo,wdi):
  if (lng in wdi.descriptions) or (len(wdi.claims)>1):   #there is already a description, skip this one
    return('',txt2skip)
  return('Wikimedia-doorverwijspagina','')      #use default description

def its_a_thing_located_in_country(lng,repo,wditem,countryname, thing):
    if (gelegen_inCLAIM in wditem.claims):
      LNKcommunity = wditem.claims.get(gelegen_inCLAIM)[0].getTarget()
      WDIcommunity = pywikibot.ItemPage(repo,LNKcommunity.title())
      WDIcommunity.get(get_redirect=True)
      
      if (lng in WDIcommunity.labels):
        return(thing+u' in '+WDIcommunity.labels[lng]+u', '+countryname, '')     
      else:
        return(thing+u' in '+countryname, WDIcommunity.title())
    else:
      return(thing+u' in '+countryname,wditem.title())

def its_a_publication(lng,repo,wditem):
  over=uitgever=missing=datumstr=''
  if ('P921' in wditem.claims):
    over,missing=its_a_generalthing(lng,repo,wditem,'', 'over', 'P921',True,False)
  if ('P123' in wditem.claims):
    uitgever,missing=its_a_generalthing(lng,repo,wditem,'','van uitgever','P123',True,False)
  if ('P577' in wditem.claims):
    datumstr,missing='',''
  return('publicatie',missing)  

def its_an_episode(lng, repo, wditem):
  if 'P179' in wditem.claims: #serie
    LNKseries = wditem.claims.get('P179')[0].getTarget()
    WDIseries = pywikibot.ItemPage(repo,LNKseries.title())
    WDIseries.get(get_redirect=True)
    
    serienaam,missing=get_label(lng,WDIseries)
    if (serienaam=='') or (missing==txt2skip):
      return('aflevering van '+WDIseries.title(), txt2skip)
    else :
      return('aflevering van ' + serienaam,'')
      
  else:
    return('',txt2skip)
    
def its_a_list(lng,repo,wditem):
  return('Wikimedia-lijst','')
    
def its_a_town(lng,repo,wditem):
  return its_something_in_a_country(lng,repo,wditem,'stad in',True)  
  
def its_a_football_club(lng, repo, wditem):
  return(its_something_in_a_country(lng,repo,wditem,'voetbalclub uit',True))

def its_a_football_team(lng, repo, wditem):
  return(its_something_in_a_country(lng,repo,wditem,'voetbalteam uit',True))  

def its_a_band(lng,repo,wditem):
    missing = u''
    return its_something_in_a_country(lng,repo,wditem,'muziekgroep uit',True)

def its_a_tvseries(lng,repo,wditem):
  return(its_something_in_a_country(lng,repo,wditem,'televisieserie uit',True))

def its_a_tvprogram(lng,repo,wditem):
  #return(get_lng_description(lng,wditem),txt2skip)
  if (countryCLAIM in wditem.claims):
    return(its_something_in_a_country(lng,repo,wditem,'televisieprogramma uit',True))
  else:
    return('televisieprogramma','')

def its_a_musicalbum(lng,repo,wditem):
  #return(get_lng_description(lng,wditem),txt2skip)
  if 'P175' in wditem.claims:
    LNKartist = wditem.claims.get('P175')[0].getTarget()
    WDIartist=pywikibot.ItemPage(repo,LNKartist.title())
    WDIartist.get(get_redirect=True)
    if (lng in WDIartist.labels):
      return('muziekalbum van '+WDIartist.labels[lng],'')
  
  return('muziekalbum','')
  
  
def its_a_book(lng,repo,wditem):
  if (get_lng_description(lng,wditem) in ['','boek']):
    return its_a_generalthing(lng,repo,wditem,'boek','boek van','P50',True,False)
  return('',txt2skip)


def its_a_nummer(lng,repo,wditem):
  if not(get_lng_description(lng,wditem) in [u'nummer','single','lied','']):
    return('',txt2skip)
  return its_a_generalthing(lng,repo,wditem,'nummer','nummer van','P175',True,False)


def its_a_single(lng,repo,wditem):
  if not(get_lng_description(lng,wditem) in [u'single','nummer','lied','']):
    return('',txt2skip)
  return its_a_generalthing(lng,repo,wditem,'single','single van','P175',True,False)

def its_a_carmodel(lng,repo,wditem):  #automodel van P176
  manufacturer = u''
  if(get_lng_description(lng,wditem) not in [u'automodel','']):
    return('',txt2skip)
  return its_a_generalthing(lng,repo,wditem,'automodel','automodel van','P176',True,False)

def its_a_discography(lng,repo,wditem):
  if 'P175' in wditem.claims:
    artistLNK = wditem.claims.get('P175')[0].getTarget()
    if not(artistLNK is None):
      wdArtist=pywikibot.ItemPage(repo,artistLNK.title())
      wdArtist.get(get_redirect=True)
      if lng in wdArtist.labels:
        return ('discografie van '+wdArtist.labels[lng],'')
      else:
        for trylng in lng_canbeused:
          if trylng in wdArtist.labels:
            return('discografie van '+wdArtist.labels[trylng],'')
  return('discografie','')

def its_chemical(lng,repo,wditem):
  return('',txt2skip)  
  
def action_one_P131_item(lng,repo,oneitem):  
   global totaledits

   nld=get_lng_description(lng,oneitem)
   if (lng in oneitem.labels):
     nll = oneitem.labels[lng]      
   else:
     nll = ''
     
   adminname=''
   isaname=''
   countryname=''
   
   if ('P31' in oneitem.claims):
     LNKisa=oneitem.claims.get('P31')[0].getTarget()
     if not LNKisa is None:
       isa=pywikibot.ItemPage(repo,LNKisa.title())
       isa.get(get_redirect=True)
       if lng in isa.labels:
         isaname = isa.labels[lng]
   if (isaname in ['dorp in China']):
      shortname='dorp'
   else:
      shortname=isaname      
        
   if (gelegen_inCLAIM in oneitem.claims):
     LNKadmin=oneitem.claims.get(gelegen_inCLAIM)[0].getTarget()
     if not LNKadmin is None:
       admin=pywikibot.ItemPage(repo,LNKadmin.title())
       admin.get(get_redirect=True)
       if lng in admin.labels:
         adminname = admin.labels[lng]
   if (countryCLAIM in oneitem.claims):
     LNKcountry=oneitem.claims.get(countryCLAIM)[0].getTarget()
     if not LNKcountry is None:
       country=pywikibot.ItemPage(repo,LNKcountry.title())
       country.get(get_redirect=True)
       if lng in country.labels:
         countryname = country.labels[lng]
   data={}
   found=False
   if (not lng in oneitem.labels): 
     for plang in lng_canbeused:
       if (plang in oneitem.labels) and not found:
         data.update({'labels': { lng:oneitem.labels[plang]  }})
         found=True
   
   if (adminname==''):
     newdescription = '%s' % isaname
   else:
     newdescription='%s in %s, %s' % (shortname,adminname,countryname)
   if (isaname!='') and (nld in['','dorp','dorp in China','gemeente','gemeente in China']):
     data.update({'descriptions': { lng: newdescription }})
   try:  
     oneitem.editEntity(data,summary=u'nl-description, [[User:Edoderoobot/Set-nl-description|python code]], logfile on https://goo .gl/BezTim')
     logme(False, '%s|%s|%s|%s|%s|%s|%s',datetime.now().strftime("%Y-%b-%d/%H:%M:%S"),oneitem.title(),lng,newlabel,orig_desc,my_description,placefound)
     totaledits += 1
     return(1)
   except ValueError:
     log_unknown(False, "ValueError occured on %s",oneitem.title())
   except :
     log_unknown(False, "Undefined error occured on %s-[%s]",oneitem.title(),'simpleP131')
     pass
   else :
     pass #print("Else:")
   return(0)

def its_a_sports_season(lng,repo,wditem):
  if ('P641' in wditem.claims):
    LNKsport=wditem.claims.get('P641')[0].getTarget()
    if (not(LNKsport is None)):
      sport=pywikibot.ItemPage(repo,LNKsport.title())
      sport.get(get_redirect=True)
      if (lng in sport.labels):
        return(('sportseizoen van een %scompetitie'%sport.labels[lng]),'')
      else:
        return('sportseizoen van een competitie','')
  return ('sportseizoen van een competitie','')

def its_an_audio_drama(lng,repo,wditem):
  if ('P179' in wditem.claims):
    return its_a_generalthing(lng,repo,wditem,'hoorspel','hoorspel van','P50',True,False)
  if ('P50' in wditem.claims):
    return its_a_generalthing(lng,repo,wditem,'hoorspel','hoorspel van','P50',True,False)
  if ('P495' in wditem.claims):
    return its_a_generalthing(lng,repo,wditem,'hoorspel','hoorspel uit','P495',True,False)
  return('hoorspel','')

def its_a_film(lng,repo,wditem):
  if 'P57' in wditem.claims:
    LNKdirector=wditem.claims.get('P57')[0].getTarget()
    if not(LNKdirector is None):
      LNKdirector=pywikibot.ItemPage(repo,LNKdirector.title())
      LNKdirector.get(get_redirect=True)
      directorname,missing=get_label(lng,LNKdirector)
      if (directorname!=''):
        return('film van %s' % directorname,'')
  return('film','')
  
def its_a_taxon(lng,repo,wditem):
  """
  read P171/mother taxon until taxo-rang/P105 is <Q19970288/no value> -> that mother taxon is the first part (insect/)
  """    
  if 'P171' in wditem.claims:
    mother=get_label(lng,wditem)
    if ('P105' in wditem.claims):
      try:
        if wditem.claims.get('P105')[0].getTarget().title()=='Q6847':
          return(f'taxon, ondersoort van {mother}','')        
      except:
        pass    
  return('taxon','')
  
def its_a_composition(lng, repo, wditem):
  """
  find composer P86
  """  
  if ('P86' in wditem.claims):
    composerLNK = wditem.claims.get('P86')[0].getTarget()
    if not composerLNK is None:
      composer = pywikibot.ItemPage(repo,composerLNK.title())
      composer.get(get_redirect=True)
      if (lng in composer.labels):
        return('compositie van %s' % composer.labels[lng], '')
  return('compositie','')
  
def its_a_tabon_in_thailand(lng,repo,wditem):
  newdescription = ''
  if (gelegen_inCLAIM in wditem.claims):
    LNKtambon=wditem.claims.get(gelegen_inCLAIM)[0].getTarget()
    if not (LNKtambon is None):
      WDitemtambon=pywikibot.ItemPage(repo,LNKtambon.title())
      WDitemtambon.get(get_redirect=True)
      return(get_label(lng,WDitemtambon))
  return(newdescription,'')      

def get_label(lng, wditem):
  if (lng in wditem.labels):
    return (wditem.labels[lng],'')
  if ('en' in wditem.labels):
    return (wditem.labels['en'],'')
  if ('de' in wditem.labels):
    return (wditem.labels['de'],'')
  if ('nl' in wditem.labels):
    return (wditem.labels['nl'],'')
  if ('fr' in wditem.labels):
    return (wditem.labels['fr'],'')
  if ('it' in wditem.labels):
    return (wditem.labels['it'],'')
  if ('es' in wditem.labels):
    return (wditem.labels['es'],'')
  return('',txt2skip)


def get_description(lng, wditem):
  if (lng in wditem.descriptions):
    return (wditem.descriptions[lng],'')
  return('',txt2skip)

def its_a_fictional_character(lng,repo,wditem):
  if ('P1441' in wditem.claims):
    my_description,missing=its_a_generalthing(lng,repo,wditem,'personage','personage uit','P1441',True,False)
  elif ('P1080' in wditem.claims):
    my_description,missing=its_a_generalthing(lng,repo,wditem,'personage','personage uit','P1080',True,False)
  else: 
    my_description='personage'
    missing=''
  return (my_description,missing)

def its_a_computergame(lng, repo, wditem):
  if ('P178' in wditem.claims):
    LNKdeveloper=wditem.claims.get('P178')[0].getTarget()
    if not (LNKdeveloper is None):
      WDitemdeveloper=pywikibot.ItemPage(repo,LNKdeveloper.title())
      WDitemdeveloper.get(get_redirect=True)
      developer_name,missing=get_label(lng,WDitemdeveloper)
      if (developer_name!=''):
        return('computerspel van %s'%developer_name,'')
  if ('P179' in wditem.claims):
    serieLNK=wditem.claims.get('P179')[0].getTarget()
    if not(serieLNK is None):
      WDitemserie=pywikibot.ItemPage(repo,serieLNK.title())
      WDitemserie.get(get_redirect=True)
      seriename,missing=get_label(lng,WDitemserie)
      if (seriename!=''):
        return('computerspel uit de serie %s' % seriename,'')
  return('computerspel','')

def action_one_item(lng, repo, wditem):
    global output2screen
    global items2do
    global totaledits
    
    if (debugedo): print('action-one-item1')
    items_written=items_found=0
    missing = u''
    new_description=u''
    orig_description = get_lng_description(lng,wditem).lower()
    en_description = u''
    en_description = get_lng_description('en',wditem)
    type_of_item=u''
    placefound=''
    force_label=''
    
    items2do -= 1
    
    str1 = '{:>10d}'.format(items2do)
    str2 = '{:>10}'.format(wditem.title())
    
    if commit:
      sys.stdout.write("\r%s%s" % (str1, str2))
    gotP31 = False
    if (is_eenCLAIM in wditem.claims):
      gotP31 = True
      type_id = wditem.claims.get(is_eenCLAIM)[0].getTarget()
      if type_id != None:
        type_of_item = type_id.title()  #we only use the first one, and assume the first one is most relevant
    if (type_of_item!='') :  
      #print('Type: [%s]' % (type_of_item))
      if (False):
        pass #just to have the same structure below
      elif (type_of_item == 'Q5') and ((orig_description in ['','mens','politicus','politica','voetballer','maakster','nederlands maakster','televisiepresentator','nederlands maker','onderzoeker','xxx']) or (orig_description.find('teatrestrino')>-1) or (orig_description.find('hokeistino')>-1)):
        new_description,missing = its_a_person(lng, repo, wditem)
        placefound='person'
      elif type_of_item=='Q4167410': #disambiguation-page
        if (orig_description in ['','dp','doorverwijzing','doorverwijspagina']):
          new_description,missing = its_disambigue(lng,repo,wditem)
        placefound='disamb'
      elif type_of_item=='Q8502': #a mountain
        new_description,missing = its_a_mountain(lng,repo,wditem)
        placefound='mountain'
      elif type_of_item=='Q16521': #it is a taxon
        if (orig_description in ['','']): #old one is blank
          new_description,missing=its_a_taxon(lng,repo,wditem) #fix it to "taxon"
        placefound='taxon'
      elif type_of_item=='Q577': #jaar
        new_description='jaar'
        placefound='jaar'
      elif (type_of_item=='Q515') or (type_of_item=='Q5119') or (type_of_item=='Q1549591') or (type_of_item=='Q3957'):  #stad
        new_description,missing = its_a_town(lng,repo,wditem)
        placefound='town'
      elif type_of_item=='Q747074': #Italian communiity
        new_description,missing = its_a_thing_located_in_country(lng,repo,wditem,u'Italië','dorp')
        placefound='IT-gemeente'
      elif type_of_item=='Q484170': #Franse gemeente 
        new_description,missing = its_a_thing_located_in_country(lng,repo,wditem,u'Frankrijk','gemeente')
        placefound='FR-gemeente'
      elif (type_of_item=='Q262166') or (type_of_item=='Q22865' ): #Duitse gemeente
        new_description,missing = its_a_thing_located_in_country(lng,repo,wditem,u'Duitsland','gemeente')
        placefound='DE-gemeente'
      elif type_of_item=='Q13406463': #wikimedia-lijst
        new_description,missing = its_a_list(lng,repo,wditem)
        placefound='lijst'
      elif type_of_item=='Q476028': #voetbalclub
        new_description,missing=its_a_football_club(lng,repo,wditem)  
        placefound='voetbalCLUB'
      elif type_of_item=='Q15944511': #voetbalteam
        new_description,missing = its_a_football_team(lng,repo,wditem)
        placefound='voetbalteam'
      elif type_of_item=='Q11173':#chemische verbinding
        if (orig_description in ['chemische stof','chemische samenstelling','']):
          new_description = 'chemische verbinding'
        placefound = 'chemische samenstelling'
      elif type_of_item=='Q79529':
        if (orig_description in ['chemische samenstelling','chemische verbinding']):         #was blank, it should be, but better double check
          new_description='chemische stof' #then use default description
        placefound='chemische stof'
      elif type_of_item=='Q5398426': #tv_series
        new_description,missing=its_a_tvseries(lng,repo,wditem)
        placefound='tvserie'
      elif type_of_item=='Q1983062': #aflevering/episode
        new_description,missing=its_an_episode(lng,repo,wditem)
        placefound='episode'
      elif type_of_item=='Q21191270': #aflevering/episode van tv-serie
        new_description,missing=its_an_episode(lng,repo,wditem)
        placefound='tv-episode'
      elif type_of_item=='Q184188': #Frans kanton
        new_description,missing=its_canton_of_France(lng,repo,wditem)
        placefound='Frans kanton'
      elif type_of_item=='Q318': #sterrenstelsel
        if ('nl' in wditem.labels) and ('en' in wditem.labels):
          if (wditem.labels['en'][:len(wditem.labels['nl'])]==wditem.labels['nl']):
            force_label=wditem.labels['en']
        if (orig_description in ['sterrenstelsel','galaxy','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'galaxy','sterrenstelsel in','P59',MultiLanguage,False)
        placefound='galaxy2'
      elif type_of_item=='Q13632': #planetaire nevel
        if (orig_description in ['planetaire nevel','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'planetaire nevel','planetaire nevel in','P59',MultiLanguage,False)
        placefound='planetaire nevel'
      elif type_of_item=='Q2247863': #hardlopende ster 1153690
        if (orig_description in ['hardlopende ster','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'hardlopende ster','hardlopende ster in','P59',MultiLanguage,False)
        placefound='planetaire nevel'
      elif type_of_item=='Q1153690': #lange-periode variabele ster
        if (orig_description in ['lange-periode variabele ster','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'lange-periode variabele ster','lange-periode variabele ster in','P59',MultiLanguage,False)
        placefound='lpvs'
      elif type_of_item=='Q115518': #planetaire nevel
        if (orig_description in ['melkwegstelstel met lage helderheid','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'melkwegstelstel met lage helderheid','melkwegstelstel met lage helderheid in','P59',MultiLanguage,False)
        placefound='planetaire nevel'
      elif type_of_item=='Q67206691': #infraroodbron
        if (orig_description in ['infraroodbron','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'infraroodbron','infraroodbron in','P59',MultiLanguage,False)
        placefound='planetaire nevel'
      elif type_of_item=='Q215380': #muziekband
        if (orig_description in ['band','']):
          new_description,missing = its_a_band(lng,repo,wditem)
        placefound='band'
      elif type_of_item=='Q39367': #hondenras
        if (orig_description in ['hond','']):
          new_description=u'hondenras'
        placefound='hondenras'
      elif type_of_item=='Q34770': #taal
        if (orig_description in ['taal','']):
          new_description='taal'
          placefound='taal'
      elif type_of_item=='Q482994': #muziekalbum
        if (orig_description in ['','muziekalbum','album','cd']):
          new_description,missing=its_a_musicalbum(lng,repo,wditem)
          placefound='muziekalbum'
      elif type_of_item=='Q11266439':
        if (orig_description in ['','template','sjabloon']):
          new_description='Wikimedia-sjabloon'
          placefound='template'
      elif type_of_item=='Q310890':  #monotypiscal taxon
        if (orig_description in ['taxon','']):  
          new_description = 'monotypische taxon'
          placefound='x'
      elif type_of_item=='Q877358': #resolution of the UN
        if (orig_description in ['resolutie','']):
          new_description='resolutie van de Veiligheidsraad van de Verenigde Naties'
          placefound='VN-resolutie'
      elif type_of_item=='Q486972':
        l1=orig_description.find('stad in')
        l2=orig_description.find('plaats in')
        if (orig_description in ['stad','nederzetting','']) or (l1>=0) or (l2>=0):
          wditem.descriptions['nl']=''
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'nederzetting in',False)
        placefound='nederzetting'
      elif type_of_item=='Q14752149':  #amateur football club
        if (orig_description in ['','amateurvoetbalclub']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'amateurvoetbalclub uit',False)
          placefound='amateurvoetbalclub'
      elif type_of_item=='Q43229': #organisation
        if (orig_description in ['organisatie','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,'organisatie uit',False)
          placefound='organisatie'
      elif type_of_item=='Q728937': #railway line
        if (orig_description in ['spoorlijn','']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'spoorlijn in',False)
          placefound='railwayline'
      elif type_of_item=='Q7278': #political party
        if (orig_description in ['politieke partij','']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'politieke partij uit',False)
          placefound='political party'
      elif type_of_item=='Q532':  #dorp in P17
        if (orig_description in ['dorp','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,'dorp in ',False)
          if (new_description in ['d','']):
            new_description = 'dorp'
            missing=''
          placefound='dorp'
      elif type_of_item=='Q46970': #luchtvaartmaatschappij uit P17
        if (orig_description in ['luchtvaartmaatschappij','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,'luchtvaartmaatschappij uit',False)
          placefound='airliner'
      elif type_of_item=='Q15416':   #television program
        if (orig_description in ['televisieprogramma','']):
          new_description,missing = its_a_tvprogram(lng,repo,wditem)
          placefound='televisieprogramma'
      elif ((type_of_item=='Q783794') or (type_of_item=='Q4830453')):
        new_description,missing = its_something_in_a_country(lng,repo,wditem,'bedrijf uit',True)
        placefound='bedrijf'
      elif type_of_item=='Q11424': #film uit P495 (P577)
        if (orig_description in ['','film']):
          new_description,missing=its_a_film(lng,repo,wditem)
          placefound='film'
      elif type_of_item=='Q18340514': #gebeurtenis in jaar
        new_description = 'gebeurtenis in jaar'
        placefound='gebeurtenis'
      elif type_of_item=='Q1539532':
        new_description = 'sportseizoen'
        placefound='sportseizoen'
      elif type_of_item=='Q3305213': #schilderij van P170
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'schilderij','schilderij van ','P170',False)
        if (orig_description in ['schilderij','']) or (prev_desc==orig_description):
          new_description,missing = its_a_generalthing(lng,repo,wditem,'schilderij','schilderij van','P170',MultiLanguage,False)
          placefound='schilderij'

      elif type_of_item=='Q3231690': #automodel van P176
        if (orig_description in ['automodel','']):
          new_description,missing = its_a_carmodel(lng,repo,wditem)
          placefound='automodel'
      elif type_of_item=='Q3192808': #commune in Madagascar
        if (orig_description in ['commune','']):
          new_description='commune in Madagascar'
          placefound='madagascar'
      elif type_of_item=='Q1002697': #periodiek in het genre P136
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'periodiek','periodiek in het genre ','P123',False)
        if (orig_description in ['periodiek','']) or (prev_desc==orig_description):
          new_description,missing = its_a_generalthing(lng,repo,wditem,'periodiek','periodiek over','P641',not MultiLanguage,False)
          placefound='periodiek-sport'
      elif type_of_item=='Q18536594': #sportevenement op de Olympische Spelen
        if (orig_description in ['sportevenement','']):
          new_description = 'sportevenement op de Olympische Spelen'
          placefound='OS-event'
      elif type_of_item=='Q7889':  #computerspel  genre=P136   ontwikkelaar=P178  uitgeverij=P123
        if (orig_description in ['computerspel','']):
          new_description,missing=its_a_computergame(lng,repo,wditem)
          placefound='computerspel'
      elif type_of_item=='Q659103':  #gemeente in P131, Roemenië
        if (orig_description in ['gemeente in Roemenie','gemeente in Roemenië','gemeente','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'gemeente in')
          placefound='Roemenie'
      elif type_of_item=='Q15081032': #historisch motorfietsmerk
        if (orig_description in ['motorfietsmerk','']): 
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'motorfietsmerk uit',False)
          placefound='motorfiets'
      elif type_of_item=='Q178561': #veldslag in #P17
        if (orig_description in ['veldslag','']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'veldslag in',False)
          placefound='veldslag'
      elif type_of_item=='Q618779': #onderscheiding
        if (orig_description in ['onderscheiding','']):
          new_description,missing='onderscheiding',''
          placefound='awardy'
      elif type_of_item=='Q106259': #polder in P131, P17
        if (orig_description in ['polder','']):
          new_description, missing = its_something_in_an_entity(lng,repo,wditem,'polder in')
          placefound='polder'
      elif type_of_item=='Q18127': #platenlabel uit P17
        if (orig_description in ['','']):
          pass
          placefound='recordlabel'
      elif type_of_item=='Q3184121': #gemeente in Brazilië
        if (orig_description in ['gemeente','gemeente in brazilie','gemeente in brazilië','']):
          new_description,missing = its_something_in_an_entity(lng,repo,wditem,'gemeente in')
          placefound='Brazil'
      elif type_of_item=='Q2635894':  #hoorspel uit de serie P179/uit P495
        if (orig_description in ['hoorspel','']):
          new_description,missing=its_an_audio_drama(lng,repo,wditem)
          placefound='hoorspel'
      elif type_of_item=='Q523':  #ster uit het sterrenbeeld P59
        if (orig_description in ['','ster']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'ster','ster in','P59',MultiLanguage,False)
          placefound='ster'
      elif type_of_item=='Q197': #vliegtuig van P176
        if (orig_description in ['','vliegtuig']):
          new_description,missing='vliegtuig',''
          placefound='plane'
      elif type_of_item=='Q847017': #sportvereniging uit P17
        if (orig_description in ['','']):
          pass
          placefound='x'
      elif type_of_item=='Q2590631': #gemeente in Hongarije
        if (orig_description in ['','']):
          new_description = u'gemeente in Hongarije'
          placefound='hungary'
      elif type_of_item=='Q3024240': #historisch land in P30
        if (orig_description in ['','']):
          new_description = u'historisch land'
          placefound='histland'
      elif type_of_item=='Q253019':
        if (orig_description in ['','ortsteil','plaats in duitsland']):
          new_description, missing =its_a_thing_located_in_country(lng,repo,wditem,'Duitsland', 'ortsteil')
          placefound='ortsteil';
      elif type_of_item=='Q41710': #etniciteit
        if (orig_description in ['','']):
          new_description = u'etnische groep'
          placefound='etnic'
      elif type_of_item=='Q11446':  #schip
        if (orig_description in ['','']):
          new_description = u'schip'
          placefound='schip'
      elif type_of_item=='Q180684': #conflict
        if (orig_description in ['conflict','']):
          its_something_in_a_country(lng,repo,wditem,'conflict in',False)
          placefound='conflict'
      elif type_of_item=='Q5153359': #cz gemeente
        if (orig_description in ['','']):
          new_description = u'gemeente in Tsjechië'
          placefound='CZ-gemeente'
      elif type_of_item=='Q1131296': #portugese bestuurslaag, fregusia
        if (orig_description in ['','']):
          new_description = u'freguesia in Portugal'
          placefound='fregusia'
      elif type_of_item=='Q123705':  #wijk in P131, P17
        if (orig_description in ['','wijk']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'wijk in')
          placefound='wijk'
      elif type_of_item=='Q14659': #heraldisch wapen uit P17
        if (orig_description in ['heraldisch wapen','']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'wapen uit ',True)
          placefound='heraldiek'
      elif type_of_item=='Q2831984': #stripalbum uit de serie P179
        if (orig_description in ['','stripalbum']):
          new_description,missing = its_a_generalthing(lng,repo,wditem,'stripalbum','stripalbum van','P179',MultiLanguage,False)
          placefound='strip'
      elif type_of_item=='Q207628': #compositie van P86
        if (orig_description in ['compositie','']):
          new_description,missing = its_a_composition(lng,repo,wditem)
          placefound='compositie'
      elif type_of_item=='Q95074':  #personage uit P1080
        if (orig_description in ['personage','']):
          new_description,missing=its_a_fictional_character(lng,repo,wditem);
          placefound='personage'
      elif type_of_item=='Q42032':  #ccTLD top level domain van P17
        if (orig_description in ['top level domain','toplevel domain','']):
          pass
          placefound='ccTLD'
      elif type_of_item=='Q106658':  #Landkreis in P131
        if (orig_description in ['landkreis','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'Landkreis in')
          placefound='landkreis'
      elif type_of_item=='Q571': #boek van P50
        if (orig_description in ['','boek','book']):
          new_description,missing = its_a_book(lng,repo,wditem)
          placefound='boek'
      elif type_of_item=='Q134556':  #single van P175
        if (orig_description in ['','single','nummer','plaat']):
          new_description,missing = its_a_single(lng,repo,wditem)
          placefound='single'
      elif type_of_item=='Q7302866':  #single van P175
        if (orig_description in ['','single','nummer','plaat']):
          new_description,missing = its_a_nummer(lng,repo,wditem)
          placefound='nummer'
      elif type_of_item=='Q2912397': #eendagswielerwedstrijd in P17
        if (orig_description in ['eendaagse wielerwedstrijd','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,'eendaagse wielerwedstrijd in ',True)
          placefound='1dagswielerkoers'
      elif type_of_item=='Q355304': #watergang
        if (orig_description in ['','watergang']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,u'watergang in ',True)
          placefound='watergang'
      elif type_of_item=='Q34763': #schiereiland
        if (orig_description in ['schiereiland','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,u'schiereiland in ',True)
          placefound='schiereiland'
      elif type_of_item=='Q23442':
        if (orig_description in ['eiland','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,u'eiland in ',True)
          placefound='eiland'
      elif type_of_item=='Q16970': #kerkgebouw
        if (orig_description in ['kerkgebouw','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,u'kerkgebouw in ',True)
          placefound='kerkgebouw'
      elif type_of_item=='Q23925393': #douar
        if (orig_description in ['douar','']):    
          new_description,missing = its_something_in_a_country(lng,repo,wditem,'douar in',True)
          placefound='douar'
      elif type_of_item=='Q165':
        if (orig_description in ['zee','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,u'zee in ',True)
          placefound='zee'
      elif type_of_item=='Q102496':
        if (orig_description in ['parochie','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,u'parochie in ',True)
          placefound='parochie'
      elif type_of_item=='Q9842':
        if (orig_description in ['basisschool','basisschool in italië','']):
          new_description,missing = its_something_in_an_entity(lng,repo,wditem,u'basisschool in ')
          placefound='basisschool'
      elif type_of_item=='Q3914':
        if (orig_description in ['school','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,u'school in ',True)
          placefound='school'
      elif type_of_item=='Q273057': #discografie   
        if (orig_description in ['','discografie']):
          new_description,missing = its_a_discography(lng,repo,wditem)
          placefound='discografie'
      elif type_of_item=='Q3966183': #Pokémonwezen 
        if (orig_description in [u'Pokemonwezen',u'Pokémon-wezen','Pokemon',u'Pokémon','']):
          new_description = u'Pokémonwezen'
          missing = ''
          placefound='Pokemonwezen'
      elif type_of_item=='Q5633421': #wetenschappelijk tijdschrift
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'wetenschappelijk tijdschrift','wetenschappelijk tijdschrift van ','P123',False)
        if (orig_description in ['','tijdschrift','wetenschappelijk tijdschrift']) or (prev_desc==orig_description): 
          new_description,missing = its_a_generalthing(lng,repo,wditem,'wetenschappelijk tijdschrift','wetenschappelijk tijdschrift van','P123',MultiLanguage,False)
          placefound='wetenschappelijk tijdschrift'
      elif type_of_item=='Q202444':
        if (orig_description in ['voornaam','']):
          new_description,missing=its_a_firstname(lng,repo,wditem)
          placefound='voornaam'
      elif type_of_item=='Q101352': #achternaam
        if (orig_description in ['','']):
          new_description='achternaam'
          missing=''
          placefound='achternaam'
      elif type_of_item=='Q24574745':
        if (orig_description in ['','categorie','category']):
          new_description='Commons-categorie'
          missing=''
          placefound='commonscat'
      elif type_of_item=='Q4167836':
        if (orig_description in ['','categorie','category']):
          new_description='Wikimedia-categorie'
          missing=''
          placefound='categorie'
      elif type_of_item=='Q3863': #planetoide
        if (orig_description in ['']):
          new_description=u'planetoïde'
          placefound='planetoide'
      elif type_of_item=='Q13442814':
        if (orig_description in ['artikel','']):
          new_description='wetenschappelijk artikel'
          placefound='wetenschappelijk artikel'
      elif type_of_item=='Q2039348': #Nederlandse gemeente
        if (orig_description in ['gemeente','Nederlandse gemeente','gemeente in Nederland','']):
          pass
          placefound='Nederlandse gemeente'
      elif type_of_item=='Q5864':
        if (orig_description in ['geile dwerg','']):
          new_description = 'gele dwerg'
          placefound='gele dwerg' 
      elif type_of_item=='Q50231':
        if (orig_description in ['bestuurlijk gebied','gebied','']):
          new_description = 'bestuurlijk gebied in China'
          placefound='geo van China'
      elif type_of_item=='Q5084':  #gehucht
        if (orig_description in ['gehucht','']):
          new_description,missing = its_something_in_an_entity(lng,repo,wditem,'gehucht in')
          placefound='gehucht'
      elif type_of_item=='Q55488':
        if (orig_description in ['spoorwegstation','']):
          new_description,missing = its_something_in_an_entity(lng,repo,wditem,'spoorwegstation in')
          placefound='spoorwegstation'
      elif type_of_item=='Q735428':
        if (orig_description in ['gemeente','']):
          new_description,missing = its_something_in_an_entity(lng,repo,wditem,'gemeente in')
          placefound='gemeente in China'
          #print('[%s][%s]'%(my_description,missing))
      elif type_of_item=='Q2526255': # filmregisseur
        if (orig_description in ['filmregisseur','','regisseur']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,'filmregisseur uit',True)
          placefound='filmregisseur'
      elif type_of_item=='Q34442': #weg
        if (orig_description in ['weg','straat','straat in','']):
          new_description,missing= its_something_in_a_country(lng,repo,wditem,'weg in',True)
          placefound = 'weg'
      elif type_of_item=='Q985488':
        if (orig_description in ['bewonersgemeenschap','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,'bewonersgemeenschap in',True)
          placefound='bewonersgemeenschap'
      elif type_of_item=='Q23397':
        if (orig_description in ['meer','']):
          new_description,missing = its_something_in_a_country(lng,repo,wditem,'meer in',True)
          placefound='meer'
      elif type_of_item=='Q2996394':
        if (orig_description in ['x','']):
          new_description = 'biologisch proces'
          placefound='biologisch proces'
      elif type_of_item=='Q14860489':
        if (orig_description in ['y','']):
          new_description = 'moleculaire functie'
          placefound='mol.func'
      elif type_of_item=='Q5058355':
        if (orig_description in ['z','']):
          new_description = 'cellulaire component'
          placefound='cel.comp'
      elif type_of_item=='Q1077097':
        if (orig_description in ['tambon','']):
          its_a_tabon_in_thailand(lng,repo,wditem)
          placefound='tambon'
      elif type_of_item=='Q4592255':
        if (orig_description in ['','']):
          new_description = 'project sub-pagina'
          placefound='pr.sub'
      elif type_of_item=='Q7366': #lied
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'lied','lied van ','P175',False)
        if (orig_description in ['lied','']) or (prev_desc==orig_description):
          new_description,missing = its_a_generalthing(lng,repo,wditem,'lied','lied van','P175',MultiLanguage,False)
          placefound='lied'
      elif type_of_item=='Q21278897':
        if (orig_description in ['','']):
          new_description = 'Wiktionary-doorverwijzing'
          placefound='wikt.redirect'
      elif type_of_item=='Q17329259': #encyclopedisch artikel
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'encyclopedisch artikel','encyclopedisch artikel uit ','P1433',False)
        if (orig_description in ['encyclopedisch artikel','']) or (prev_desc==orig_description):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'encyclopedisch artikel','encyclopedisch artikel uit','P1433',MultiLanguage,False)
          placefound='ency-art'
      elif type_of_item=='Q620615': #mobiele app
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'mobiele app','mobiele app van ','P178',False)
        if (orig_description in ['mobiele app','']) or (prev_desc==orig_description):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'mobiele app','mobiele app van','P178',MultiLanguage,False);
          placefound='x'
      elif type_of_item=='Q1004':
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'stripverhaal','stripverhaal van ','P179',False)
        if (orig_description in ['stripverhaal','']) or (prev_desc==orig_description):
          new_description,missing = its_a_generalthing(lng,repo,wditem,'stripverhaal','stripverhaal van','P179',MultiLanguage,False)
          placefound='stripverhaal'
      elif type_of_item=='Q14406742':
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'stripreeks','stripreeks door ','P50',False)
        if (orig_description in ['stripreeks','']) or (prev_desc==orig_description):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'stripreeks','stripreeks door','P50',MultiLanguage,False)
          placefound='stripreeks'
      elif type_of_item=='Q737498': #academisch tijdschrift
        if (orig_description in ['tijdschrift','']):
          new_description='academisch tijdschrift'
          placefound='academisch tijdschrift'
      elif type_of_item=='Q24764':
        if (orig_description in ['gemeente','']):
          new_description='Filipijnse gemeente'
          placefound='filip-gem'
      elif type_of_item=='Q70208':
        if (orig_description in ['gemeente','']):
          new_description='Zwitserse gemeente'
          placefound='zwits-gem'
      elif type_of_item=='Q127448':
        if (orig_description in ['gemeente','zweedse gemeente']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'Zweedse gemeente in')
          placefound='zwe-gem'
      elif type_of_item=='Q203300':
        if (orig_description in ['gemeente','']):
          new_description='gemeente in Liechtenstein'
          placefound='licht-gem'
      elif type_of_item=='Q54050': 
        if (orig_description in ['','heuvel','heuvel in','heuvel in noorwegen','heuvel in albanie','heuvel in albanië','heuvel in australie','heuvel in australië','heuvel in mexico','heuvel in nederland','heuvel in marokko','heuvel in duitsland',
                          'zuid-afrika','','','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'heuvel in')
          placefound='heuvel'
      elif type_of_item=='Q166735': #broekbos
        if (orig_description in ['broekbos','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'broekbos in')
          placefound='broekbos'
      elif type_of_item=='Q7075':
        if (orig_description in ['bibliotheek','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'bibliotheek in')
          placefound='bieb'
      elif type_of_item=='Q50386450': #opera-personage
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'opera-personage','opera-personage uit ','P1441',False)
        if (orig_description in ['opera-personage','']) or (prev_desc==orig_description):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'opera-personage','opera-personage uit','P1441',MultiLanguage,False)
          placefound='opera-personage'
      elif type_of_item=='Q21014462': #cel lijn
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'cellijn','cellijn van een ','P703',False)
        if (orig_description in ['cellijn','']) or (prev_desc==orig_description):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'cellijn','cellijn van een','P703',MultiLanguage,False)
          placefound='cellijn'
      elif type_of_item=='Q178122':
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'aria','aria van ','P86',False)
        if (orig_description in ['aria','']) or (prev_desc==orig_description):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'aria','aria van','P86',MultiLanguage,False)
          placefound='aria'
      elif type_of_item=='Q3331189':
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'uitgave','uitgave van ','P50',False)
        if (orig_description in ['uitgave','editie','']) or (prev_desc==orig_description):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'uitgave','uitgave van','P50',False,False)
          placefound='uitgave'
      elif type_of_item=='Q1344':
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'opera','opera van ','P86',False)
        if (orig_description in ['opera','']) or (orig_description==prev_desc):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'opera','opera van','P86',MultiLanguage,True)
          placefound='opera'
      elif type_of_item=='Q53764738':
        if (orig_description in ['','']):
          new_description = 'Chinees karakter'
          placefound='chinees karakter'
      elif type_of_item=='Q79007':
        if (orig_description in ['straat','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'straat in')
          placefound='straat'
      elif type_of_item=='Q27020041':
        if (orig_description in ['sportseizoen','sportseizoen van een competitie','']):
          new_description,missing=its_a_sports_season(lng,repo,wditem)
          placefound='sportseizoen'
      elif type_of_item=='Q15991303':
        if (orig_description in ['voetbalcompetitie','']):
          new_description, missing=its_something_in_a_country(lng,repo,wditem,'voetbalcompetitie in',True)
          placefound='voetbalcompetitie'
      elif type_of_item=='Q742421':
        if (orig_description in ['','theatergezelschap']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'theatergezelschap uit',True)
          placefound='theatergezelschap'
      elif type_of_item=='Q4022':
        if (orig_description in ['rivier','']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'rivier in',True)
          placefound='rivier'
      elif type_of_item=='Q12323':
        if (orig_description in ['dam','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'dam in')
          placefound='dam'
      elif type_of_item=='Q30198':
        if (orig_description in ['','uitstekend landdeel','meers','moeras']) or (orig_description[:19]=='uitstekend landdeel'):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'moeras in')
          placefound='uitstekend landdeel'
      elif type_of_item=='Q22698':
        if (orig_description in ['park','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'park in')
          placefound='park'
      elif type_of_item=='Q2042028':
        if (orig_description in ['kloof','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'kloof in')
          placefound='kloof'
      elif type_of_item=='Q131681':
        if (orig_description in ['stuwmeer','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'stuwmeer in')
          placefound='stuwmeer'
      elif type_of_item=='Q4421':
        if (orig_description in ['bos','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'bos in')
          placefound='bos'
      elif type_of_item=='Q953806':
        if (orig_description in ['bushalte','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'bushalte in')
          placefound='bushalte'
      elif type_of_item=='Q751876':
        if (orig_description in ['kasteel','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'kasteel in')
          placefound='kasteel'
      elif type_of_item=='Q4502142':
        if (orig_description in ['visueel kunstwerk','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'visueel kunstwerk','visueel kunstwerk in collectie','P195',MultiLanguage,False)
          placefound='visueel kunstwerk'
      elif type_of_item=='Q732577':
        if (orig_description in ['publicatie','']):
          new_description,missing=its_a_publication(lng,repo,wditem)
          placefound='publicatie'
      elif type_of_item=='Q55659167':
        if (orig_description in ['','natuurlijke waterloop']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'natuurlijke waterloop in',NoCheckFilled)
          placefound='natuurlijke waterloop'
      elif type_of_item=='Q41176':
        if (orig_description in ['gebouw','bouwwerk','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'gebouw in')
          placefound='gebouw'
      elif type_of_item=='Q58034280':
        if (orig_description in ['bijgebouw','bouwwerk','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'bijgebouw in')
          placefound='bijgebouw'
      elif type_of_item=='Q5783996':
        if (orig_description in ['cottage','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'cottage in')
          placefound='cottage'
      elif type_of_item=='Q3947':
        if (orig_description in ['woonhuis','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'woonhuis in')
          placefound='woonhuis'
      elif type_of_item=='Q191067':
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'redactioneel artikel','redactioneel artikel in ','P1433',False)
        if (orig_description in ['redactioneel artikel','']) or (prev_desc==orig_description):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'redactioneel artikel','redactioneel artikel in','P1433',MultiLanguage,True)
          placefound='redactioneel artikel'
      elif type_of_item=='Q13141064':
        if (orig_description in ['','badmintonner','badmintonspeler','']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'badmintonspeler uit',)
          placefound='badmintonspeler'
      elif type_of_item=='Q26703203':
        if (orig_description in ['stolperstein','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'stolperstein in')
          placefound='stolperstein'
      elif type_of_item=='Q8054':
        prev_desc,missing=it_was_a_generalthing(lng,repo,wditem,'proteïne','proteïne in ','P702',False)
        if (orig_description in ['proteine','proteïne','protein','']) or (prev_desc==orig_description):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'proteïne','proteïne in','P703',MultiLanguage,True)
          placefound='proteine'
      elif type_of_item=='Q7187':
        prev_desc=it_was_a_generalthing(lng,repo,wditem,'gen','gen in', 'P703',MultiLanguage)
        if (orig_description in ['gen','']) or (orig_description==prev_desc):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'gen','gen in','P703',MultiLanguage,(orig_description==prev_desc)) #fixing
          if (missing==txt2skip) and (new_description==''): new_description='gen'
          print(f'<{new_description}>[{missing}]---<{prev_desc}>')
          placefound='gen'
        else:
          print(f'{wditem.title()}-{prev_desc}')
      elif type_of_item=='Q30612':
        if (orig_description in ['klinisch onderzoek','']):
          new_description='klinisch onderzoek'
          placefound='klinisch onderzoek'
      elif type_of_item=='Q56436498':
        if (orig_description in ['','dorp in india',' ']):
          new_description,missing = its_something_in_an_entity(lng,repo,wditem,'dorp in')
          if (new_description in ['',' ']):
            new_description='dorp in India'
            missing=''
          placefound='dorp in India'
      elif type_of_item=='Q811979':
        if (orig_description in ['bouwwerk','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'bouwwerk in')
          placefound='bouwwerk'
      elif type_of_item=='Q277338':
        if (orig_description in ['pseudogen','gen','speudogen','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'pseudogen','pseudogen in','P703',MultiLanguage,False)  #P1057 #fixed
          placefound='pseudogen'
      elif type_of_item=='Q126807':
        if (orig_description in ['kleuterschool','school','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'kleuterschool in')
          placefound='kleuterschool'
      elif type_of_item=='Q39614':
        if (orig_description in ['begraafplaats','','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'begraafplaats in')
          placefound='begraafplaats'
      elif type_of_item=='Q14660':
        if (orig_description in ['vlag','']):
          pass
          new_description,missing=its_a_generalthing(lng,repo,wditem,'vlag','vlag van jurisdictie','P1001',MultiLanguage,False)
          placefound='vlag'
      elif type_of_item=='Q6451276':
        if (orig_description in ['CSR-rapport','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'CSR-rapport','CSR-rapport over','P921',MultiLanguage,False)
          placefound='CSR-rapport'
      elif type_of_item=='Q2668072':
        if (orig_description in ['','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'collectie','collectie uit','P195',MultiLanguage,False)
          placefound='collectie'
      elif type_of_item=='Q17633526':
        if (orig_description in ['','']):
          new_description='Wikinews-artikel'
          missing=''
          placefound='wikinews-artikel'
      elif type_of_item=='Q57733494':
        if (orig_description in ['','badmintoernooi']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'badmintontoernooi in',False)
          placefound='badmintontoernooi'
      elif type_of_item=='Q726242':
        if (orig_description in ['','RR Lyrae-ster']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'RR Lyrae-ster','RR Lyrae-ster in sterrenbeeld','P59',MultiLanguage,False)
          placefound='RR Lyrae-ster'
      elif type_of_item=='Q2065704': #tingrett
        if (orig_description in ['','kantongerecht','kantongerecht in noorwegen']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'kantongerecht in',NoCheckFilled)
          placefound='tingrett'
      elif type_of_item=='Q1457376':
        if (orig_description in ['','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'overlappende dubbelster','overlappende dubbelster in sterrenbeeld','P59',MultiLanguage,False)
          placefound='overlappende dubbelster'
      elif type_of_item=='Q1149652':
        if (orig_description in ['','district']):
          new_description='district in India'
          placefound='district in India'
      elif type_of_item=='Q13005188':
        if (orig_description in ['','mandal','mandal in India']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'mandal in')
          placefound='mandal'
      elif type_of_item=='Q19389637':
        if (orig_description in ['biografisch artikel','']) or (orig_description.find('biografisch artikelvan')==0):
          #my_description,missing='biografisch artikel',''
          new_description,missing=its_a_generalthing(lng,repo,wditem,'biografisch artikel','biografisch artikel van','P2093',MultiLanguage,False)
          if (missing!=''):
            new_description,missing=its_a_generalthing(lng,repo,wditem,'biografisch artikel','biografisch artikel uit','P1433',MultiLanguage,False)
          placefound='biografisch artikel'
      elif type_of_item=='Q1931185':
        if (orig_description in ['','']):
          new_description='radiobron'
          placefound='radiobron'
      elif type_of_item=='Q2154519':
        if (orig_description in ['','']):
          new_description='bron van astrofysische röntgenstraling'
          placefound='rontgenbron'
      elif type_of_item=='Q67206701':
        if (orig_description in ['','']):
          new_description='ver-liggend infrarood object'
          placefound='IR-far'
      elif type_of_item=='Q11812394':
        if (orig_description in ['','theaterbedrijf']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'theaterbedrijf in',CheckFilled)
          placefound='theater'
      elif type_of_item=='Q83373':
        if (orig_description in ['quasar','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'quasar','quasar in sterrenbeeld','P59',MultiLanguage,False)
          placefound='quasar'
      elif type_of_item=='Q189004':
        if (orig_description in ['','']):
          new_description='onderwijsinstelling'
          placefound='college'
      elif type_of_item=='Q15917122':
        if (orig_description in ['roterende variabele ster','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'roterende variabele ster','roterende variabele ster in sterrenbeeld','P59',MultiLanguage,False)
          placefound='rot.var.ster'
      elif type_of_item=='Q204194':
        if (orig_description in ['absorptienevel','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'absorptienevel','absorptienevel in sterrenbeeld','P59',MultiLanguage,False)
          placefound='absorptienevel'
      elif type_of_item=='Q71963409':
        if (orig_description in ['compacte groep van sterrenstelsels','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'compacte groep van sterrenstelsels','compacte groep van sterrenstelsels in sterrenbeeld','P59',MultiLanguage,False)
          placefound='compacte groep sterrenstelsels'
      elif type_of_item=='Q66619666':
        if (orig_description in ['rode reuzentak-ster','rode reuzentak-ster in sterrenbeeld']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'rode reuzentak-ster','rode reuzentak-ster in sterrenbeeld','P59',MultiLanguage,False)
          placefound='rode reuzentak-ster'
      elif type_of_item=='Q130019':
        if (orig_description in ['koolstofster','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'koolstofster','koolstofster in sterrenbeeld','P59',MultiLanguage,False)
          placefound='koolstofster'
      elif type_of_item=='Q72802508':
        if (orig_description in ['emissielijn-sterrenstelsel','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'emissielijn-sterrenstelsel','emissielijn-sterrenstelsel in sterrenbeeld','P59',MultiLanguage,False)
          placefound='emissielijn-sterrenstelsel'
      elif type_of_item=='Q1332364':
        if (orig_description in ['roterende ellipsoide ster','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'roterende ellipsoide ster','roterende ellipsoide ster in sterrenbeeld','P59',MultiLanguage,False)
          placefound='rot.ell.ster'
      elif type_of_item=='Q72803622': 
        if (orig_description in ['emissie-lijn-ster','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'emissie-lijn-ster','emissie-lijn-ster in sterrenbeeld','P59',MultiLanguage,False)
          placefound='emissie-lijn-ster'
      elif type_of_item=='Q88965416':
        if (orig_description in ['','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'Zweedse schooleenheid in')
          placefound='se-school'
      elif type_of_item=='Q6243':
        if (orig_description in ['veranderlijke ster','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'veranderlijke ster','veranderlijke ster in sterrenbeeld','P59',MultiLanguage,False)
          placefound='verand.ster'
      elif type_of_item=='Q1690211':
        if (orig_description in ['','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'openbare wasplaats in')
          placefound='openb.waspl'
      elif type_of_item=='Q5358913':
        if (orig_description in ['','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'Japanse basisschool in')
          placefound='jap.bas.sch'
      elif type_of_item=='Q3508250':
        if (orig_description in ['','']):
          new_description,missing=its_a_headquarted_thing(lng,repo,wditem,'syndicat intercommunal in')
          placefound='synd.intercomm'
      elif type_of_item=='Q3508373':
        if (orig_description in ['','']):
          new_description,missing=its_a_headquarted_thing(lng,repo,wditem,'syndicat mixte in')
          placefound='synd.mixte'
      elif type_of_item=='Q272447':
        if (orig_description in ['moleculaire wolk','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'moleculaire wolk','moleculaire wolk in sterrenbeeld','P59',MultiLanguage,False)
          placefound='moleculaire wolk'
      elif type_of_item=='Q204107':
        if (orig_description in ['cluster van sterrenstelsels','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'cluster van sterrenstelsels','cluster van sterrenstelsels in sterrenbeeld','P59',MultiLanguage,False)
          placefound='cluster.v.sterstels'
      elif type_of_item=='Q72803426':
        if (orig_description in ['','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'horizontale tak','horizontale tak in sterrenbeeld','P59',MultiLanguage,False)
          placefound='hor.tak'
      elif type_of_item=='Q12280':
        if (orig_description in ['brug','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'brug in')
          placefound='bridge'
      elif type_of_item=='Q1260524':
        if (orig_description in ['','']):
          new_description='tijd op een dag'
          placefound='time-of-day'
      elif type_of_item=='Q2557101':
        if (orig_description in ['','liner']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'LINER','laag-ioniserend nucleaire stralingslijn-regio in sterrenbeeld','P59',MultiLanguage,False)
          placefound='LINER'
      elif type_of_item=='Q81505329':
        if (orig_description in ['','eiwitfamilie']):
          new_description='eiwitfamilie met een domein'
          placefound='domfamprot'
      elif type_of_item=='Q417841':
        if (orig_description in ['','']):
          new_description='eiwitfamilie'
          placefound='eiwitfam'
      elif type_of_item=='Q569500':
        if (orig_description in ['','wijkgezondheidscentrum']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'wijkgezondheidscentrum in')
          placefound='wgzc'
      elif type_of_item=='Q44559':
        if (orig_description in ['exoplaneet','planeet','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'exoplaneet','exoplaneet in sterrenbeeld','P59',MultiLanguage,False)
          placefound='exoplaneet'
      elif type_of_item=='Q15184295':
        if (orig_description in ['','']):
          new_description='Wikimedia-module'
          placefound='wm-mod'
      elif type_of_item=='Q49008':
        if (orig_description in ['','']):
          new_description='priemgetal'
          placefound='prime'
      elif type_of_item=='Q7930614':
        if (orig_description in ['','']):
          new_description='dorp in Taiwan'
          placefound='dorpTaiwan'
      elif type_of_item=='Q44539': #tempel
        if (orig_description in ['','tempel']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'tempel in')
          placefound='tempel'
      elif type_of_item=='Q47150325':
        if (orig_description in ['','']):
          new_description='datum'
          placefound='datum'
      elif type_of_item=='Q125191':
        if (orig_description in ['','']):
          new_description='foto'
          placefound='foto'
      elif type_of_item=='Q1505023':
        if (orig_description in ['','interpellatie']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'interpellatie','interpellatie in','P1001',MultiLanguage,False)
          placefound='interellatie'
      elif type_of_item=='Q98467717':
        if (orig_description in ['rijksdagprotocol','']):
          new_description='rijksdagprotocol uit Zweden'
          placefound='zrdp'
      elif type_of_item=='Q182832': #concert in P276
        if (orig_description in ['','concert']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'concert','concert in','P276',MultiLanguage,False)
          placefound='concert'
      elif type_of_item=='Q11032':
        if (orig_description in ['','krant']):
          new_description,missing=its_something_in_a_country(lng,repo,wditem,'krant uit',CheckFilled)
          placefound='krant'
      elif type_of_item=='Q235557':
        if (orig_description in ['','']):
          new_description='bestandsformaat'
          placefound='fileformat'
      elif type_of_item=='Q59199015':
        if (orig_description in ['','']):
          new_description='groep van stereo-isomeren'
          placefound='stereoisomeergroep'
      elif type_of_item=='Q2151232':
        if (orig_description in ['','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'Townland in')
          placefound='Irish townland'
      elif type_of_item=='Q96739634':
        if (orig_description in ['','']):
          new_description='motie in de Zweedse rijksdag'
          placefound='midzr'
      elif type_of_item=='Q13433827':
        if (orig_description in ['','']):
          new_description='encyclopedisch artikel'
          placefound='enc-art'
      elif type_of_item=='Q452237':
        if (orig_description in ['','']):
          new_description='motie'
          placefound='motie'
      elif type_of_item=='Q155076':
        if (orig_description in ['','']):
          new_description='rechtspersoon'
          placefound='rechtspersoon'
      elif type_of_item=='Q2116450':
        if (orig_description in ['','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'havezate in')
          placefound='havezate'
      elif type_of_item=='Q820655':
        if (orig_description in ['','']):
          new_description='wet'
          placefound='wet'
      elif type_of_item=='Q106006703':
        if (orig_description in ['','']):
          new_description,missing=its_a_generalthing(lng,repo,wditem,'lokale Chinese wet','lokale Chinese wet in','P1001',True,False)
          placefound='lokchinwet'
      elif type_of_item=='Q6453643':
        if (orig_description in ['','']):
          new_description='wet per decreet'
          placefound='wpd'
      elif type_of_item=='Q97695005':
        if (orig_description in ['','']):
          new_description='comité-motie in de Zweedse rijksdag'
          placefound='cmidzr'
      elif type_of_item=='Q3539870':
        if (orig_description in ['','district']):
          new_description = 'district in Oeganda'
          missing=''
          placefound='dstrctUg'
          #print('Uganda district!')
      elif type_of_item=='Q55678':
        if (orig_description in ['spoorweghalte','station','']):
          new_description,missing=its_something_in_an_entity(lng,repo,wditem,'spoorweghalte in')
          placefound='halte'
      elif type_of_item=='Q':
        if (orig_description in ['','']):
          pass
          placefound='x'
      elif type_of_item=='Q':
        if (orig_description in ['','']):
          pass
          placefound='x'
      elif type_of_item=='Q':
        if (orig_description in ['','']):
          pass
          placefound='x'
      elif type_of_item=='Q':
        if (orig_description in ['','']):
          pass
          placefound='x'
      elif new_description=='':
        #log_unknown(False,'%s|%s|%s',wditem.title(),type_of_item,en_description)
        placefound='unknown: %s' %type_of_item
        if (not commit):
          print('type of item: %s, orig_desc: [%s], new: [%s]' % (type_of_item,orig_description,new_description))

          
          
      
      if (((new_description!='') and (missing!=txt2skip)) or not(lng in wditem.labels) or force_label!='') and (new_description.find('n/a')==-1):  
        newlabel = u''
        try :
          data = {}
          if not (lng in wditem.labels):
            if (type_of_item in update_label_allowed):
              if (lng in wditem.labels):  #use link-name of same lng as label 
                newlabel=wditem.labels[lng]
                data.update({'labels': { lng: newlabel }})
              else:
                for trylng in lng_canbeused:
                  if trylng in wditem.labels: #same lng is not there, use en-wiki instead
                    mylabel = wditem.labels[trylng]
                    if (',' in mylabel):
                      pass #don't use this label, there are unacceptable characters in the label
                    elif ('(' in mylabel) and not(type_of_item in labelSkipBrackets):
                      mylabel = mylabel[0:mylabel.index('(')]
                    data.update({'labels': { lng: mylabel }})
                    newlabel=mylabel #to put in logfile
                    break  #found, leave for-loop
              
          if (new_description!='') and (missing!=txt2skip):
            data.update( {'descriptions': {lng:new_description}} )
          if skiplog:
            if ((new_description=='') and (orig_description=='') and (missing!=txt2skip) and gotP31):
              log_skipped(type_of_item)
          if data!={}:
            items_written += 1
            if commit:
              wditem.editEntity(data,summary=f'nl-description, [[User:Edoderoobot/Set-nl-description|python code]] - {placefound}')
              totaledits+=1
              if (force_label!=''): 
                print(wditem.title())
                print(1110/0)
              #print('Written %d-%s' % (lend(data),data))
              #if (newlabel=='') and (my_description==''):
              #  pass
              #else:
              #  logme(False, '%s|%s|%s|%s|%s|%s|%s',datetime.now().strftime("%Y-%b-%d/%H:%M:%S"),wditem.title(),lng,newlabel,orig_desc,my_description,placefound)
            else:
              print('No commit, item not changed: %s - data=[%s]' % (wditem.title(),data))
        except ValueError:
          print("ValueError occured on %s",wditem.title())
          log_unknown(False, "ValueError occured on %s",wditem.title())
        except :
          print("Undefined error occured on %s-[%s]-<%s>"%(wditem.title(),missing,data))
          log_unknown(False, "Undefined error occured on %s-[%s]-<%s>"%(wditem.title(),missing,data))
          pass
        else :
          pass

        items_found += 1


    return items_found,items_written






def lastXnewpages(maxp):
  print('Begonnen')
  site=pywikibot.Site(run_lng)
  mygenerator=pg.NewpagesPageGenerator(site,0,maxp)
  for onepage in mygenerator:
    if (onepage.exists()): #avoid speedy deleted 
      #print('p:%s' % onepage.title())
      if ('wikibase_item' in onepage.properties()):
       try:
        wd=onepage.data_item()  
        wd.get(get_redirect=True)
        yield(wd)
       except:
        pass
  print('Klaar')

def testrun():  
 global output2screen
 output2screen = True
 repo = pywikibot.Site().data_repository()
 item2get = 'Q92924911' 
 
 x = pywikibot.ItemPage(repo, item2get)
 x.get(get_redirect=True) 
 print('read item')
 if x.exists():
   print('item does exist')
   found,written = action_one_item('nl',repo,x)
   #print('[%s][%s]' % (x.descriptions['nl'],''))
 else:
   print('no action!') 

def wd_one_without_description(item):
  base_sparql = 'SELECT ?item WHERE {?item wdt:P31 wd:%s . OPTIONAL {?item schema:description ?itemdescription filter (lang(?itemdescription) = \"nl\").  } FILTER (!BOUND(?itemdescription))}' 
  one_sparql = base_sparql % item
  for wditem in wd_sparql_query(one_sparql):
    if (wditem.exists()):
      yield wditem

def wd_all_without_description():
  base_sparql = 'SELECT ?item WHERE {?item wdt:P31 wd:%s . OPTIONAL {?item schema:description ?itemdescription filter (lang(?itemdescription) = \"nl\").  } FILTER (!BOUND(?itemdescription))}'
  for item in all_types_list:
    print(f'Next item: {item.title()}')
    for xitem in wd_one_without_description(item):
      yield xitem
    """
    one_sparql = base_sparql % item
    for wditem in wd_sparql_query(one_sparql):
      if (wditem.exists()):
        yield wditem
    """
    
def wd_all_simple_P131():
  for onesimpleitem in simple_set_byP131:
    query = 'select ?item where {?item wdt:P31 wd:%s}' % onesimpleitem
    print('\n\nQuery: %s\n\n' % query)
    for oneitem in wd_sparql_query(query):
      try:
        if oneitem.exists():
          oneitem.get(get_redirect=True)
          yield oneitem
          #action_one_P131_item()
        else:
          print('Else wd-simple: %s' % oneitem.title())        
          pass
      except:
        pass      
  yield u'Q5'
     
     
def wd_all_countries(spq):
  country_query = 'select ?item where {?item wdt:P31 wd:Q6256}'
  country_generator = wd_sparql_query(country_query)
  for wd_country in country_generator:
    spq_with_country = spq % wd_country.title()
    one_country_generator = wd_sparql_query(spq_with_country)
    for item in one_country_generator:
        if (item.exists()):
          item.get(get_redirect=True)
          yield item
 

def sparql_nodescription(sparql):
  return 'select distinct ?item where {{%s}filter (!bound(?itemDescription))}' % sparql  
 
def some_items():
  repo=pywikibot.Site('wikidata','wikidata').data_repository()
  do_these=['Q91524287','Q91524287']  #null edits
  for one_item in do_these:
    wd=pywikibot.ItemPage(repo,one_item)
    wd.get(get_redirect=True)
    if (wd.exists()):
      yield wd

def newest_items(repo,site):
    for item in pg.NewPagesPageGenerator(site):
        break
    startno=int(item.title()[1:])
    for itemno in range(startno,0,-1):
        item=pywikibot.ItemPage(repo,'Q%d'%itemno)
        yield(item)
    
    
def old_generator_last_hour():
    timenow=None
    site=pywikibot.Site('wikidata','wikidata')
    repo=site.data_repository()
    generator=newest_items(repo,site);
    generator=pg.NewpagesPageGenerator(site)
    for item in generator:
      if timenow==None:
        timenow=item.oldest_revision.timestamp
        endtime=timenow-timedelta(1.0/24.0);
        untilltime=endtime-timedelta(0.001);
      if (item.oldest_revision.timestamp > untilltime):
        #print(item.title())
        item=pywikibot.ItemPage(repo,item.title())
        item.get(get_redirect=True)
        if (item.exists()):
          #print(item.title())
          yield item
      else:
        print(f'Klaar: {item.oldest_revision.timestamp}' )
        break

def generator_last_hour(gen=None):
  site=pywikibot.Site('wikidata','wikidata')
  repo=site.data_repository()
  if (gen==None):
    gen=pg.NewpagesPageGenerator(site=site,namespaces=[0],total=1)
  for firstpage in gen:
    item=firstpage
    start=int(firstpage.title()[1:])
    counter=start
  timenow=item.oldest_revision.timestamp
  endtime=timenow-timedelta(1.0/24.0);
  untilltime=endtime-timedelta(0.001);

  while (True):
      if (item.oldest_revision.timestamp > untilltime):
        try:
          item=pywikibot.ItemPage(repo,f'Q{counter}')
          item.get()
          if (item.exists()):
            yield item
        except:
          item=firstpage
        counter=counter-1
      else:
        print(f'Klaar: {item.oldest_revision.timestamp}' )
        break


def gen_double_sparql(Pid,Qid,subPid, subQid):
  subquery='select ?item where {?item wdt:%s wd:%s}' % ('P31',subQid)
  print(subquery)
  for oneID in wd_sparql_query(subquery):
    query='select ?item where {?item wdt:%s wd:%s . ?item wdt:%s wd:%s} ' % (Pid,Qid,subPid,oneID.title())
    print(query)
    for returnID in wd_sparql_query(query):
      yield returnID
 
def main(debug=False):
    maxwrites=1
    print ("main")
    global mailmessage
    pigenerator=None
    
    """
    query = default_query #later, I want to manage this with params
    sparql_query = u'SELECT ?item WHERE {   ?item wdt:P31 wd:Q21191270 .   ?item wdt:P179 ?dummy0 . }'
    sparql_query = u'select ?item where{{select ?item ?itemLabel ?itemDescription WHERE {   ?item wdt:P31 wd:Q21191270 .   ?item wdt:P179 ?dummy0 . {service wikibase:label{bd:serviceParam wikibase:language "nl" . }}}} filter (!bound(?itemDescription))}'
    
    
    #sparql_query=sparql_nodescription(sparql_query)
    sparql_query=u'SELECT ?item WHERE { ?item wdt:P31 wd:Q5 . ?item wdt:P106 ?dummy0 . ?wiki0 <http://schema.org/about> ?item . ?wiki0 <http://schema.org/isPartOf> <https://nl.wikipedia.org/> }'  #claim[31:5] and claim[106] and link[nlwiki]

    sparql_query = u'select * {{SELECT ?item ?itemDescription WHERE {{ ?item wdt:P31 wd:Q4167836 }  service wikibase:label{bd:serviceParam wikibase:language "nl" . }  }}}'

    """
    #query = u'link[nlwiki]'
    #sparql_query = u'SELECT * {{SELECT ?item WHERE { ?wiki0 <http://schema.org/about> ?item . ?wiki0 <http://schema.org/isPartOf> <https://nl.wikipedia.org/> {service wikibase:label{bd:serviceParam wikibase:language "nl" . }}}} filter (!bound(?itemDescription))}   '
    #sparql_query = u'SELECT * {{SELECT ?item WHERE { ?wiki0 <http://schema.org/about> ?item . ?wiki0 <http://schema.org/isPartOf> <https://nl.wikipedia.org/> }} }   '
    """
    query = u'claim[31:8502] and claim[17]'
    sparql_query=u'select * where {{ SELECT ?item  WHERE { ?item wdt:P31 wd:Q8502 . ?item wdt:P17 ?dummy0 {service wikibase:label{bd:serviceParam wikibase:language "nl" . }}}} filter (!bound(?itemDescription))}'
    """

    #sparql_query = u'SELECT ?item WHERE {{SELECT ?item WHERE {hint:Query hint:optimizer "None" .{SELECT ?item WHERE {?item wdt:P31 wd:Q4167836 .} LIMIT 275000}OPTIONAL { ?item schema:description ?itemDescription  }filter (!bound(?itemDescription)) }} SERVICE wikibase:label {  bd:serviceParam wikibase:language "nl" .  }}'
    #sparql_query=sparql_nodescription('select ?item where {?item wdt:P31 wd:Q5633421. OPTIONAL { ?item schema:description ?itemDescription  } }')
    #sparql_query='select ?item where {?item wdt:P31 wd:Q202444 }'
    #sparql_query='select ?item where {?item wdt:P31 wd:Q5633421 }'
    #
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q13442814 .     ?item wdt:P577 ?published .     filter ((?published > "1800-01-01T00:00:00Z"^^xsd:dateTime) && (?published < "2000-01-01T00:00:00Z"^^xsd:dateTime)) }'
    #sparql_query='SELECT ?item WHERE {?item wdt:P27 wd:%s . ?item wdt:P31 wd:Q5 . ?item wdt:P106 ?beroep optional { ?item schema:description ?itemDescription . FILTER(lang(?itemDescription)="nl") } .  FILTER (REGEX(STR(?itemDescription), "n[/]a", "i"))}'
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q207628 . OPTIONAL {?item schema:description ?itemdescription filter (lang(?itemdescription) = \"nl\").  } FILTER (!BOUND(?itemdescription))} '  #church no description
    #sparql_query='select ?item where {?item wdt:P31 wd:Q207628}'
    #sparql_query='select ?item where {?item wdt:P31 wd:Q5 . ?item wdt:P106 ?beroep . ?item wdt:P27 wd:%s . {service wikibase:label{bd:serviceParam wikibase:language "nl" . }} OPTIONAL { ?item schema:description ?d .  FILTER(lang(?d)="nl") } filter (!bound(?d))}'
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q3184121 . ?item wdt:P17 wd:%s}'  #basisschool per land
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q1077097 }'
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q985488}' #bewonersgemeenschap in ?land
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q4830453}' #onderneming
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q21278897}' #doorverwijzing naar wiktionary
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q5084}' #gehucht -> test
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q55488}' #spoorwegstation -> test
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q43229}' #organisatie
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q17329259}' #encyclopedsich artikel
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q207628}' #
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q23397}' #meer 
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q1004 }' #stripverhaal
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q14406742 . }' #stripreeks
    #sparql_query='select ?item where {?item wdt:P31 wd:Q34442 . ?item wdt:P17 ?land}' #weg in land
    #sparql_query='select ?item where {?item wdt:P31 wd:Q273057}' #discografie
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q486972 . ?item wdt:P17 wd:%s}'  #nederzetting per land
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q101352} ' #achternaam
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q7366}' #lied
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q5. ?item wdt:P106 wd:Q2526255}' #filmregisseur
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q15416}' #televisieprogramma
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q134556}' #single
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q3305213}' #3. schilderij
    #sparql_query='SELECT ?item where {?item wdt:P31 wd:Q4167410 . ?item wdt:P17 ?land}' #disambiguation-page
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q1539532}' #sportseizoen -> pass
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q737498}' #academisch tijdschrift
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q166735}' #broekbos
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q54050}' #heuvel
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q253019}' #ortsteil
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q7075}' #bibliotheek

    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q21014462}' #cel lijn 100.000++
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q5 . ?item wdt:P106 wd:Q1028181 . ?item wdt:P27 ?land}'  #kunstschilders geboren in een land
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q178122}'  #aria
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q3331189}' #2d2 #uitgave van P50
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q1344}'     #3d3 #opera van P86

    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q742421}' #theatergezelschap
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q4022}' #rivier
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q180684}' #conflict
    ##sparql_query='select distinct ?item where {?item wdt:P31 wd:Q571 . ?item wdt:P50 ?auteur}' #boek met auteur
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q732577 . ?item wdt:P123 ?itsthere}' #badmintonners
    #sparql_query='select ?item where {  ?item wdt:P31 wd:Q5 .   ?item wdt:P106 wd:Q639669 .   ?item wdt:P27 ?land . }' #zwemmers
    #sparql_query='select ?item where {  ?item wdt:P31 wd:Q5 .   ?item wdt:P106 ?beroep .   ?item wdt:P27 wd:Q183 . }' #belgen met een beroep
    #sparql_query='SELECT ?item WHERE {{select ?constellation where {?constellation wdt:P31 wd:Q8928}}?item wdt:P31 wd:Q318 . ?item wdt:P59 ?constellation }' #galaxy

    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q5783996}' #cottage
    #sparql_query='select ?item where {?item wdt:P31 wd:Q3863}'    #planetoide
    #sparql_query='select ?item where {?item wdt:P31 wd:Q726242}' #LLYR-ster
    #sparql_query='SELECT * { ?item schema:description "onderzoeker"@nl . ?item wdt:P27 wd:%s }'
    #sparql_query='SELECT * { ?item schema:description "tennisser"@nl . ?item wdt:P27 ?land}' #
    #sparql_query='select ?item where {?item wdt:P31 wd:Q5 .  ?item wdt:P106 wd:Q11338576 .  OPTIONAL { ?item schema:description ?d .  FILTER(lang(?d)=\"nl\") } {service wikibase:label {bd:serviceParam wikibase:language \"nl\"}}     FILTER (regex(str(?d),\'ster\')       )}  ' #tenisistino 
    #sparql_query='select ?item where {?item wdt:P31 wd:Q5 . ?item wdt:P106 wd:Q3387717 . OPTIONAL { ?item schema:description ?d .  FILTER(lang(?d)=\"nl\") } {service wikibase:label {bd:serviceParam wikibase:language \"nl\"}}     FILTER (regex(str(?d),\'teatrestrino\')       )} '
    #sparql_query='select ?item ?land where { ?item wdt:P31 wd:Q5. ?item wdt:P106 wd:Q10843263. ?item wdt:P27 ?land.}'
    #sparql_query='SELECT ?item {?item wdt:P31 wd:Q13442814 . OPTIONAL { ?item schema:description ?d . FILTER(lang(?d)="nl") }  FILTER( !BOUND(?d) )} LIMIT 1000'
    #sparql_query=u'SELECT ?item WHERE { ?item wdt:P31 wd:Q5 . ?item wdt:P106 ?dummy0 . ?wiki0 <http://schema.org/about> ?item . ?wiki0 <http://schema.org/isPartOf> <https://nl.wikipedia.org/> {service wikibase:label{bd:serviceParam wikibase:language "nl" . }}}'  #claim[31:5] and claim[106] and link[nlwiki]
    #sparql_query='select ?item where {?item wdt:P496 ?orcid}' #wetenschappers
    #sparql_query='SELECT ?item WHERE {?item wdt:P31 wd:Q5 . ?item wdt:P496 ?orcid . OPTIONAL {?item schema:description ?itemdescription filter (lang(?itemdescription) = \"nl\").  } FILTER (!BOUND(?itemdescription))}'
    #sparql_query='select ?item where {?item wdt:P31 wd:Q83373}' #wm-quasar
    #sparql_query='select ?item where {?item wdt:P31 wd:Q58034280}' #bijgebouw
    #sparql_query='select ?item where {?item wdt:P31 wd:Q11032}' #bijgebouw
    #sparql_query='select ?item ?d where {?item wdt:P31 wd:Q13406463 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' #all lists with no nl-Description
    #sparql_query='select ?item ?d where {?item wdt:P31 wd:Q15416 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' #tv-episodes without description
    #sparql_query='select ?item ?moedertaxon where {?item wdt:P31 wd:Q16521 . ?item wdt:P171 ?moedertaxon . ?item wdt:P105 wd:Q68947  OPTIONAL { ?item schema:description ?d .  FILTER(lang(?d)="nl") }  {service wikibase:label {bd:serviceParam wikibase:language \"nl\"}}   FILTER (str(?d)=\'taxon\')}' #taxon is ondersoort met moedertaxon in P171
    #sparql_query='select ?item where {?item wdt:P31 wd:Q2151232 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}'   #Townland
    #sparql_query='select ?item where {?item wdt:P31 wd:Q13433827 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' 
    #sparql_query='select ?item where {?item wdt:P31 wd:Q452237 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' 
    #sparql_query='select ?item where {?item wdt:P31 wd:Q155076 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' 
    #sparql_query='select ?item where {?item wdt:P31 wd:Q2116450 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' 
 
    #sparql_query='select ?item where {?item wdt:P31 wd:Q820655 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' 
    #sparql_query='select ?item where {?item wdt:P31 wd:Q106006703 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' 
    #sparql_query='select ?item where {?item wdt:P31 wd:Q6453643 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' 
    #sparql_query='select ?item where {?item wdt:P31 wd:Q97695005 optional{?item schema:description ?d . filter(lang(?d)="nl")} filter(!bound(?d))}' 
    #sparql_query='select ?item ?itemDescription where {?item wdt:P31 wd:Q476028 . ?item wdt:P17 ?land . SERVICE wikibase:label { bd:serviceParam wikibase:language "nl" }}'
    #sparql_query='select ?item where {?item wdt:P31 wd:Q55678 }' #districts of spoorweghalte
    sparql_query='select ?item where {?item wdt:P31 wd:Q482994 . ?item wdt:P175 ?artiest}'

    site=pywikibot.Site('wikidata','wikidata')
    repo=site.data_repository()

    items_processed=0

    lng = run_lng
    if debug: print("main-1")


    if (True):
      pigenerator=wd_sparql_query(sparql_query)
      mailmessage=f'query: {sparql_query}\nItems processed: {items_processed}'
      #pigenerator=gen_double_sparql('P31','Q318','P59','Q8928')
      #mailmessage=f'star-with-constellation'
      #pigenerator = wd_from_file('/stack/lijsten.csv')
      #pigenerator = wd_all_countries(sparql_query)
      #pigenerator=wd_one_without_description('Q189004')  #onderwijsinstelling
      #pigenerator=wd_all_without_description()
      #mailmessage='wd_ALL_without_description()'
      #pigenerator = wd_all_simple_P131()
      #pigenerator = wd_user_edits('Edoderoo',site,51111)
      #pigenerator = wd_all_items(1)
      #pigenerator = lastXnewpages(1999999) #max one month of newpages anyways
      pigenerator = wd_all_items(-1)
      mailmessage='ALL from 105xxxxxx..105999999'
      mailmessage='ALL down from 32xxxxxx..29999999'

      #query=mailmessage='all items 82'
      #pigenerator=some_items()
      #mailmessage='some items Q91524287'
    if (edohourly):
       print('Edo last hour edits!')
       pigenerator=generator_last_hour(wd_user_edits('Edoderoo',site,999999))
    if (pigenerator==None) or (forcehourly):
       print('Force hourly script...')
       pigenerator=generator_last_hour()
       mailmessage='hourly'

    if (commit):
      print('Commit')
    else:
      print('No commit modus!')
    totalreads=0
    for wd in pigenerator:
      totalreads+=1
      if prelog: log_premature(wd.title())
      if debug: print('Found: %s' % wd.title())
      thisfound,thisone = action_one_item(run_lng,repo,wd)
      items_processed += thisone
      #if (items_processed>12): break
      #if ((items_processed>maxwrites) and (maxwrites>0)): break


    print(f'Klaar: {items_processed}\nQuery: {sparql_query}')
    if (items_processed>10): sendmail('Run completed!',totalreads,items_processed);  #often runs for two weeks ... mail me to notify

def wd_all_items(direction):
 
  startrange=70999999
  stoprange =70000000
  startrange=80999999
  stoprange =80000000

  #startrange= 106999999
  #stoprange=  106000000

  startrange= 32945412 
  stoprange = 30000000 

  repo=pywikibot.Site('wikidata','wikidata').data_repository()
  for itemno in range(startrange,stoprange,direction):
   try:
    wd=pywikibot.ItemPage(repo,'Q%d' % itemno)
    if not wd.isRedirectPage():
     if wd.exists():
      wd.get(get_redirect=True)
      yield wd
    else:
      pass
    itemno -= 1
   except:
     pass

print('Ik loop')
forcehourly=False
edohourly=False
try:
  if (len(sys.argv)>1):
    if (sys.argv[1].lower()=='hourly'):
      forcehourly=True
    elif (sys.argv[1].lower()=='range'):
      pass
    elif (sys.argv[1].lower()=='edo'):
      edohourly=True
    elif (sys.argv[1].lower()=='zzz'):
      pass
    else:
      print(sys.argv[1].lower())
  else:
    print(len(sys.argv))
  if(debugedo):
    print("debug mode: start")
    testrun()
  else :
    main()
finally:
  pywikibot.stopme()
