#!/usr/bin/python3
# coding: utf-8

"""plotting.py cluster and plot for hackatal2018

Usage:
  plotting.py <infile> <out> [options]

Options:
    --false          only fake news
    --true           only trusted
    -h --help        Display help and exits
"""


import clustering
import clustervisualizer
import csv
import docopt
import json
import sys, os


def main(args):
    sentences=[]
    polarity=[]
    
    fic_in=open(sys.argv[1], 'r')
    #fic_vocab=open('vocabxml.txt', 'w')
    ligne_fic_in=fic_in.readline()
    print ('ETAPE 1 - récuperation des segments et polarité')
    i=1
    while(ligne_fic_in!=''):
        if(ligne_fic_in!='\n'):
            elm_ss_annot=ligne_fic_in.split('\t')
            sentences.append (elm_ss_annot[0])
            polarity.append ( elm_ss_annot[7].replace('\n',''))
            i+=1
        ligne_fic_in=fic_in.readline()
    analyzer = clustering.Clustering(stopwords=True, tfidf=True, stemming=True, nbclusters=5, algo="spectral", dist="manhattan")
    dtm, vocab = analyzer.preprocess(sentences)
    print(len(vocab))
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
    #for chaine in enumerate(vocab):
    #    print (chaine)
    print ('ETAPE 3- écriture du fichier')
    fic_out_vect=open(sys.argv[1].replace('.txt','_vectorised.txt'), 'w')
    nb_sentences =len(sentences)
    for i in  range(nb_sentences):  
        fic_out_vect.write(sentences[i]+'\t')
        fic_out_vect.write(listeTF[i]+'\t')
        fic_out_vect.write(polarity[i]+'\n')
#    dm = analyzer.compute_distances(dtm)
#    y_pred, nb = analyzer.cluster(dm)
#    visu = clustervisualizer.ClusterVisualizer(nb)
#    visu.make_plot(dm, sentences, y_pred, index, output=args["<out>"])
#    data = list(csv.DictReader(open(args["<infile>"]), delimiter="\t", quotechar='"'))
#    results = {}
#    for docid, val in enumerate(y_pred):
#        results[str(val)] = results.get(str(val), []) + [data[docid]]
#    with open(args["<out>"]+".json", "w") as f:
#        json.dump(results, f, indent=2)

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)
