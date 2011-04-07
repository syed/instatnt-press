# -*- coding: utf-8 -*-
#
# Instant Press. Instant sites. CMS developed in Web2py Framework
# Site: http://www.instant2press.com 
#
# Copyright (c) 2010 Mulone, Pablo Martín 
#
# License Code: GPL, General Public License v. 2.0
# License Content: Creative Commons Attribution 3.0 
#
# Also visit: www.web2py.com 
#             or Groups: http://groups.google.com/group/web2py 
#                http://groups.google.com/group/web2py-usuarios  
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>

#import math
#import datetime

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
import gluon.contrib.simplejson as sj
from utils import *

def en_stopwords():
    stopwords = ["a’s","able","about","above","according","accordingly","across","actually","after",\
                 "afterwards","again","against","ain’t","all","allow","allows","almost","alone",\
                 "along","already","also","although","always","am","among","amongst","an","and",\
                 "another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere",\
                 "apart","appear","appreciate","appropriate","are","aren’t","around","as","aside","ask",\
                 "asking","associated","at","available","away","awfully","be","became","because","become",\
                 "becomes","becoming","been","before","beforehand","behind","being","believe","below",\
                 "beside","besides","best","better","between","beyond","both","brief","but","by","c’mon",\
                 "c’s","came","can","can’t","cannot","cant","cause","causes","certain","certainly","changes",\
                 "clearly","co","com","come","comes","concerning","consequently","consider","considering",\
                 "contain","containing","contains","corresponding","could","couldn’t","course","currently",\
                 "definitely","described","despite","did","didn’t","different","do","does","doesn’t","doing",\
                 "don’t","done","down","downwards","during","each","edu","eg","eight","either","else",\
                 "elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody",\
                 "everyone","everything","everywhere","ex","exactly","example","except","far","few","fifth",\
                 "first","five","followed","following","follows","for","former","formerly","forth","four",\
                 "from","further","furthermore","get","gets","getting","given","gives","go","goes","going",\
                 "gone","got","gotten","greetings","had","hadn’t","happens","hardly","has","hasn’t","have",\
                 "haven’t","having","he","he’s","hello","help","hence","her","here","here’s","hereafter",\
                 "hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully",\
                 "how","howbeit","however","i’d","i’ll","i’m","i’ve","ie","if","ignored","immediate","in",\
                 "inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead",\
                 "into","inward","is","isn’t","it","it’d","it’ll","it’s","its","itself","just","keep",\
                 "keeps","kept","know","knows","known","last","lately","later","latter","latterly","least",\
                 "less","lest","let","let’s","like","liked","likely","little","look","looking","looks",\
                 "ltd","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more",\
                 "moreover","most","mostly","much","must","my","myself","name","namely","nd","near",\
                 "nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine",\
                 "no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere",\
                 "obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only",\
                 "onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside",\
                 "over","overall","own","particular","particularly","per","perhaps","placed","please","plus",\
                 "possible","presumably","probably","provides","que","quite","qv","rather","rd","re","really",\
                 "reasonably","regarding","regardless","regards","relatively","respectively","right","said",\
                 "same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed",\
                 "seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven",\
                 "several","shall","she","should","shouldn’t","since","six","so","some","somebody","somehow",\
                 "someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry",\
                 "specified","specify","specifying","still","sub","such","sup","sure","t’s","take",\
                 "taken","tell","tends","th","than","thank","thanks","thanx","that","that’s","thats",\
                 "the","their","theirs","them","themselves","then","thence","there","there’s","thereafter",\
                 "thereby","therefore","therein","theres","thereupon","these","they","they’d","they’ll",\
                 "they’re","they’ve","think","third","this","thorough","thoroughly","those","though",\
                 "three","through","throughout","thru","thus","to","together","too","took","toward","towards",\
                 "tried","tries","truly","try","trying","twice","two","un","under","unfortunately","unless",\
                 "unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually",\
                 "value","various","very","via","viz","vs","want","wants","was","wasn’t","way","we","we’d",\
                 "we’ll","we’re","we’ve","welcome","well","went","were","weren’t","what","what’s","whatever",\
                 "when","whence","whenever","where","where’s","whereafter","whereas","whereby","wherein",\
                 "whereupon","wherever","whether","which","while","whither","who","who’s","whoever","whole",\
                 "whom","whose","why","will","willing","wish","with","within","without","won’t","wonder",\
                 "would","would","wouldn’t","yes","yet","you","you’d","you’ll","you’re","you’ve","your",\
                 "yours","yourself","yourselves","zero"]
    
    return stopwords

