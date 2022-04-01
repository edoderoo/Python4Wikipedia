import pywikibot, mwparserfromhell, re
#from pprint import pprint

sourcepage = 'Gebruiker:Vinkje83/WTA150'
destination= 'User:Vinkje83/WTA150/results'
tabelheader='{| class="wikitable sortable"\n|-\n! Artikel !! Posities !! Gestegen !! Qid\n'
tabelfooter='\n|}\n'

class Dame:
        def __init__(self, rij):
                nummer, speelster, punten, verandering = rij._contents.nodes
                self.nieuwe_rangpositie = int(nummer.contents.strip_code().replace('. ', ''))
                self.naam = speelster.contents.filter_wikilinks()[0].title
                self.verandering = verandering.contents.filter_templates()[0].title()
                self.bestaande_rangpositie = 0
                self.Qid = ''
        def load_enkelhoogstepositie(self, site):
                p = pywikibot.Page(site, self.naam)
                wikicode = mwparserfromhell.parse(p.text)
                "Enkelhoogstepositie  Infobox tennisspeler"
                infoboxes = [template for template in wikicode.filter_templates(matches=lambda t: t.name.matches('Infobox tennisspeler'))]
                if len(infoboxes) == 0:
                   self.bestaande_rangpositie = -1
                   return
                if ('Enkelhoogstepositie' in infoboxes[0]):
                  positie_text = infoboxes[0].get('Enkelhoogstepositie').value.strip_code() # "17. (18 april 2018)"
                  if (positie_text != ''):
                    self.bestaande_rangpositie = int(re.findall('[0-9]+', positie_text)[0])


def laadtennistabel(site):
        p = pywikibot.Page(site, sourcepage)
        wikicode = mwparserfromhell.parse(p.text)
        dames = [Dame(rij) for rij in wikicode.filter_tags(matches=lambda node: node.tag == 'tr')[1:]]
        "Dames met verlies en stabiel overslaan, blijft over winst"
        dames = [dame for dame in dames if dame.verandering == '{{Winst}}' ]
        for dame in dames:
          try:
            print('dame',dame.naam)
            dame.load_enkelhoogstepositie(site)
          except:
            pass
        return dames

def main(*args):
        local_args = pywikibot.handle_args(args)
        site = pywikibot.Site(code='nl', fam='wikipedia')

        dames = laadtennistabel(site)
        geenbox = [(dame.naam, 'N = %d-Geen infobox' % (dame.nieuwe_rangpositie)) for dame in dames if dame.bestaande_rangpositie == -1]
        nietgevonden = [(dame.naam, 'Geen bestaande rangpositie') for dame in dames if dame.bestaande_rangpositie == 0]
        gestegen = [(dame.naam, f'({dame.nieuwe_rangpositie} < {dame.bestaande_rangpositie})||{dame.bestaande_rangpositie-dame.nieuwe_rangpositie}||{dame.Qid}') for dame in dames if dame.nieuwe_rangpositie < dame.bestaande_rangpositie]


        resulttxt=';Enkelspel\nInfobox (en Wikidata) mag worden bijgewerkt voor: \n'
        resulttxt += '\n;Gestegen\n'+tabelheader
        for x in gestegen:
          print('g',x);
          resulttxt+=('|-\n|[[%s]]||%s\n'%(x[0],x[1]) )
        resulttxt+=tabelfooter+'\n;Geen infobox\n'+tabelheader
        for x in geenbox:
          print('gb', x)
          resulttxt+=('|-\n|[[%s]]||%s\n'%(x[0],x[1]) )
        resulttxt+=tabelfooter
        pywikibot.Page(site,destination).put(resulttxt,summary='WTA-statistieken bijgewerkt')
        #print(resulttxt)

print('Begonnen')
main()
print('Klaar')
