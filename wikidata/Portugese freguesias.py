import pywikibot
import datetime

def getAmount(wd,claim):
  if claim in wd.claims:
    return wd.claims.get(claim)[0].getTarget().amount
  else:
    return 0

def tmp_gen():
  site=pywikibot.Site('pt')  
  ptlst=['Abraveses','Vila Boa do Mondego']
  for one in ptlst:
    onepage=pywikibot.Page(site,one)   
    yield(onepage)

print(datetime.datetime.now())
useSite='pt'
otherSite='nl'
siteList={'nl':'Lijst van plaatsen in Portugal','pt':'Lista de freguesias de Portugal'}
useTarget='Gebruiker:Edoderoo/Lijst van freguesias in Portugal'
wiki='wiki'
dab_add='_(freguesia)'
pl={}


article_template= '' \
'{{Infobox plaats in Portugal'\
'| land         = Portugal'\
'| naam         = {_naam}'\
'| altnaam      = '\
'| coa          = {_wapen}'\
'| flag         = {_vlag}'\
'| map          = {_map}'\
'| area         = '\
'| subarea      = '\
'| overigniveau = '\
'| provincie    = '\
'| district     = '\
'| inwoners     = {_inwoners}'\
'| census       = '\
'| netnummer    = {_netnummer}'\
'| postcode     = {_postcode}'\
'| tijdzone     = {_tijdzone}'\
'| burgemeester = '\
'| km2          = {_oppervlak}'\
'| hoogte       = '\
'| lat_deg      = {_lat_deg}'\
'| lat_min      = {_lat_min}'\
'| lat_sec      = {_lat_sec}'\
'| lat_dir      = N'\
'| lon_deg      = {_lat_deg}'\
'| lon_min      = {_lat_min}'\
'| lon_sec      = {_lat_sec}'\
'| lon_dir      = W'\
'| image        = {_afbeelding}'\
'| caption      = '\
'| image1       = '\
'| caption1     = '\
'| image2       = '\
'| caption2     = '\
'| image3       = '\
'| caption3     = '\
'| www          = '\
'| website      = {_website}'\
'| portaal2     = '\
'}}'\
'\'\'\'{_Naam}\'\'\' is een freguesia in Portugal'\
'[[Categorie:Gemeente in Portugal]]'


wikistr='{| class="wikitable sortable"\n|-\n!Gemeente!!Wikidata!!taal!!naam!!bij ons!!naam2!!datum opgericht\n'
site=pywikibot.Site(useSite)
page=pywikibot.Page(site,siteList[useSite])
mygenerator=tmp_gen()
mygenerator=page.linkedPages()
for onelink in mygenerator:
 if (onelink.namespace().id==0):  
   art=article_template; 
   begstr=endstr=otherLabelname=otherPagename=gemeentelbl=''
   onepage=pywikibot.Page(site,onelink.title())
   while (onepage.isRedirectPage()):
    onepage=onepage.getRedirectTarget()

   wd=onepage.data_item()
   wd.get(get_redirect=True)

   if (otherSite in wd.labels):
     otherLabelname = wd.labels[otherSite]    
   if (otherSite+'wiki' in wd.sitelinks): 
     otherPagename = wd.sitelinks[otherSite+wiki]
   else:
     otherPagename = wd.sitelinks[useSite+wiki]
     otherPage=pywikibot.Page(pywikibot.Site(otherSite),otherPagename) #should not exist, if it does, add {dab_add} to the name  
     if (otherPage.exists()):
       if (otherLabelname==''):
            otherLabelname=otherPagename
       otherPagename+=dab_add
   if ('P31' in wd.claims):
     myclaims=wd.claims.get('P31')
     for myclaim in myclaims:
        if (myclaim.getTarget().title()=='Q1131296'):
          if ('P580' in myclaim.qualifiers):
            q=myclaim.qualifiers['P580'][0].getTarget()
            if (isinstance(q,pywikibot.WbTime)):
              begstr = ('%d-%d-%d' % (q.day,q.month,q.year))  
          if ('P582' in myclaim.qualifiers):
            q=myclaim.qualifiers['P582'][0].getTarget()
            if (isinstance(q,pywikibot.WbTime)):
              endstr = ('%d-%d-%d' % (q.day,q.month,q.year))
        
   if ('P571' in wd.claims):
        date=wd.claims.get('P571')[0].getTarget()
        begstr=f'{date.day}-{date.month}-{date.year}'
   if ('P131' in wd.claims):  
     gemeenteWD=wd.claims.get('P131')[0].getTarget()
     gemeenteWD.get(get_redirect=True)
     if 'pt' in gemeenteWD.labels: 
       gemeentelbl = gemeenteWD.labels['pt']
   population=getAmount(wd,'P1082')
   if (otherLabelname==otherPagename) or (otherLabelname=='') :
     otherPagestr = f'[[{otherPagename}]]'
   else:
     otherPagestr = f'[[{otherPagename}|{otherLabelname}]]'
   if (len(wd.claims)==0):
     pl['P0'] += 1
   else: 
     for c in wd.claims: #count claims
       if (c in pl):
         pl[c] += 1
       else:
         pl.update({c:1})
        
   wikistr +=f'|-\n|{gemeentelbl}||{wd.title()}||{useSite}||{onelink.title()}||{otherSite}||{otherPagestr}||{begstr}||{endstr}\n'
   #print(art)
wikistr += '|-\n}' 
#pywikibot.Page(pywikibot.Site(otherSite), useTarget).put(wikistr,summary='lijst van pt-wiki') #save page
print(datetime.datetime.now())
print(wikistr)

#for pl_item in sorted(pl.items(), key=operator.itemgetter(1)): 
#  print(pl_item)
