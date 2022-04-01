import pywikibot
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
from pywikibot import pagegenerators as pg
#from datetime import datetime
from dateutil import parser

site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()
biodata = '<table class=\'biodata\'>'

Pweight = 'P2067'
Plength = 'P2048'
numbers = '01234567890'
characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
space = ' '
m = 'Q11573'
cm = 'Q174728'
kg = 'Q11570'
g = 'Q41803'
lng = 'nl'

countries = {'ALB': 'Q222', 'AND': 'Q228', 'ARG': 'Q414', 'ARM': 'Q399', 'AUS': 'Q408', 'GER': 'Q183', 'ETH': 'Q115', 'CUB': 'Q241', 'CAN': 'Q16', 'BLR': 'Q184', 'USA': 'Q30', '': '', 'ISL': 'Q189', 'JPN': 'Q17', 'SWE': 'Q34',
             'GBR': 'Q145', 'KOR': 'Q884', 'NOR': 'Q20', 'BEL': 'Q31', 'HUN': 'Q28', 'EGY': 'Q79', 'NZL': 'Q664', 'ITA': 'Q38', 'MOZ': 'Q1029', 'CRO': 'Q224', 'DEN': 'Q35', 'IRQ': 'Q796', 'IRI': 'Q794', 'LTU': 'Q37', 'CZE': 'Q213', 
             'TCH': 'Q33946', 'RSA': 'Q258', 'ROU': 'Q218', 'RUS': 'Q159', 'SLO': 'Q215', 'CHN': 'Q148', 'FRA': 'Q142', 'FIN': 'Q33', 'BRA': 'Q155', 'FRG': 'Q183', 'SUI': 'Q39', 'POR': 'Q45', 'IRL': 'Q27', 'NED': 'Q29999', 
             'ISR': 'Q801', 'IND': 'Q668', 'GUA': 'Q774', 'MEX': 'Q96', 'MYA': 'Q836', 'KSA': 'Q851', 'CRC': 'Q800', 'SVK': 'Q214', 'POL': 'Q36', 'TUR': 'Q43', 'GEQ': 'Q983', 'NGR': 'Q1033', 'LAT': 'Q211', 'GEO': 'Q230', 
             'UKR': 'Q212', 'ESP': 'Q29', 'GAB': 'Q1000', 'PUR': 'Q30', 'AUT': 'Q40', 'URS': 'Q15180', 'PAK': 'Q843', 'BUL': 'Q219', 'COL': 'Q739', 'THA': 'Q869', 'GDR': 'Q16957', 'URU': 'Q77', 'VEN': 'Q717', 'JAM': 'Q766', 
             'LCA': 'Q760', 'SUD': 'Q1049', 'ZIM': 'Q954', 'EST': 'Q191', 'CHI': 'Q298', 'ALG': 'Q262', 'GRE': 'Q41', 'ANG': 'Q916', 'GUM': 'Q16635', 'LUX': 'Q32', 'BOL': 'Q750', 'KEN': 'Q114', 'MDV': 'Q826', 'MRI': 'Q1027', 
             'PER': 'Q419', 'HKG': 'Q148', 'VIE': 'Q881', 'ROC': 'Q159', 'PRK': 'Q423', 'MAR': 'Q1028', 'UGA': 'Q1036', 'MNE': 'Q236', 'GRN': 'Q769', 'BUR': 'Q965', 'MAS': 'Q833', 'HON': 'Q783', 'BAH': 'Q778', 'BRN': 'Q398', 
             'PLE': 'Q219060', 'MDA': 'Q217', 'ESA': 'Q792', 'FIJ': 'Q712', 'LBR': 'Q1014', 'LBN': 'Q822', 'UZB': 'Q265', 'KGZ': 'Q813', 'KAZ': 'Q232', 'GHA': 'Q117', 'SRB': 'Q403', 'SLE': 'Q1044', 'MLT': 'Q233', 'AZE': 'Q227', 
             'TPE': 'Q865', 'YUG': 'Q36704', 'BIH': 'Q225', 'VNM': 'Q881', 'BOH': 'Q39193', 'TJK': 'Q863', 'ATH': 'Q844930', 'LIE': 'Q347', 'SCG': 'Q37024', 'PHI': 'Q928', 'SRI': 'Q854', 'CIV': 'Q1008', 'NEP': 'Q837', 'ZAM': 'Q953', 
             'ARU': 'Q21203', 'LAO': 'Q819', 'UAE': 'Q878', 'GBS': 'Q1007', 'BAN': 'Q902', 'CAM': 'Q424', 'YEM': 'Q805', 'SEY': 'Q1042', 'SYR': 'Q858', 'SKN': 'Q763', 'IVB': 'Q145', 'RWA': 'Q1037', 'SEN': 'Q1041', 'QAT': 'Q846', 
             'BER': 'Q23635', 'CMR': 'Q1009', 'ISV': 'Q11703', 'SAM': 'Q683', 'CYP': 'Q229', 'TUN': 'Q948', 'KIR': 'Q710', 'EUN': 'Q159', 'MAW': 'Q1020', 'MLI': 'Q912', 'ECU': 'Q736', 'NAM': 'Q1030', 'IOA': 'Q574', 'SUR': 'Q730', 
             'ERI': 'Q986', 'MAD': 'Q1019', 'JOR': 'Q810', 'VAN': 'Q686', 'SAA': 'Q183', 'SPA': 'Q5690', 'MGL': 'Q711', 'TLS': 'Q574', 'RHO': 'Q217169', 'PAR': 'Q733', 'ANT': 'Q781', 'COK': 'Q26988', 'SGP': 'Q334', 'SMR': 'Q238', 
             'CAF': 'Q929', 'GAM': 'Q1005', 'KUW': 'Q817', 'ANZ': 'Q408', 'BDI': 'Q967', 'BOT': 'Q963', 'CGO': 'Q971', 'DOM': 'Q786', 'AFG': 'Q889', 'TTO': 'Q754', 'LBA': 'Q1016', 'NCA': 'Q811', 'HAI': 'Q790', 'PNG': 'Q691', 
             'TAN': 'Q924', 'TKM': 'Q874', 'GUY': 'Q734', 'BAR': 'Q244', 'FSM': 'Q702', 'KOS': 'Q1246', 'PLW': 'Q695', 'TOG': 'Q945', 'VIN': 'Q757', 'STP': 'Q45', 'ASA': 'Q30', 'BIZ': 'Q242', 'MON': 'Q235', 'INA': 'Q252', 
             'MAK': 'Q83958', 'SWZ': 'Q1050', 'PAN': 'Q804', 'BRU': 'Q921', 'COD': 'Q974', 'BEN': 'Q962', 'OMA': 'Q842', 'CHA': 'Q657', 'TUV': 'Q672', 'TGA': 'Q678', 'AHO': 'Q29999','LES': 'Q1013', 'NRU': 'Q697', 
             'GUI': 'Q1006', 'BHU': 'Q917', 'SOL': 'Q685', 'DMA': 'Q784', 'SOM': 'Q1045', 'DJI': 'Q977', 'MKD': 'Q221', 'CAY': 'Q145', 'UAR': 'Q79', 'CPV': 'Q1011', 'MHL': 'Q709', 'EOR': 'Q958', 'COM': 'Q970', 
             'NIG': 'Q1032', 'COR': 'Q884','EPH': 'Q1747689', 'MAL': 'Q833', 'ROM': 'Q1747689', 'YMD': 'Q199841', 'WIF': 'Q754', 'YAR': 'Q267584', 'MTN': 'Q1025', 'ALX': 'Q87'}

