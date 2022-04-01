
import pywikibot
from pywikibot import pagegenerators as pg

convertstr={'Ç':'C','ü':'u','é':'e','â':'a','ä':'a','à':'a','å':'a','ç':'c','ê':'e','ë':'e','è':'e','ï':'i','î':'i',
            'ì':'i','Ä':'A','Å':'A','É':'E','æ':'ae','Æ':'AE','ô':'o','ö':'o','ò':'o','û':'u','(':'(',')':')','*':'*',
            'á':'a','í':'i','ó':'o','ú':'u','ñ':'n','Ñ':'N','ª':'a','º':'o','¿':'?','½':'1/2','¼':'1/4','¡':'!','[':'[',']':']',
            'α':'a','ß':'ss','π':'pi','σ':'delta','µ':'micro','τ':'teta','Φ':'phi',' ':' ','-':'-','+':'+','!':'!',
            '0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9','=':'=','-':'-','_':'_',
            'a':'a','b':'b','c':'c','d':'d','e':'e','f':'f','g':'g','h':'h','i':'i','j':'j','k':'k','l':'l','m':'m',
            'n':'n','o':'o','p':'p','q':'q','r':'r','s':'s','t':'t','u':'u','v':'v','w':'w','x':'x','y':'y','z':'z',
            'A':'A','B':'B','C':'C','D':'D','E':'E','F':'F','G':'G','H':'H','I':'I','J':'J','K':'K','L':'L','M':'M',
            'N':'N','O':'O','P':'P','Q':'Q','R':'R','S':'S','T':'T','U':'U','V':'V','W':'W','X':'X','Y':'Y','Z':'Z',
            '@':'@','#':'#','$':'$','%':'%','^':'^','&':'&','|':'|','\\':'\\','{':'{','}':'}','`':'`','\'':'\'','’':'’',
            ',':',','.':'.','\"':'\"','Ö':'O','—':'—','':'','':'','':'','':'','':'','':'','':'','':'','':'',}

def normalise_str(inp):
    outp=''
    for ch in inp:
      if ch in convertstr:  
        outp += convertstr[ch]
      else:
        print(f'Missing: {ch}')
        print(10/0)
    return(outp)


def wd_sparql_query(spq):
   generator=pg.WikidataSPARQLPageGenerator(spq,site=pywikibot.Site('wikidata','wikidata'))
   for wd in generator:
     try:
       wd.get(get_redirect=True)
       yield wd
     except:
       pass

def add2alias(wd,alias):
    if srclng in wd.aliases:
      if (not (alias in wd.aliases[srclng])):
        wd.aliases[srclng].append(alias)
    else:
        return([alias])
    return(wd.aliases[srclng])

def check_alias(wd, check4alias):
  if (srclng in wd.aliases):
    for alias in wd.aliases[srclng]:
      if (alias.upper()==check4alias.upper()):
        return(True)
  if (srclng in wd.labels):
    return(wd.labels[srclng].upper()==check4alias.upper())
  return(False)        

site = pywikibot.Site('nl','wikipedia')           #Geef aan naar welke site je wilt schrijven
repo = site.data_repository()                     #voor ophalen wikidata-items adhv Qxxxx
query='select ?item where {?item wdt:P31 wd:Q79007 . ?item wdt:P17 wd:Q55 . ?item wdt:P276 ?loc}'
srclng='nl'
commit=True

print('Begonnen')
kookpunt=0
for street in wd_sparql_query(query):
  data={}  
  for loc in street.claims['P276']:
    location=loc.getTarget()
    location.get(get_redirect=True)
    if (srclng in street.labels) and (srclng in location.labels):
      newAlias=f'{street.labels[srclng]} ({location.labels[srclng]})'
      if not check_alias(street,newAlias):
        data.update({'aliases':{srclng:add2alias(street,newAlias)}})
      newAlias=normalise_str(newAlias)
      if not check_alias(street,newAlias):
        data.update({'aliases':{srclng:add2alias(street,newAlias)}})
        
    if (data!={}):
      if (commit): 
        kookpunt+=1
        street.editEntity(data,summary=f'add alias for street ({srclng})')    
        #if kookpunt>10: print(10/0)
      else:
        print(data)
print('Klaar')  
