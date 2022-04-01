#20200520-22:40
import pywikibot
from pywikibot import pagegenerators
import mwparserfromhell
from mwparserfromhell.nodes import Template
import datetime
import requests 
import json

useSite='nl'
useCategory={'nl':'Categorie:Tennisser naar nationaliteit'}
useTarget={'nl':'Gebruiker:Edoderoo/Tennis-stats','de':'Benutzer:Edoderoo/Tennis-stats','en':'User:Edoderoo/Tennis-stats'}

intro={'nl':'Deze pagina is automatisch aangemaakt. Wijzig het niet handmatig.','de':'','en':'This page is created automatically by a script. Please do not change it manually.','fr':''}
infobox_title={'nl':'Infobox tennisspeler','de':'Infobox Tennisspieler','en':'Infobox tennis biography','fr':'Infobox Joueur de tennis'}
infobox_singles={'nl':'enkelrecord','de':'einzelbilanz','en':'singlesrecord','fr':''}
infobox_prize={'nl':'prijzengeld', 'de':'preisgeld', 'en':'careerprizemoney', 'fr':'gains en tournois'}
infobox_doubles={'nl':'dubbelrecord','de':'doppelbilanz','en':'doublesrecord','fr':''}
infobox_image={'nl':'afbeelding','de':'bild','en':'image','fr':'image'}
table_start='{| class="wikitable sortable"\n|-\n! Type !! Item !! diff !! country !!link!! Pct !! wd-last-edit !! P180wd !! Instagram !! FamilyName!!1!!2!!3!!4!!5!!6!!7 \n|-'
table_end='\n|}\n'
max_man=150
max_man_zero=10
max_man_dollar=250000
max_woman=1199
max_women_zero=10
max_woman_dollar=15000
#pointintime=datetime.datetime(2020,6,1)
pointintime=datetime.datetime.today()-datetime.timedelta(120)

commonssite=pywikibot.Site('commons','commons')


def getEndPoint(pageid):
    url=f'https://commons.wikimedia.org/wiki/Special:EntityData/M{pageid}.json'
    data=requests.get(url)
    if (data):
      st=json.loads(data.text)
      return(st['entities'])
    return None

def getCommonsStructuredData(pageid):
  endp=getEndPoint(pageid)
  if endp:
    if (f'M{pageid}' in endp):
      retval=endp[f'M{pageid}']
    else:
      return(None)
    if ("statements" in retval):
      return retval["statements"]
    else:
      return None
  return None

def getCommonsProperty(pageid,property):
  comSD=getCommonsStructuredData(pageid)
  if comSD:
    if (property in comSD):
      return comSD[property][0]['mainsnak']['datavalue']['value']['id']
    else:
      return None

def CommonsFileProperty(filename,property):
  site=pywikibot.Site('commons','commons')
  file=pywikibot.Page(site,filename)
  return getCommonsProperty(file.pageid,property)

def smallest(x):
  smallval=x[0]
  for y in x:
    if y<smallval:
      smallval=y
  return smallval

def getCategory(page,text2find=None):
  catfound = None
  for c in page.categories():
    if not(text2find==None):
      if ((c.title().upper().find(text2find.upper())) >= 0):
        catfound = c.title()[10:]
        break
    else: 
      catfound=c.title()[10:] 
      break
  return catfound

def getTemplate(page,template):                #find one template on a page
  wikicode=mwparserfromhell.parse(page.text)     
  templates=wikicode.filter_templates()
  mytemplates = [x for x in templates if x.name.matches(template)]
  if (len(mytemplates)>0):
    for returntemplate in mytemplates:
      yield  returntemplate                    #return template we searched for  

def get_int_from_str(mystr):
  numbers='0123456789'
  ok=numbers+'.,'
  start=0
  while (start<len(mystr)) and (not(mystr[start] in numbers)):
    start+=1
  stop=start
  result=''
  while (stop<len(mystr)) and (mystr[stop] in ok):
    if (mystr[stop] in numbers):
      result+=mystr[stop]
    stop+=1
  if (result==''):
    return 0
  return int(result)

def strip_from_till(mystr, fromstr, tillstr):
  start=mystr.find(fromstr)+len(fromstr)
  end=mystr.find(tillstr)
  if (start<end):
    return mystr[start:end]
  return mystr

def strip_stuff_from_str(mystr):
  mystr=mystr.lower().replace('[[amerikaanse dollar|us$]]','').replace('[[amerikaanse dollar|$]]','')
  mystr=mystr.replace('[[US$]]','')
  mystr=strip_from_till(mystr,'<!--','-->')
  mystr=strip_from_till(mystr,'<ref>','</ref>')
  return mystr.strip()  