def wd_sparql_query(spq):
    wikidatasite = pywikibot.Site('wikidata', 'wikidata')
    generator = pg.WikidataSPARQLPageGenerator(spq, site=wikidatasite)
    for wd in generator:
        if (wd.exists()):
            wd.get(get_redirect=True)
            yield wd


def parseWeightLength(string):
    try:
        string += ' x x x '
        weight = length = 0
        wstr = lstr = ''
        w_unit = l_unit = rw_unit = rlunit = ''
        i = 0
        while string[i] in numbers:
            lstr += string[i]
            i += 1
        while string[i] in [space]:
            i += 1
            # print('lstr',lstr,i)
        while string[i] not in [' ', '/', characters]:
            l_unit += string[i]
            i += 1
            # print('l_unit',l_unit,i)
        while string[i] in [space, ' ', '/', '-']:
            i += 1
            # print('x',i)
        while string[i] in numbers:
            wstr += string[i]
            i += 1
            # print('wstr',wstr)
        while string[i] in [space]:
            i += 1
            # print('z',i)
        while ((i < len(string)) & (string[i] not in [' ', '/', characters])):
            w_unit += string[i]
            if (i < len(string)):
                i += 1
            # print('wunit',i,w_unit,len(string))

        if l_unit == 'cm':
            rl_unit = cm
        elif l_unit == 'm':
            rl_unit = m
        else:
            return(0, '', 0, '')

        if w_unit == 'g':
            rw_unit = g
        elif w_unit == 'kg':
            rw_unit = kg
        else:
            return(0, '', 0, '')

        while string[i] in numbers:
            lstr = lstr+string[i]
        #print('[%s][%s]-[%s][%s]' % (wstr,w_unit,lstr,l_unit))
        if wstr == '':
            wstr = '0'
        if lstr == '':
            lstr = '0'
        return (int(wstr), rw_unit, int(lstr), rl_unit)
    except:
        return null, null, null, null


