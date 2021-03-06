import re
import spacy
from chart_studio.plotly import iplot
from wordcloud import WordCloud
import matplotlib
from matplotlib import pyplot as plt
import operator
import argparse
import collections
import plotly.graph_objects as go
import clustering
import plottingvso2
import math
import sys


def tokenizer(text):
    new = re.sub(r"[^\w\s]", "", text)
    liste = new.split()
    return liste


def frequency(liste):
    # literelement: compte pour moi nombre d'occurence de chauque mot dans la liste pour chauque element de liste
    liste_of_frequence = [liste.count(w) for w in liste]
    # les valeurs seront les nombres d'occurences dans le deuxieme liste(liste_of_frequence)
    dictionary = dict(zip(liste, liste_of_frequence))
    r = input("Voulez-vous sauvegarder un nuage de mots? ")
    if r == "oui":
        wordcl(dictionary)
    r = input("Voulez-vous sauvegarder un graphique? ")
    if r == "oui":
        freqplot(dictionary)

    # print("in form of a dictionary:")
    # dans une celule de liste insertons clés et valeur pour chaque clés et valeur de diccionaire (methode .items() permet acceder en même temps aux clés et valeurs)
    list_key_value = [[k, v] for v, k in dictionary.items()]
    # print("in form of a list:")
    # print(list_key_value)
    r = input("Voulez-vous afficher les résultats par ordre croissant? ")
    if r == "oui":
        for w in sorted(dictionary, key=dictionary.get, reverse=False):
            print(w, dictionary[w])
    elif r == "non":
        for w in sorted(dictionary, key=dictionary.get, reverse=True):
            print(w, dictionary[w])
    else:
        print("Mauvaise réponse!")

    # juste le methode sorted. en fait on peut comme ici n'indiquer pas reverse quand on a beaoin d;ordre decroissant parce que il est par defaut
    list_croissant = sorted(list_key_value)
    # print (list_croissant)
    list_descroissant = sorted(list_key_value, reverse=True)
    # print(list_descroissant)


# verifies if pattern is correct
def verify(inp):
    spacyliste = [
        "ADJ",
        "NOUN",
        "VERB",
        "ADP",
        "ADV",
        "AUX",
        "CCONJ",
        "DET",
        "PRON",
        "PROPN",
        "NUM",
        "SCONJ",
    ]
    if len(inp) > 0:
        if inp.isupper():
            for e in inp.split():
                if e in spacyliste:
                    return inp
                else:
                    NError = ValueError("Cette catégorie POStag ne se trouve pas dans la liste.")
                    raise NError
        else:
            NError = ValueError("En majuscule svp")
            raise NError
    else:
        NError = ValueError("Aucun patron")
        raise NError


# gives the pattern
def posstats(doc):
    t = [word.pos_ for word in doc]
    liste_of_frequence = [t.count(e) for e in t]
    # les valeurs seront les nombres d'occurences dans le deuxieme liste(liste_of_frequence)
    dictionary = dict(zip(t, liste_of_frequence))
    list_key_value = [[k, v] for v, k in dictionary.items()]
    # print("in form of a list:")
    # print(list_key_value)
    r = input("Voulez-vous sauvegarder un nuage de mots? ")
    if r == "oui":
        wordcl(dictionary)
    r = input("Voulez-vous sauvegarder un graphique? ")
    if r == "oui":
        freqplot(dictionary)
    for w in sorted(dictionary, key=dictionary.get, reverse=True):
        print(w, dictionary[w])


def specificity(text):
    inp = input("Quel document?")
    sys.float_info.max
    ltotal = len(text)
    r = text.split("***")
    l = len(r)
    print("Il y a", l, "documents dans votre corpus. ")
    lpartie = len(r[int(inp) - 1])
    terme = input("Quel mot? ")
    if terme in text:
        freqdanspartie = r[0].count(terme)
        freqtotal = text.count(terme)
        s = (
            (
                math.factorial(ltotal - freqtotal)
                // (
                    math.factorial(lpartie - freqdanspartie)
                    * math.factorial((ltotal - freqtotal) - (lpartie - freqdanspartie))
                )
            )
            * (
                math.factorial(freqtotal)
                // (
                    math.factorial(freqdanspartie)
                    * math.factorial(freqtotal - freqdanspartie)
                )
            )
        ) // (
            math.factorial(ltotal)
            // (math.factorial(lpartie) * math.factorial(ltotal - lpartie))
        )
        print(terme, "-", s)
    else:
        print("Aucune occurrence de ce mot dans le corpus.")


def patterngiver(doc):
    t = [(word.text, word.pos_) for word in doc]
    inp = input(
        "Choisissez une série de 1 à 4 POStags de cette liste et écrivez-les en majuscules séparés par un espace ('ADJ','NOUN','VERB','ADP','ADV','AUX','CCONJ','DET','PRON','PROPN','NUM','SCONJ')"
    )
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    if verify(inp) == inp:
        pattern = inp.split()
        for e in range(len(t) - 1):
            if len(pattern) == 1:
                if pattern[0] in t[e]:
                    l1.append(t[e][0])
                    print(t[e])
                    print(t[e][0])
            elif len(pattern) == 2:
                if pattern[0] in t[e] and pattern[1] in t[e + 1]:
                    l2.append([t[e][0], t[e + 1][0]])
                    print(t[e], "-", t[e + 1])
                    print(t[e][0], t[e + 1][0])
            elif len(pattern) == 3:
                if (
                    pattern[0] in t[e]
                    and pattern[1] in t[e + 1]
                    and pattern[2] in t[e + 2]
                ):
                    l3.append([t[e][0], t[e + 1][0], t[e + 2][0]])
                    print(t[e], "-", t[e + 1], t[e + 2])
                    print(t[e][0], t[e + 1][0], t[e + 2][0])
            elif len(pattern) == 4:
                if (
                    pattern[0] in t[e]
                    and pattern[1] in t[e + 1]
                    and pattern[2] in t[e + 2]
                    and pattern[3] in t[e + 3]
                ):
                    l4.append([t[e][0], t[e + 1][0], t[e + 2][0], t[e + 3][0]])
                    print(t[e], "-", t[e + 1], "-", t[e + 2], "-", t[e + 3])
                    print(t[e][0], t[e + 1][0], t[e + 2][0], t[e + 3][0])

        print("Nombre de matches", len(l1 + l2 + l3 + l4))


