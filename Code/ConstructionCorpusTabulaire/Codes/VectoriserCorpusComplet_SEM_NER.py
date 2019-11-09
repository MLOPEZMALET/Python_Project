import sys, os, csv

if (len(sys.argv) > 1) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	reader=csv.reader(fichier, delimiter='\t', quotechar=None)

	nomFichierNet=sys.argv[2]
	fichierNet=open(nomFichierNet, 'w')

	for ligne in reader :
		if(len(ligne)>0):
			fichierNet.write(ligne[1]+'\n')
		else:
			fichierNet.write('\n')