def es_es_stopwords():
    stopwords = ["a","acuerdo","adelante","ademas","además","adrede","ahi","ahí","ahora","al","alli",\
                 "allí","alrededor","antano","antaño","ante","antes","apenas","aproximadamente","aquel",\
                 "aquél","aquella","aquélla","aquellas","aquéllas","aquello","aquellos","aquéllos","aqui",\
                 "aquí","arribaabajo","asi","así","aun","aún","aunque","b","bajo","bastante","bien",\
                 "breve","c","casi","cerca","claro","como","cómo","con","conmigo","contigo","contra",\
                 "cual","cuál","cuales","cuáles","cuando","cuándo","cuanta","cuánta","cuantas","cuántas",\
                 "cuanto","cuánto","cuantos","cuántos","d","de","debajo","del","delante","demasiado","dentro",\
                 "deprisa","desde","despacio","despues","después","detras","detrás","dia","día","dias",\
                 "días","donde","dónde","dos","durante","e","el","él","ella","ellas","ellos","en","encima",\
                 "enfrente","enseguida","entre","es","esa","ésa","esas","ésas","ese","ése","eso","esos",\
                 "ésos","esta","está","ésta","estado","estados","estan","están","estar","estas","éstas",\
                 "este","éste","esto","estos","éstos","ex","excepto","f","final","fue","fuera",\
                 "fueron","g","general","gran","h","ha","habia","había","habla","hablan","hace","hacia",\
                 "han","hasta","hay","horas","hoy","i","incluso","informo","informó","j","junto","k","l",\
                 "la","lado","las","le","lejos","lo","los","luego","m","mal","mas","más","mayor","me",\
                 "medio","mejor","menos","menudo","mi","mí","mia","mía","mias","mías","mientras","mio",\
                 "mío","mios","míos","mis","mismo","mucho","muy","n","nada","nadie","ninguna","no","nos",\
                 "nosotras","nosotros","nuestra","nuestras","nuestro","nuestros","nueva","nuevo","nunca",\
                 "o","os","otra","otros","p","pais","paìs","para","parte","pasado","peor","pero","poco",\
                 "por","porque","pronto","proximo","próximo","puede","q","qeu","que","qué","quien","quién",\
                 "quienes","quiénes","quiza","quizá","quizas","quizás","r","raras","repente","s","salvo",\
                 "se","sé","segun","según","ser","sera","será","si","sí","sido","siempre","sin","sobre",\
                 "solamente","solo","sólo","son","soyos","su","supuesto","sus","suya","suyas","suyo","t",\
                 "tal","tambien","también","tampoco","tarde","te","temprano","ti","tiene","todavia",\
                 "todavía","todo","todos","tras","tu","tú","tus","tuya","tuyas","tuyo","tuyos","u","un",\
                 "una","unas","uno","unos","usted","ustedes","v","veces","vez","vosotras","vosotros",\
                 "vuestra","vuestras","vuestro","vuestros","w","x","y","ya","yo","z"]
    
    return stopwords


def pt_br_stopwords():
    
    stopwords = ["último","é","acerca","agora","algmas","alguns","ali","ambos","antes","apontar",\
                 "aquela","aquelas","aquele","aqueles","aqui","atrás","bem","bom","cada","caminho",\
                 "cima","com","como","comprido","conhecido","corrente","das","debaixo","dentro",\
                 "desde","desligado","deve","devem","deverá","direita","diz","dizer","dois","dos",\
                 "e","ela","ele","eles","em","enquanto","então","está","estão","estado","estar",\
                 "estará","este","estes","esteve","estive","estivemos","estiveram","eu","fará",\
                 "faz","fazer","fazia","fez","fim","foi","fora","horas","iniciar","inicio","ir",\
                 "irá","ista","iste","isto","ligado","maioria","maiorias","mais","mas","mesmo","meu",\
                 "muito","muitos","nós","não","nome","nosso","novo","o","onde","os","ou","outro",\
                 "para","parte","pegar","pelo","pessoas","pode","poderá","podia","por","porque",\
                 "povo","promeiro","quê","qual","qualquer","quando","quem","quieto","são","saber",\
                 "sem","ser","seu","somente","têm","tal","também","tem","tempo","tenho","tentar",\
                 "tentaram","tente","tentei","teu","teve","tipo","tive","todos","trabalhar","trabalho",\
                 "tu","um","uma","umas","uns","usa","usar","valor","veja","ver","verdade","verdadeiro",\
                 "você"]
    
    return stopwords


