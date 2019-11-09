import unicodedata, sys, os

if (len(sys.argv) > 0) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	nomFichierNet='net_'+nomFichier
	fichierNet=open(nomFichierNet, 'w')

	ligne=fichier.readline()
	listeEmoticone=[]
	while(ligne!=''):
		for char in ligne :
			if(unicodedata.category(char) == 'So' or unicodedata.category(char) == 'Lo' or unicodedata.category(char) == 'Sk'): 
				fichierNet.write(' EEMMOOTTIICCOONNEE ')
			else:
				fichierNet.write(char)
		ligne=fichier.readline()
	os.remove(nomFichier)
	os.rename(nomFichierNet, nomFichier)