def makesrc():
    source_claim = pywikibot.Claim(repo, 'P248', is_reference=True)
    source_claim.setTarget(pywikibot.ItemPage(repo, 'Q95606922'))
    return(source_claim)


def newClaim(wd, P, value, unit, summary):
    # target=pywikibot.WbQuantity(value,pywikibot.ItemPage(repo,unit),0.1,site=site)
    target = pywikibot.WbQuantity(
        value, pywikibot.ItemPage(repo, unit), site=site)
    claim = pywikibot.Claim(repo, P)
    claim.setTarget(target)
    claim.addSources([makesrc()])
    wd.addClaim(claim, summary=summary)


def simpleway(wd, table):
    row = 0
    hdr = [td.get_text() for td in table.findAll('th')]
    for rowdata in table.findAll("tr"):
        cells = rowdata.findAll("td")
        for x in range(0, len(cells)):
            if (hdr[row] == 'Measurements'):
                weight, wunit, length, lunit = parseWeightLength(
                    cells[x].find(text=True))
                # print(weight,wunit,length,lunit)

                if (not Pweight in wd.claims) and (weight > 30):
                    newClaim(wd, Pweight, weight, wunit,
                             'add weight from Olympedia')
                if (not Plength in wd.claims) and (length > 90):
                    newClaim(wd, Plength, length, lunit,
                             'add length from Olympedia')
            elif (hdr[row] == 'Type'):
                pass
            elif (hdr[row] == 'Full name'):
                fullname = cells[x].find(text=True).replace('•', ' ')
                updateOneAlias(wd, lng, fullname)
            elif (hdr[row] == 'Used name'):
                usedname = cells[x].find(text=True).replace('•', ' ')
                updateOneAlias(wd, lng, usedname)
            elif (hdr[row] == 'Other names'):
                othername = cells[x].find(text=True).replace('•', ' ')
                updateOneAlias(wd, lng, othername)
            elif (hdr[row] == 'Original name'):
                originalname = cells[x].find(text=True).replace('•', ' ')
                updateOneAlias(wd, lng, originalname)
            elif (hdr[row] == 'Nick/petnames'):
                for nick in cells[x].find(text=True).split(','):
                    addNickName(wd, nick)
            elif (hdr[row] == 'NOC'):
                countryname = cells[x].find()
                if (not('P27' in wd.claims)):
                    addCountry(wd, countryname)
                else:
                    listCountry(wd, countryname)
            elif (hdr[row] == 'Affiliations'):
                pass
            elif (hdr[row] == 'Died'):
                if (not 'P570' in wd.claims):
                    DateClaim(wd, 'P570', cells[x].find(text=True))
            elif (hdr[row] == 'Born'):
                if (not 'P569' in wd.claims):
                    DateClaim(wd, 'P569', cells[x].find(text=True))
            elif (hdr[row] == 'Sex'):
                if (not('P21') in wd.claims):
                    sexe = cells[x].find(text=True)
                    if (sexe == 'Female'):
                        addFemale(wd)
                    elif (sexe == 'Male'):
                        addMale(wd)
            else:
                print(hdr[row], '––', cells[x].find(text=True))
            row += 1
