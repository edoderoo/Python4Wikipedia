import pywikibot
from pywikibot import pagegenerators
from datetime import datetime

"""
  Bezoek alle pagina's met het {{meebezig}} sjabloon, en kijk wanneer de laatste edit was.
  Is dit meer dan 28 dagen geleden? Dan zetten we ze op een lijst, en gaan we er ook vanuit dat we er eigenlijk niet meer mee bezig zijn.
"""

def lastedit(page):
  now = datetime.today()               #current date/time
  old = page.latest_revision.timestamp #date/time of last edit on page
  timediff = now-old
  if (timediff.days>29):
    return(u'*%s - [[%s]]\n' % (page.latest_revision.timestamp,page.title()))
  else:
    return('')

#referredPageTitle = 'Sjabloon:Bronvermelding inwonertal ' + urllib.quote(deelstaat)
#referredPage = pywikibot.Page(pywikibot.Link(referredPageTitle, site))
# gen = pagegenerators.ReferringPageGenerator(referredPage)
#
# wikicode = mwparserfromhell.parse(page.text)
# templates = wikicode.filter_templates()
# infobox = [x for x in templates if x.name.matches('Infobox Duitse plaats plus')]


def main():
   print('start') 
   wikistr = u''
   site=pywikibot.Site(u'nl')
   refPage = pywikibot.Page(pywikibot.Link(u'sjabloon:meebezig',site))
   gen = refPage.getReferences() #pagegenerators.ReferringPageGenerator(refPage)
   gen=pagegenerators.NamespaceFilterPageGenerator( refPage.getReferences(), namespaces=[0])
   for onepage in gen:
     if (onepage.namespace().id==0):
       wikistr = wikistr + lastedit(onepage)
       #print("-------%s- %s" % (onepage.namespace().id,onepage.title()))
     else  :
       pass  #do nothing at all ... other namespaces are skipped
       #print("-------%s- %s" % (onepage.namespace().id,onepage.title()))
   print(wikistr)
   pywikibot.Page(site, u'User:Edoderoo/oude-meebezig').put(wikistr, summary=u'Update . Source on User:Edoderoobot/meebezig-tracker.py') #Save page
   print('Klaar')



"""
def main():
  site = pywikibot.Site(u'nl')
  meebezig = pywikibot.Page(site,u'template:meebezig')
  for onepage in meebezig.backlinks(namespaces=1):
    print(onepage.title())
"""  
main()  
