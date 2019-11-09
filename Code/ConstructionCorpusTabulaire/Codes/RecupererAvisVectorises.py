import sys, csv

if (len(sys.argv) > 1) :
    nomCorpusVect=sys.argv[1]+'_talismane.conll'
    fichier=open(nomCorpusVect, 'r')
    nomCorpusVect_Net=sys.argv[1]+'_vect.conll'
    fichierNet=open(nomCorpusVect_Net, 'w')

    reader=csv.reader(fichier, delimiter='\t', quotechar=None)
    nbLignesVides=0
    for ligne in reader:
        if (len(ligne)>0):
            fichierNet.write(ligne[1]+'\n')
        else:
            fichierNet.write('\n')
    fichier.close()
    fichierNet.close()
