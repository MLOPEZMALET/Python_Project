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
    theme=[]
    token=[]
    lemme=[]
    pos=[]
    chunk=[]
    nb_token=[]
    polarity=[]
    index=[]
    
    fic_in_ss_annot=open(sys.argv[1], 'r')
    ligne_in_ss_annot=fic_in_ss_annot.readline()

    fic_in_avec_annot=open(sys.argv[1].replace('vecteur.txt', 'Annote.txt'))
    ligne_in_avec_annot=fic_in_avec_annot.readline()
    i=1
    while(ligne_in_ss_annot!=''):
        if(ligne_in_ss_annot!='\n'):
            elm_ss_annot=ligne_in_ss_annot.split('\t')
            elm_avec_annot=ligne_in_avec_annot.split('\t')
            sentences.append (elm_ss_annot[0])
            theme.append (elm_ss_annot[1])
            token.append (elm_ss_annot[2])
            lemme.append (elm_ss_annot[3])
            pos.append (elm_ss_annot[4])
            chunk.append (elm_ss_annot[5])
            nb_token.append (elm_ss_annot[6].replace('\n',''))
            polarity.append (elm_avec_annot[2].replace('\n',''))
            index.append (str(i))
            i+=1
        ligne_in_ss_annot=fic_in_ss_annot.readline()
        ligne_in_avec_annot=fic_in_avec_annot.readline()
    print ('coucou0')
    analyzer = clustering.Clustering(stopwords=True, tfidf=False, stemming=True, nbclusters=5, algo="spectral", dist="manhattan")
    dtm, vocab = analyzer.preprocess(sentences)
    print ('coucou1')
    
    listeTF=[]

    for vecteur in dtm:
        res=''
        for chaine in vecteur:  
            res += str(chaine)+' '
        listeTF.append(res)
    print ('coucou2')
    print ('count sentences :'+str(len(sentences))+' count listeTF :'+str(len(listeTF)))
    #for chaine in enumerate(vocab):
    #    print (chaine)
    fic_out_vect=open(sys.argv[1].replace('.txt','_tf.txt'), 'w')
    nb_sentences =len(sentences)
    for i in  range(nb_sentences):  
        fic_out_vect.write(index[i]+'\t')
        fic_out_vect.write(sentences[i]+'\t')
        fic_out_vect.write(theme[i]+'\t')
        fic_out_vect.write(token[i]+'\t')
        fic_out_vect.write(lemme[i]+'\t')
        fic_out_vect.write(pos[i]+'\t')
        fic_out_vect.write(chunk[i]+'\t')
        fic_out_vect.write(nb_token[i]+'\t')
        fic_out_vect.write(polarity[i]+'\t')
        fic_out_vect.write(listeTF[i]+'\n')
    print ('coucou3')
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
