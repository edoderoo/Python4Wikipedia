#20200427 
#sudo pip install mwviews


from datetime import date,datetime,timedelta
#import datetime
import pywikibot
from mwviews.api import PageviewsClient

hasreftxt='√'
hasnoreftxt=''
skiplist={'nl:Speciaal:Zoeken'}

def hasreferences(articletitle):
  if (articletitle.find(':')>0):
    return(hasreftxt)
  site=pywikibot.Site('nl','wikipedia')
  print('Artikel: [%s]' % (articletitle))
  page=pywikibot.Page(site, articletitle);
  #print(page.text)  
  if (page.text.lower().find('<ref>') > 0):
    return(hasreftxt)
  if (page.text.lower().find('<ref name') > 0):
    return(hasreftxt)
  return(hasnoreftxt)
    
  

def yesterdaysrank(listofranks, article, rankyesterday):
  thisrank = 0
  for onerank in listofranks:
    thisrank += 1
    if article==onerank['article']: 
      if thisrank>rankyesterday:
        return str(thisrank)+u'       ||\u2191||'+str(thisrank-rankyesterday)
      elif thisrank<rankyesterday:
        return str(thisrank)+u'       ||\u2193||'+str(rankyesterday-thisrank)  
      else:
        return (' || ||')
  return u'||=||'
  
  
maxlst = 100 #a short list for now
nrdays=7 #1 week for now
topxxlist = []
debugmodus=True
debugmodus=False
weekdays=['ma','di','wo','do','vr','za','zo']
    
endday = date.today()-timedelta(days=1)
startday = endday - timedelta(days=nrdays)
yesterday = endday-timedelta(days=1)  #to calculate position of day before
mywiki = u'nl.wikipedia'
print(f'Statstics for: {yesterday} -> period {startday}–{endday}')
p = PageviewsClient(mywiki) #initialize
todaystoplist = p.top_articles(mywiki, limit=maxlst)  #get the current topxx of articles

yesterdaystoplist = p.top_articles(mywiki, limit=2*maxlst, year=yesterday.year, month=yesterday.month, day=yesterday.day)

for articles in todaystoplist:
   if debugmodus:
     print (articles['article'])
     probe=p.article_views(mywiki,[articles['article']],start=startday,end=endday)
   topxxlist.append(articles['article'])
topxxtable = p.article_views(mywiki,topxxlist,start=startday,end=endday)

wikistr = ('Onderstaande tabel geeft de statistieken van de meest bezochte artikelen op de Nederlandstalige Wikipedia van %s. \n\n{| class=\"wikitable sortable\"\n|-\n! Positie !! Gisteren !! r !! verschil !! Artikel !! A !! Aantal views op ') % str(endday)

dayloop=endday
while dayloop>=startday:
  wikistr += str(dayloop)+'!!' 
  dayloop -= timedelta(days=1) 
wikistr = wikistr[:len(wikistr)-2] + '!! wikidata-omschrijving' + '\n'  
rank = 0

site = pywikibot.Site('nl','wikipedia')
for article in topxxlist:
   rank += 1
   rankyesterday = yesterdaysrank(yesterdaystoplist,article,rank)
   prnarticle = article.replace('Bestand',':Bestand',1)
   prnarticle = prnarticle.replace('Categorie',':Categorie',1)
   prnarticle = prnarticle.replace('Sjabloon',':Sjabloon',1)
   if (prnarticle[0:1]==':'):
     prnarticle=prnarticle[1:]
   linkarticle=prnarticle.replace('_',' ')
   linestr = f'|-\n|{rank}\n|{rankyesterday}\n|[[:{linkarticle}]]\n|{hasreferences(article)}\n'
   dayloop=endday
   while (dayloop>=startday):
      indexdate = datetime.combine(dayloop,datetime.min.time()) #make date in right format
      hitsoneday = topxxtable[indexdate][article]
      if hitsoneday is None: hitsoneday = 0
      linestr += '|%s\n' % '{0:6d}'.format(hitsoneday)
      dayloop -= timedelta(days=1) 
   try:
      artpage=pywikibot.Page(site,article)
      wd=artpage.data_item()
      wd.get(get_redirect=True)
      wd_desc=wd.descriptions['nl']
   except Exception as e:    
      wd_desc=str(e)
   wikistr += linestr + '|' + wd_desc  + '\n'
wikistr += "\n|}\n"   

if not debugmodus:
      

      yesterday=date.today()-timedelta(days=1)
      try:
        daystr=weekdays[yesterday.weekday()]
      except:
        daystr='--'
      pywikibot.Page(site, u'User:Edoderoo/nl-stats-gisteren/%4d%02d%02d'%(yesterday.year,yesterday.month,yesterday.day)).put(wikistr, summary=u'Update stats. Source on https://goo .gl/tKMxHv') #Save page
      survey = pywikibot.Page(site,'User:Edoderoo/nl-stats-gisteren')
      survey.text = '%s\n%s' % ('*[[Gebruiker:Edoderoo/nl-stats-gisteren/%4d%02d%02d|%s %02d %02d %4d]]' % (yesterday.year,yesterday.month,yesterday.day,daystr,yesterday.day,yesterday.month,yesterday.year),survey.text)
      pywikibot.Page(site,'User:Edoderoo/nl-stats-gisteren').put(survey.text,summary='new statistics page created for yesterday')
else:
  print("%s" % wikistr)