def get_values(lng,pagetxt):
  dollars_value=-1
  image_found=False
  for onetemplate in getTemplate(pagetxt,infobox_title[lng]):
    for oneparam in onetemplate.params:
      paramname=oneparam.name.strip().lower()
      if (paramname in [infobox_prize[lng],infobox_singles[lng],infobox_doubles[lng],infobox_image[lng]]):
        thisvalue = strip_stuff_from_str(oneparam.value)
        if (paramname==infobox_image[lng]):
          image_found=image_found or (thisvalue!='')
        if (paramname==infobox_prize[lng]):
          if (thisvalue.find('p2121') != -1): #not in use right now on de-wiki, but let's hope they mature ;-)
            dollars_value=0
          else:
            dollars_value = get_int_from_str(thisvalue)
  return dollars_value, image_found

def find_last_stat_edit(wd):
  for rev in wd.revisions():
    if (rev['comment'].find('P2121')>0) or (rev['comment'].find('P555')>0) or (rev['comment'].find('P564')>0) or (rev['comment'].find('P6104')>0):  
      return rev.timestamp
  return None

def getUICcode_fromPerson(wd):
  if ('P27' in wd.claims):
    con=wd.claims['P27'][0].getTarget()
    con.get(get_redirect=True)
    if ('P2981' in con.claims):
      uic=con.claims['P2981'][0].getTarget()
      return(uic)
    if ('P297' in con.claims):
      iso3166=con.claims['P297'][0].getTarget()
      return(iso3166)
    if ('P298' in con.claims):
      iso3166=con.claims['P298'][0].getTarget()
      return(iso3166)
  return('')

def getCommonsStructuredData(pageid):
  endp=getEndPoint(pageid)  
  if endp:
    if (f'M{pageid}' in endp):
      retval=endp[f'M{pageid}']    
    else:
      return(None)
    if ("statements" in retval):
      return retval["statements"]
    else:
      return None
  return None

def ImageHasP180(filename):
  print(filename)
  commonsfile=pywikibot.Page(commonssite,filename)
  commstructdata=getCommonsStructuredData(commonsfile.pageid)
  if (commstructdata):
    return('P180' in commstructdata)
  return False

