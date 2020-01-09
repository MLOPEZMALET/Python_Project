#!/usr/bin/python3
# coding: utf-8

"""inspired by hackatal2018
"""


import clustering
import clustervisualizer
import csv
import json
import sys, os


def tfidfer(sentences):
    analyzer = clustering.Clustering(stopwords=False, tfidf=True, stemming=True, nbclusters=5, algo="spectral", dist="manhattan")
    dtm, vocab = analyzer.preprocess(sentences)
    print(len(vocab))
    print(vocab)
    #fic_vocab.write("<?xml version='1.0' encoding='UTF-8'?\n")
    #fic_vocab.write("<voc>\n")
    #print(dic[:40])
    #dic=[]
    #for i in dtm[:10]:
        #for i in dtm:
            #for e in i:
                #for w in vocab:
                    #dic.append(w)
                    #dic.append(e)
    #print(len(dic))
    #for e in dic:
        #fic_vocab.write(e)
        #fic_vocab.write(',')
    #import pandas as pd
    #import numpy as np
    #df = pd.DataFrame(dtm, columns = vocab)
    #print(df[:100])
    #df.to_string(fic_vocab)
    #fic_vocab.close()
    print ('ETAPE 2 - tf-idf')
    listeTF=[]

    for vecteur in dtm:
        res=''
        for chaine in vecteur:  
            res += str(chaine)+' '
        listeTF.append(res)
    print ('count sentences :'+str(len(sentences))+' count listeTF :'+str(len(listeTF)))
    print ('ETAPE 3- écriture du fichier')
    fic_out_vect=open("fichier_tf_idf.txt", 'w')
    f=open("vocab",'w')
    for i in vocab:
        f.write(i+'\n')
    nb_sentences =len(sentences)
    for i in  range(nb_sentences):
        fic_out_vect.write(listeTF[i]+'\n')

    dm = analyzer.compute_distances(dtm)
    y_pred, nb = analyzer.cluster(dm)
    visu = clustervisualizer.ClusterVisualizer(nb)
    visu.make_plot(dm, sentences, y_pred, index, output=sentences["<out>"])
    data = list(csv.DictReader(open(sentences["<infile>"]), delimiter="\t", quotechar='"'))
    results = {}
#    for docid, val in enumerate(y_pred):
#        results[str(val)] = results.get(str(val), []) + [data[docid]]
#    with open(args["<out>"]+".json", "w") as f:
#        json.dump(results, f, indent=2)
