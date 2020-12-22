import glob
import os
import treetaggerwrapper


def replace(string, filter):
    ''' Entfernt Elemente in filter aus string und entfernt Anführungszeichen. '''
    for char in filter:
        string = string.replace(char, " ")
        string = string.replace("\"", " \" ")
        string = string.lower()
    return string

def lemma(inpath, outpath, charFilter):
    ''' Lemmatisiert Texte in gegebenem Ordner inpath. '''
    for text in os.listdir(inpath):
        if text.endswith('.txt'):
            f_lemma = []
            result = ''
            t = open(inpath + '/' + text, 'r')
            f = t.read()
            for i in t:
                f.replace(i, charFilter + ' ')
            tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')
            tags = tagger.tag_text(f)
            tags2 = treetaggerwrapper.make_tags(tags)
            print("text", text)
            for t in tags2:
                try:
                    result += t.lemma
                    result += ' '
                except:
                    pass
            f_lemma.append(result)
            if not os.path.exists(outpath + text[:-4]+'_lemma.txt'):
                txtFile = open(outpath + text[:-4]+'_lemma.txt', 'w')
                txtFile.write('')
                txtFile.close()
            txtFile = open(outpath + text[:-4]+'_lemma.txt', 'a')
            for i in f_lemma:
                txtFile.write(replace(i, charFilter + ' '))
            txtFile.close()
    return

##charFilter = "§*1234567890,.!;:—?-_(){}[]/\\"
#inpath = '/home/piah/Dokumente/Projektarbeit_LyrikGattungszuweisung/corpus/corpus/Angepasst_Größe/Lyrik/'
#outpath = '/home/piah/Dokumente/Projektarbeit_LyrikGattungszuweisung/corpus/corpus/Angepasst_Größe/Lyrik/Lyrik_Lemma/'
#print("text", lemma(inpath, outpath, charFilter))
#
def concat_corpus(path):
    ''' Fügt alle txt-Datein zu einer Großen zusammen '''
    read_files = glob.glob(path) #Arent/lemma/*.txt")
    path = os.path.dirname(path)
    corpus = path.split('/')[6]
    print(read_files)
    with open("/home/piah/Dokumente/Uni/Projektarbeit/Projektarbeit_LyrikGattungszuweisung/corpus/corpus/Angepasst_Größe_groß/result.txt", "wb") as outfile:
        for f in read_files:
            print(f)
            with open(f, "rb") as infile:
                outfile.write(infile.read()) #.lower())
    corpus_name = os.rename('/home/piah/Dokumente/Uni/Projektarbeit/Projektarbeit_LyrikGattungszuweisung/corpus/corpus/Angepasst_Größe_groß/result.txt', '/home/piah/Dokumente/Uni/Projektarbeit/Projektarbeit_LyrikGattungszuweisung/corpus/corpus/Angepasst_Größe_groß/_' + str(corpus) + '.txt')
    return corpus_name
#path = "/home/piah/Dokumente/Uni/Projektarbeit/Projektarbeit_LyrikGattungszuweisung/corpus/corpus/Angepasst_Größe_groß/Balladen/Balladen_Lemma/*.txt"
#concat_corpus(path)
#tagger.tag_file_to('../corpus/German_prosa/prosa/achleitner_bergrichters.txt', '../corpus/German_prosa/prosa/achleitner_bergrichters2.txt') #evtl für gesamtes Korpus


def segment(wordList, n, outpath):
    """ Teilt den Korpus wordList in Segmente der Länge n. """
    for i in range(0, len(wordList), n):
        datei = []
        if i + n <= len(wordList):
            for j in range(i, i+n):
                datei.append(wordList[j].encode('utf8')) #.lower())

            if os.path.exists(outpath + str(i) + ".txt"):
                txtFile = open(outpath + str(i) + ".txt", "w")
                txtFile.write('')
                txtFile.close()
            txtFile = open(outpath + str(i) + ".txt", "a")
            for word in datei:
                txtFile.write(word.decode('utf8') + " ")
            txtFile.close()
        else:
            pass
    return

#
out = '/home/piah/Dokumente/Uni/Projektarbeit/Projektarbeit_LyrikGattungszuweisung/corpus/corpus/Angepasst_Größe_groß/segments/Lyrik/500/'
words = open('/home/piah/Dokumente/Uni/Projektarbeit/Projektarbeit_LyrikGattungszuweisung/corpus/corpus/Angepasst_Größe_groß/corpus_gross_Lyrik.txt', 'r')
wordList = words.read()
segment(wordList.split(), 500, out)