def phrasesnominales(dic):
    nlp = spacy.load("fr_core_news_sm")
    l1 = []
    l2 = []
    for e in dic:
        doc = nlp(e.replace("\n", ""))
        l1.append([word.pos_ for word in doc])
        l2.append([word.text for word in doc])
    for e in range(len(l1)):
        if "VERB" not in l1[e]:
            print(" ".join(l2[e]))


def longuermots(doc):
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    for token in doc:
        l1.append(len(token.text))
        l2.append(token.text)

    print("Longueur maximale de mots dans le corpus", max(l1))
    print(l2[l1.index(max(l1))])
    if input("Je veux voir tous les mots de la longueur choisie ") == "oui":
        inp = int(input("Mots de longueur: "))
        if inp in l1:
            for e in range(len(l1)):
                if l1[e] == inp:
                    print(l2[e])
    elif input("Voulez-vous voir les statistiques sur la longueur des mots? ") == "oui":
        for e in l1:
            l3.append((l1.count(e), e))
        for e in sorted(l3):
            if e not in l4:
                l4.append(e)
        l5 = dict(l4)
        r = input("Voulez-vous sauvegarder un nuage de mots? ")
        if r == "oui":
            freqplot(l5)
        r = input("Voulez-vous sauvegarder un graphe?")
        if r == "oui":
            l6 = []
            l7 = []
            for e in l4:
                if e[0] == 1:
                    l6.append(e[0])
                    l7.append(e[1])
                else:
                    l6.append(e[0])
                    l7.append(e[1])

            fig = go.Figure(
                data=[
                    go.Table(
                        header=dict(values=["Quantité", "Longueur du mot"]),
                        cells=dict(values=[l6, l7]),
                    )
                ]
            )
            fig.show()
            fig.write_image("longueur.png")


def contexte(text, dic3):
    w = input("De quel mot voulez-vous voir le contexte? ")
    fenetre = int(input("Combien de mots avant et après le terme choisi? "))
    liste1 = []
    liste2 = []
    liste3 = []
    if w in text:
        for e in range(len(dic3)):
            if dic3[e] == w:
                print(
                    (" ".join(dic3[(e - (fenetre)) : e])),
                    (" ".join(dic3[e : (e + (fenetre) + 1)])),
                )
                liste1.append(" ".join(dic3[(e - (fenetre)) : e]))
                liste2.append(" ".join(dic3[e + 1 : (e + (fenetre) + 1)]))
                liste3.append(dic3[e])
    import plotly.graph_objects as go

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=["Avant", "mot", "après"]),
                cells=dict(values=[liste1, liste3, liste2]),
            )
        ]
    )
    fig.write_image("contexte.png")
    fig.show()


def wordcl(word_freq):
    text = " ".join([(k + " ") * v for k, v in word_freq.items()])

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="nearest", aspect="auto")
    plt.axis("off")
    plt.show(block=True)
    print(
        "Si le nuage de mots ne s'affiche pas sur votre écran, vous le trouverez sauvegardé dans votre dossier actuel."
    )
    plt.savefig("wc.png")


# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()
def freqplot(dictionary):
    # printing most common words
    # the next line sorts the default dict on the values in decreasing  # order and prints the first "to_print".
    to_print = int(input("Combien de mots parmi les plus communs du corpus voulez-vous afficher?"))
    mc = sorted(dictionary.items(), key=lambda k_v: k_v[1], reverse=True)[:to_print]
    # Draw the bart chart
    mc = dict(mc)
    names = list(mc.keys())
    values = list(mc.values())
    plt.bar(range(len(mc)), values, tick_label=names)
    plt.savefig("freq.png")
    plt.show()


def tfidfer(sentences):
    analyzer = clustering.Clustering(
        stopwords=False,
        tfidf=True,
        stemming=True,
        nbclusters=5,
        algo="spectral",
        dist="manhattan",
    )
    dtm, vocab = analyzer.preprocess(sentences)

    print(len(vocab))
    print(vocab)
    print("ETAPE 2 - tf-idf")
    listeTF = []

    for vecteur in dtm:
        res = ""
        for chaine in vecteur:
            res += str(chaine) + " "
        listeTF.append(res)
    print(
        "count sentences :"
        + str(len(sentences))
        + " count listeTF :"
        + str(len(listeTF))
    )
    print("ETAPE 3- écriture du fichier")
    fic_out_vect = open("fichier_tf_idf.txt", "w")
    f = open("vocab.txt", "w")
    nb_sentences = len(sentences)
    for i in range(nb_sentences):
        fic_out_vect.write(listeTF[i] + "\n")
    dic = []
    for i in dtm:
        for i in dtm:
            for e in i:
                for w in vocab:
                    if w not in dic:
                        dic.append(w)
                        dic.append(str(e))
    for e in dic:
        f.write(e)
        f.write("\n")
    f.close()
