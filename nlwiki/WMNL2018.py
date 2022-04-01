import pywikibot
import sys
import codecs

userlist=[
'MoiraMoira','Rode raaf','Tulp8','Magere Hein','Wiki13','Xxmarijnw','Machaerus',
'ErikvanB','JanCK Fietser','Encycloon','Paul Brussel','The Banner','De Wikischim',
'Edoderoo','Antoine.01','Bdijkstra','Malinka1','RonaldB','Apdency','Robotje',
'Bob.v.R','Vis met 1 oog','Gouwenaar','Wikiklaas','MatthijsWiki','XXBlackburnXx',
'Kattenkruid','Jürgen Eissink','Dqfn13','Happytravels','Freaky Fries','Richardkiwi',
'Ymnes','Vinvlugt','Wikiwerner','Saschaporsche','JanB46','Ecritures','DirkVE','RonnieV',
'Heinonlein','SanderO','Verdel','Ellywa','Erik Wannee','Eve',
]

userlist=['edoderoo','edoderoobot','milanderoo','SRientjes']
userlist=['edoderoo']

bericht='' \
'E-learning programma effectieve online communicatie voor Wikipedianen\n\n' \
'Wikipedianen en Wikimedianen die meer willen weten over hoe online communicatie werkt, of die willen leren hoe ze online strategisch kunnen omgaan met moeilijke situaties - of moeilijke mensen - kunnen nu een e-learning programma doen.\n\n' \
'Het programma is in opdracht van Wikimedia Nederland ontwikkeld door de coachingsdeskundigen van het bureau eCoachPro. Het is speciaal geschreven voor de wereld achter Wikipedia. eCoachPro werkte hierbij samen met een begeleidingsgroep van Nederlandse Wikipedianen en het programma is door een aantal actieve Wikipedianen getest.\n\n' \
'*Je kunt dit programma helemaal zelfstandig doorlopen, of je kunt ervoor kiezen begeleid te worden door een coach\n' \
'*Je kunt op elk moment stoppen en later weer verder gaan.\n' \
'*In drie avonden doe je het hele programma\n' \
'*En vanzelfsprekend kost het niets....\n\n' \
'Heb je belangstelling?  Meer informatie: https://nl.wikimedia.org/wiki/Effectief_Online_Samenwerken\n\n' 

site = pywikibot.Site('nl')

def logme(verbose, formatstring, *parameters):
  with codecs.open("mailing.log.csv", "a", encoding="utf-8") as logfile:
    formattedstring = u'%s%s' % (formatstring, '\n')
    try:
      logfile.write(formattedstring % (parameters) )
    except :
      exctype, value = sys.exc_info()[:2]
      print("1) Error writing to logfile on: [%s] [%s]" % (exctype, value))
      verbose = True    #now I want to see what!
    logfile.close()
  if verbose:
    print(formatstring % (parameters))


def mailoneuser(username):
 mailsubject='Iets nuttigs doen tijdens de kerstvakantie?'

 wikiuser=pywikibot.User(site,username)
 if not wikiuser.isEmailable():
   logme(False,"User is has no mail: %s", username)
   return(0)
 if wikiuser.isBlocked():
   logme(False,"User is blocked    : %s", username)
   return(0)

 try:
   wikiuser.send_email(subject=mailsubject, text=bericht)
   logme(False,"Succes: %s",  username)
   return(1)
 except:
   logme(True,"Fail on user: %s", username)
   return(0)


for user in userlist:
    mailoneuser(user)
 