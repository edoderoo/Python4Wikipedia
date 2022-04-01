import pywikibot

print('Start')
template='Sjabloon:Navigatie tijdschriften Vlaanderen'
site=pywikibot.Site('nl','wikipedia')
tp=pywikibot.Page(site,template)
for x in tp.linkedPages():
   page=pywikibot.Page(site,x.title())
   if page.exists():
     page.put(page.text,'')
print('Klaar')