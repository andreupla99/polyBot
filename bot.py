import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from interpret import Interpret


class Bot():

    # Constructor
    def __init__(self):
        # Declara una constant amb el access token que llegeix de token.txt
        TOKEN = open('token.txt').read().strip()

        # Carpeta on es guardaran les imatges generades (carpeta local)
        self.imageFolder = 'Imatges/'

        # Instància de l'intèrpret
        # self.interpret = Interpret()

        # Crea els objectes per treballar amb Telegram
        self.updater = Updater(token=TOKEN, use_context=True)
        dispatcher = self.updater.dispatcher

        # Relaciona les comandes amb els mètodes
        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(CommandHandler('help', self.help))
        dispatcher.add_handler(CommandHandler('author', self.author))
        dispatcher.add_handler(CommandHandler('reset', self.reset))
        dispatcher.add_handler(CommandHandler('exit', self.exit))   # No acaba de funcionar del tot bé

        # Enllaça un missatge normal de text amb la funció interpret
        dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=self.interpret))

        # Encen el bot
        self.updater.start_polling()

    # Metode que està associat a la comanda /start. S'inicia el bot  i mostrem
    # totes les possibles comandes que podem demanra-li
    def start(self, update, context):
        # Cada usuari tindrà un interpret diferent pel que no se sobreescriuràn les dades dels uns als altres
        context.user_data['antlr'] = Interpret()

        nom = update.message.from_user.first_name
        nomBot = 'polyBot'
        text = '''
Hola {}. Em dic `{}` 🤖, sóc un Bot que t\'ajuda a crear Poligons, operar amb ells i representar-los visualment.
Pots escriure les següents *comandes* per a obtenir *més informació*:
*/start* - Inicia la conversa amb el Bot.
*/help* - Explicació de les comandes que pots fer servir i com utilitzar-les.
*/author* - Autor del projecte.
*/reset* - Reinicia el context d'execució i elimina les dades de l'execució prèvia.
        '''.format(nom, nomBot)

        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='Markdown', text=text)

    # Metode que està associat a la comanda /help.
    # Es dona tota l'informació de com crear els poligons i les operacions que podem fer amb ells
    def help(self, update, context):
        rgb = "{r g b}"
        text = '''
Per tal de que et pugui entendre, hauràs de demanar\'m-ho utilitzant les comandes que tens a continuació:

Per crear un polígon hauràs d'introduir tots els seus vèrtex de la següent manera:

    [x1 y1  x2 y2  x3 y3]

On cada parell de números x y correspon a les coordenades d\'un punt.
Alternativament pots utilitzar "\'!\'num" on num és el número de vèrtex. Això generarà un polígon amb "num" vèrtex amb coordenades aleatòries entre [0,1].

⚠️IMPORTANT⚠️: En cas de que el polígon introduit no sigui convex el convertiré automàticament en un polígon convex, ja que aquests són amb els que sé treballar.
Si vols assegurar el correcte funcionament de les operacions assegura\'t que introdueixes polígons regulars (amb els vèrtex en ordre horari).

Els polígons han de ser creats i guardats de manera immediata o utilitzats en alguna operació fent ús de la notació:

    nomPoligon := [x1 y1  x2 y2  x3 y3]

o alternativament

    nomPoligon := operació amb polígons

Les comandes disponibles amb polígons regulars són:

    - color p, {}: Estableix el color del polígon p als valors RGB donats (seguint les sigles en anglès Red, Green i Blue). El rang dels colors és [0,1].
    - print p o print "missatge": En cas de que p sigui un polígon mostraré els seus vèrtex per pantalla. En cas de donar un missatge mostraré el missatge.
    - area p: Mostraré l'àrea del polígon p.
    - perimeter p: Mostraré el perímetre del polígon p.
    - vertices p: Mostraré el nombre de vèrtex del polígon p.
    - centroid p: Mostraré el centroide del polígon p.
    - inside p1, p2: Et diré si p1 està dintre de p2.
    - equal p1, p2: Et diré si p1 i p2 són iguals.

Pots definir qualsevol polígon utilitzant el nom amb el que l'has definit anteriorment, utilitzant un dels dos mètodes de creació que t'he ensenyat o com a una operació entre polígons.
Les operacions que pots fer són:

    - p1 + p2: Retorna la unió convexa entre els polígons p1 i p2.
    - p1 * p2: Retorna la intersecció entre els polígons p1 i p2.
    - #p: Retorna la capsa contenidora del polígon p.

També pots utilitzar parèntesi per definir prioritat entre les opareacions.

Finalment per mostrar una imatge amb els polígons tinc la comanda draw:

    - draw "arxiu.png", p1, p2, p3

Amb la que em pots passar tants polígons com vulguis i te-ls ensenyare representats en 2D. 📈📈

        '''.format(rgb)
        # text='''Hola.'''
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Espero haver-te sigut d\'ajut, ja em diras el que puc fer per tu. ☺️')

    # Metode que està associat a la comanda /author.
    # Dóna informació sobre l'author
    def author(self, update, context):
        text = '''
El meu autor és l' *Andreu Pla*.
Pots posar-te en contacte amb ell via mail a:
✉️`andreu.pla.ortiz.de.zarate@estudiantat.upc.edu`'''
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='Markdown', text=text)

    def reset(self, update, context):
        context.user_data['antlr'] = Interpret()
        context.bot.send_message(chat_id=update.effective_chat.id, text='S\'han esborrat les dades. Ja pots tornar a demanar el que necessitis.')
        text = '''
Si vols més informació sobre les comandes que pots utilitzar escriu la comanda */help*.'''
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='Markdown', text=text)

    # Extreu els resultats de l'execució cridant a l'intèrpret
    def interpret(self, update, context):
        input = update.message.text

        info = context.user_data['antlr'].executarInstruccio(input)
        # Retorna sempre un string, tant si és un resultat o el nom d'un fitxer .png a enviar

        if (info is not None):
            out = ''
            for x in info:
                if (x is not None):
                    # print(x)
                    if (len(x) > 3 and x[len(x)-4] == '.' and x[len(x)-3] == 'p' and x[len(x)-2] == 'n' and x[len(x)-1] == 'g'):
                        file = self.imageFolder + x
                        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(file, 'rb'))
                    else:
                        out += x + '\n'

            if (out != ''):
                context.bot.send_message(chat_id=update.effective_chat.id, text=out)

        # Si info es None, es que hi ha hagut algun error al tractar l'instrucció
        else:
            text = 'No entenc el que em vols dir. Intenta-ho un altre cop'

    # Metode que està associat a la comanda /author.
    # Serviria per terminar el bot, però de moment només es pot terminar parant l'execució des de terminal.
    def exit(self, update, context):
        text = '''
Espero que t\'hagi sigut d\'ajut, si et fan falta més polígons sempre pots tornar-me a despertar amb la comanda */start*.
        '''
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode='Markdown', text=text)
        context.bot.send_message(chat_id=update.effective_chat.id, text='A reveure!')
        context.bot.send_message(chat_id=update.effective_chat.id, text='👋')
        sys.exit(0)     # això hauría de terminar el programa però per alguna raó no funciona.

bot = Bot()