def addMale(wd):
    print('addMale')
    target=pywikibot.ItemPage(repo,'Q6581097')
    claim=pywikibot.Claim(repo,'P21')
    claim.setTarget(target)
    claim.addSources([makesrc()])
    wd.addClaim(claim,summary='add sexe from Olympedia')

def addFemale(wd):
    print('addFemale')
    target=pywikibot.ItemPage(repo,'Q6581072')
    claim=pywikibot.Claim(repo,'P21')
    claim.setTarget(target)
    claim.addSources([makesrc()])
    wd.addClaim(claim,summary='add sexe from Olympedia')

def addCountry(wd, countryname):
    claim = pywikibot.Claim(repo, 'P27')
    cntr = countryname.get('src').replace(
        '/images/flags/', '').replace('.png', '')
    print(cntr)
    if (cntr in countries):
        target = pywikibot.ItemPage(repo, countries[cntr])
        claim.setTarget(target)
        claim.addSources([makesrc()])
        wd.addClaim(claim, summary='add nationality from Olympedia')
    else:
        print('missing %1 in countries' % cntr)


def updateOneAlias(wd, lng, alias):
    if lng in wd.labels:
        if wd.labels[lng] == alias:
            return  # little need to add label as alias
    wd.get(get_redirect=True)
    newalias = []
    if (lng in wd.aliases):
        newalias = wd.aliases[lng]
        if not(alias in wd.aliases[lng]):
            newalias.append(alias)
        else:
            return
    else:
        newalias.append(alias)
    wd.editEntity({'aliases': {lng: newalias}},
                  summary=f'---add from Olympedia alias for {lng}')
    print('Add alias %s' % alias)


def addNickName(wd, nickname):

    if ('P1449' in wd.claims):
        return
        for claim in wd.claims['P1449']:
            if claim.getTarget().text == nickname:
                return

    claim = pywikibot.Claim(repo, 'P1449')
    target = pywikibot.WbMonolingualText(text=nickname, language='en')
    claim.setTarget(target)
    claim.addSources([makesrc()])
    wd.addClaim(claim, summary='Nickname from Olympedia')


def Olympedia(wd):
    try:
        f = urlopen('https://www.olympedia.org/athletes/%s' %
                    wd.claims['P8286'][0].getTarget())
    except:
        return
    htmltext = f.read().decode('utf-8')
    soup = BeautifulSoup(htmltext)
    table = soup.find("table", attrs={"class": "biodata"})
    simpleway(wd, table)


def allOlympedians():
    #for wd in wd_sparql_query('select ?item where {?item wdt:P8286 ?o; wdt:P27 ?l. ?item wdt:P106 wd:Q11513337; wdt:P27 wd:Q29999} '):
    for wd in wd_sparql_query('select ?item where {?item wdt:P8286 ?o; wdt:P27 ?l}'):
        print('wd: ', wd.title())
        Olympedia(wd)


def listCountry(wd, countryname):
    try:
      cntr = countryname.get('src').replace('/images/flags/', '').replace('.png', '')
    except:
      cntr = None    
    if (cntr!=None) and (not(cntr in countries)):
        if 'P27' in wd.claims:
            if len(wd.claims['P27']) == 1:
                country = wd.claims['P27'][0].getTarget().title()
                countries.update({cntr: country})
                print(countries)  # copy-paste into source code


def DateClaim(wd, P, DateStr):
    try:
        print('Begin')
        date = parser.parse(DateStr.replace(' in ', ''))
        print('OK-!')
    except:
        print('unknown date format, skipped: ', DateStr)
        return  # no valid date extracted
    target = pywikibot.WbTime(date.year, date.month, date.day)
    claim = pywikibot.Claim(repo, P)
    claim.setTarget(target)
    claim.addSources([makesrc()])
    wd.addClaim(claim, summary='date from Olympedia')


#DateClaim('','P570','15 August 1980')
#item=pywikibot.ItemPage(repo,'Q31295074')
#Olympedia(item)
allOlympedians()