def nl_stopwords():
    
    stopwords = [                
                 "aan","af","al","als","bij","dan","dat","die","dit","een","en","er","had","heb",\
                 "hem","het","hij","hoe","hun","ik    ","in","is","je","kan","me","men","met","mij",\
                 "nog","nu","of","ons","ook","te","tot","uit","van","was","wat","we","wel","wij","zal",\
                 "ze","zei","zij","zo","zou"                
                 ]
    
    return stopwords


def get_language_stopwords(language="en"):
    stopwords=[]
    if language=="en":
        stopwords = en_stopwords()
    elif language=="es-es":
        stopwords = es_es_stopwords()
    elif language=="pt-br":
        stopwords = pt_br_stopwords()
    elif language=="nl":
        stopwords = nl_stopwords()
    return stopwords


def remove_special_chars(mystring):
    import string    
            
    blacklist = "“”¿—" #additional symbols :S 
    symbol_to_remove = string.punctuation + blacklist
               
    for char in symbol_to_remove:
        mystring = mystring.replace(char, ' ')
    return mystring
           

#this is not intent to be a fully features full text
#only to make better search, because not have like or match in Appengine
#it's use stringlist to save the words after remove the stopwords 
#perhaps this is not efficient, but this is only admin when you change content or body
#Note: we need a better method to do this 
def get_clean_words(content,language="en"):
       
    clean_list = []
    if not isinstance(content, (unicode, str) ): 
        raise ValueError('Content list must be of type string or unicode.')
    
    content = remove_special_chars(content)
    content_list = content.split() #split white spaces into an array    
    mystopwords = get_language_stopwords(language) #get stopwords to remove, 
    
    for word in content_list:
        cleanword = word.strip()
        if cleanword=="":
            continue        
        
        cleanword = cleanword.lower() #make lower caption
               
        if len(cleanword)<=1: #if a word is 1 char lenght or less pass it
            continue
        
        if cleanword in mystopwords: #if is a stopword removed
            continue
               
        clean_list.append(cleanword)    
     
    clean_list = {}.fromkeys(clean_list).keys() # finally Remove duplicates
    try: clean_list.remove('') 
    except: pass #remove ''
    
    return clean_list


#THIS IS TO PRESERVE COMPATIBILITY WITH GAE
#ABSTRACT:
#There are a problems with multilanguage support in gae, raising many unicode problems
#so I make different treat to gae,so if you think this is a problem, dont use gae.

def get_clean_words_gae(content,language="en"):
       
    clean_list = []
    if not isinstance(content, (unicode, str) ): 
        raise ValueError('Content list must be of type string or unicode.')
        
    content_list = content.split() #split white spaces into an array    
    #mystopwords = en_stopwords() #get stopwords to remove, 
    mystopwords = get_language_stopwords(language) #get stopwords to remove,
    
    for word in content_list:
        cleanword = word.strip()
        if cleanword=="":
            continue
        cleanword = normalize_word(cleanword) #lower and convert é to e example
                                              # I am not sure this is a gae problem or web2py
                                              #but in gae appears not to accept special characters 
                                              #in list types
        
        if len(cleanword)<=1:
            continue
        
        if cleanword in mystopwords:
            continue
        
        clean_list.append(cleanword)    
     
    clean_list = {}.fromkeys(clean_list).keys() # Remove duplicate
    try: clean_list.remove('') 
    except: pass #remove ''
    
    return clean_list


def normalize_word(value): 
    import unicodedata
            
    if not isinstance(value, (unicode,) ): 
        s = value.decode('utf8','ignore') 
    else:
        s = value   
    
    s = re.sub('<.*?>','',s) #remove all inside html
    s = s.lower()    # to lowercase utf-8 
    s = unicodedata.normalize('NFKD', s) # normalize eg è => e, ñ => n 
    s = s.encode('ASCII', 'ignore')      # encode as ASCII   
    s = re.sub('[^a-z0-9]', '', s)   # strip all but alphanumeric/hyphen/space
        
    return s
             




