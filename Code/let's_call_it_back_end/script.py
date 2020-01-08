#!/usr/bin/env python
# coding: utf-8
import spacy
import instruments
import re
import sys
import plotly.graph_objects as go
nlp = spacy.load('fr_core_news_sm')
stop=''
#on ouvre le fichier et on stoque le contenu dans une liste
print("Si c'est un corpus de plusieurs documents, veillez les separer par ***")
print("Veillez répondre aux questions yes or no en minuscule")
with open(sys.argv[1],'r',encoding='utf-8') as corpus:
    co=corpus.readlines()
    dic=[]
    for e in co:
        e.split('\n')
        dic.append(e)
#on fait du nettoyage
dic2=[]
for e in co:
    for i in e.replace('\n','').replace('?','').replace('!','').replace('.','').replace('’','').replace(',','').split():
        dic2.append(i)
#si on est interessé au niveau des phrases dic - sans tokenization, dicc avec tokenization
dicc=[[e.replace('\n','').split()]for e in dic]
dic3=[]
for e in co:
    for i in e.split():
        dic3.append(i)
text=' '.join(dic2)
###for pos-tags
doc = nlp(text)
###for tfidf
r=text.split('***')
####les questions#####
while stop!='yes':
    if input('Vous voullez voir fréquence de mots? ')=='yes':
        motvidesquestion=input('On consiedere les mots vides?yes/no ')
        if 'no' in motvidesquestion:
            listvide=open('stopwords.txt','r',encoding='utf-8')
            lv=listvide.readlines()
            dicvide=[]
            for e in lv:
                dicvide.append(e.replace('\n','').replace('\t',''))
            liste2=instruments.tokenizer(text)
            #lenght totale
            print(len(liste2)," - longueur du corpus")
            liste4=[e for e in liste2 if e not in dicvide]
            #combien de mots vide?
            print(len(liste2)-len(liste4)," - mots vides")
            #lenght sans mots vides
            print(len(liste4)," - sans mots vides")
            instruments.frequency(liste4)
        elif 'yes' in motvidesquestion:
            liste2=instruments.tokenizer(text)
            instruments.frequency(liste2)
    elif input('Vous voullez voir les patrons morphosyntaxiques? ')=='yes':
            instruments.patterngiver(doc)
    elif input('Vous voullez voir la statistique de parties de discours? ')=='yes':
        instruments.posstats(doc)
    elif input('Vous voullez voir la statistique de signes de ponctuation? ')=='yes':
        #combien de phrases interogatives?
        cptinterog=0
        for e in dicc:
            for i in e:
                if '?' in i:
                    cptinterog+=1
        print(cptinterog,"- ?")
        #combien de phrases exclamatives?
        cptex=0
        for e in dic3:
            for i in e:
                if '!' in i:
                    cptex+=1
        print(cptex,"- !")
        #combien de phrases avec points de suspension?
        cptpts=0
        for e in dic3:
            if '...' in e:
                cptpts+=1
        print(cptpts,"- ...")
    elif input('Vous voullez voir la specificité du mot? ')=='yes':
        instruments.specificity(text)
    elif input('Vous voullez voir les phrases nominales? ')=='yes':
        instruments.phrasesnominales(dic)
    elif input('Vous voullez voir la statistique de longueur des mots? ')=='yes':
        instruments.longuermots(doc)
    elif input('Vous voullez voir le contexte des mots que vous indiquez? ')=='yes':
        instruments.contexte(text,dic3)
    elif input('Vous voullez voir tf-idf? ')=='yes':
        instruments.tfidfer(r)
    stop=input('if you want to stop écris yes, sinon no')