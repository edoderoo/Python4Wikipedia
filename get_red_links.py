#20190828 1048
import pywikibot
import sys
from urllib.parse import urlparse

srcSite='en'
dstSite='nl'
pagename=''
type2find=[{'P31':'Q5'}]
skipredlinks=True
namespace=[0]

def process_one_link(site,link):
  global repo
  skip=False
  wd=pywikibot.ItemPage(repo,'Q5')
  if (link.exists()):
    linkedpage=pywikibot.Page(site,link.title())
    while linkedpage.isRedirectPage():
      linkedpage=linkedpage.getRedirectTarget()

    skip=not (linkedpage.namespace().id in namespace)
    if (linkedpage.exists()):
      if ('wikibase_item' in linkedpage.properties()):
        wd=linkedpage.data_item()
        wd.get(get_redirect=True)
        for findtype in type2find:
          for onetype in findtype:
            if onetype in wd.claims:
              claim=wd.claims.get(onetype)[0].getTarget().title()
              if claim!=findtype[onetype]:
                skip=True
              else:
                skip= dstSite+'wiki' in wd.sitelinks
      else:
        if (not skip): 
          print('wikidata-missing:  %s' %(link.title()))
  else:   #red links skip all
    skip=skipredlinks

  if not (skip):
    print('Missing|%s|%s' % (wd.title(),link))
  return 1  

def process_one_page(srcSite, pagename):
  total_links =0
  ensite=pywikibot.Site(srcSite)
  page=pywikibot.Page(ensite, pagename)
  for onelink in page.linkedPages():
    total_links += process_one_link(ensite,onelink)
  return total_links

def process_parameters(arg):
  global pagename
  global srcSite
  global dstSite
  global repo
  
  for x in arg:
    if (x[0:5]=='page='):
      pagename=x[5:]
      if pagename[0:2].lower()=='d:':
        wd=pywikibot.ItemPage(repo,pagename[2:])
        wd.get(get_redirect=True)
        pagename=wd.sitelinks[srcSite+'wiki']
        print('Pagename=%s'%(pagename))
    elif (x[0:5]=='wiki='):
      srcSite = x[5:]
    elif (x[0:6]=='check='):
      dstSite=x[6:]
    elif (x[0:10]=='type2find'):
      param=x[10:]
      if param=='human':
        type2find=[{'P31':'Q5'}]
      else:
        type2find=param


repo=pywikibot.Site('wikidata','wikidata').data_repository()
process_parameters(sys.argv)
if (pagename==''):
  print('python3 getredlinks.py page="US Open 2018" wiki=en check=nl type2find=human\npython3 getredlinks.py page=d:Q46977971')
  print('python3 getredlinks.py page=d:Q83629825 wiki=en human')
else:
  print('Page.............: %s\nwiki.............: %s\nFind red links on: %s' % (pagename,srcSite,dstSite))
linksdone=process_one_page(srcSite,pagename)
print('Klaar: %d links bekeken' % linksdone)