def all_from_cat(thissite,thiscat):
 site=pywikibot.Site(thissite)
 cat = pywikibot.Category(site,thiscat)
 gen = pagegenerators.CategorizedPageGenerator(cat,12)
 gen=pagegenerators.PreloadingGenerator(gen)
 wdsite=pywikibot.Site('wikidata','wikidata')
 repo=wdsite.data_repository()
 total_women=found_woman=foundZwoman=total_men=found_man=foundZman=0

 en_site=pywikibot.Site('en','wikipedia')
 de_site=pywikibot.Site('de','wikipedia')
 fr_site=pywikibot.Site('fr','wikipedia')
 print(de_site)
 mantxt=manZtxt=femtxt=femZtxt=''
 manZskipped=womanZskipped=manSkipped=womanSkipped=0
 for src_page in gen:
   if ('wikibase_item' in src_page.properties()):
     man=woman=False
     hasITF2020=''
     srcURL=''
     wd_dd = -1.11
     de_dollars_value=en_dollars_value=fr_dollars_value=0
     de_image=en_image=fr_image=False
     indicator='$'
     wd=src_page.data_item()
     wd.get(get_redirect=True)
     wdLastEdit=find_last_stat_edit(wd)
     if ('P597' in wd.claims):
       total_women+=1
       woman = True
     if ('P536' in wd.claims):
       total_men+=1
       man = True

     if (('P597' in wd.claims) and (found_woman<max_woman)) or (('P536' in wd.claims) and (found_man<max_man)): #skip if not WTA-id or ATP-id defined
       male=female=False
       nlDepicts=wdDepicts=''
       if ('P21' in wd.claims):
         sex=wd.claims.get('P21')[0].getTarget()
         if (sex.title()=='Q6581072'): 
           indicator='$$$'
           female=True
           WTAid=wd.claims.get('P597')[0].getTarget()
           srcURL=f'[https://www.wtatennis.com/players/{WTAid}/name  WTA]'
         if (sex.title()=='Q6581097'): 
           indicator='$$'
           male=True
           ATPid=wd.claims.get('P536')[0].getTarget()
           srcURL=f'[https://www.atptour.com/en/players/-/{ATPid}/overview  ATP]'
       if not('P734' in wd.claims):
         hasITF2020='*';
       if not('P2003' in wd.claims):
         nlDepicts='*';
       if ('P2121' in wd.claims):
         wd_pr=wd.claims.get('P2121')[0].getTarget()
         if (isinstance(wd_pr,pywikibot.WbQuantity)):
           wd_dd = wd_pr.amount
         else:
           wd_dd = -2
       if ('dewiki' in wd.sitelinks):
         de_page=pywikibot.Page(de_site, wd.sitelinks['dewiki'].title)
         de_dollars_value, de_image=get_values('de',de_page)
       nl_dollars_value, nl_image =get_values(useSite,src_page)
       if ('enwiki' in wd.sitelinks):
         en_page=pywikibot.Page(en_site, wd.sitelinks['enwiki'].title)
         en_dollars_value, en_image=get_values('en',en_page)
       if ('frwiki' in wd.sitelinks):
         fr_page=pywikibot.Page(fr_site, wd.sitelinks['frwiki'].title)
         fr_dollars_value, fr_image=get_values('fr',fr_page);
       if (src_page.text.lower().find('[[amerikaanse doll')>0):
         indicator += '!'
       if (not nl_image) and ((de_image) or (en_image) or (('P18') in wd.claims)):
         indicator += 'i'  #other sites might have a useful image

       ax=(wd_dd == -1.11)
       fbx=((not(nl_dollars_value==wd_dd)) and (not(nl_dollars_value>=0)) and(nl_dollars_value!=-1) and (woman))
       mbx=((not(nl_dollars_value==wd_dd)) and (not(nl_dollars_value>=0)) and(nl_dollars_value!=-1) and (man))
       dex=( (((de_dollars_value>(wd_dd+max_woman_dollar)) and woman) or ((de_dollars_value>(wd_dd+max_man_dollar)) and man) ) and (de_dollars_value>0) ) 
       enx=( (((en_dollars_value>(wd_dd+max_woman_dollar)) and woman) or ((en_dollars_value>(wd_dd+max_man_dollar)) and man) ) and (en_dollars_value>0) )
       frx=( (((fr_dollars_value>(wd_dd+max_woman_dollar)) and woman) or ((fr_dollars_value>(wd_dd+max_man_dollar)) and man) ) and (fr_dollars_value>0) )
       dex = dex and (de_dollars_value>0)
       enx = enx and (en_dollars_value>0)
       frx = frx and (fr_dollars_value>0)
       if (wdLastEdit!=None):
         pit=(pointintime>wdLastEdit)
       else:
         pit=True
       if (ax  or fbx or mbx or dex or enx or frx or pit):
         if ('P18' in wd.claims):
           wdDepicts=format(ImageHasP180(wd.claims.get('P18')[0].getTarget().title()))[:1]
           if wdDepicts=='T': wdDepicts='∙'
           if wdDepicts=='F': wdDepicts='■'
         else:
           wdDepicts=''
         diffde=wd_dd-de_dollars_value
         diffen=wd_dd-en_dollars_value
         difffr=wd_dd-fr_dollars_value
         smallval=abs(smallest((diffde,diffen,difffr)))
         try:
           diffpct=round(100*smallval/wd_dd)
         except:
           diffpct=0
         thistxt = f'|-\n|{indicator}||[[:d:{wd.title()}]]||{smallval}||{getUICcode_fromPerson(wd)}||{srcURL}||{diffpct}||{wdLastEdit} || {wdDepicts} || {nlDepicts} || {hasITF2020}||{ax}||{fbx}||{mbx}||{dex}||{enx}||{frx}||{pit} \n'
         if (male):
           if (smallval > 10):
             mantxt += thistxt
             found_man+=1
           else:
            if (foundZman<max_man_zero):
              manZtxt += thistxt
              foundZman+=1
            else:
              manZskipped+=1
         if (female) :
           if (smallval>10):
             femtxt += thistxt
             found_woman+=1
           else:
            if (foundZwoman<max_women_zero):
             femZtxt += thistxt
             foundZwoman+=1
            else:
             womanZskipped+=1
         #print('man: %d – women: %d' % (found_man, found_woman))
         print('%s'%thistxt)
       else:
         #print('\-\n|%s||[[:d:%9s]]||[%9d]||nl||[%9d]||==||{%8d}||/||de||[%9d]||{%8d}\n' %(indicator,wd.title(),wd_dd,nl_dollars_value,wd_dd-nl_dollars_value,de_dollars_value,de_dollars_value-wd_dd))
         pass
     else:
       if ('P536' in wd.claims):
         manSkipped+=1
       if ('P579' in wd.claims):
         womanSkipped+=1


 wikitext = intro[useSite]+'\n\n'+table_start+femtxt+table_end+'\n\n'+table_start+femZtxt+table_end+'\n\n'+table_start+manZtxt+table_end+table_start+mantxt+table_end+'\n\nMan..:%d\nWomen: %d\n\nMan zero: %d, woman zero %d\n\n' % (total_men,total_women,manZskipped,womanZskipped)
 wikitext += 'last edited before: %s-%s-%s' % (pointintime.year,pointintime.month,pointintime.day)
 
 if (True):
   print('%s' % wikitext)
   pywikibot.Page(pywikibot.Site(useSite), useTarget[useSite]).put(wikitext, summary='Update tennis statistics suggestions') #Save page

print('Started') 
all_from_cat(useSite,useCategory[useSite])
print('Finished')
