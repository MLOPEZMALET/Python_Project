import unicodedata, sys, os

if (len(sys.argv) > 0) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	nomFichierNet='net_'+nomFichier
	fichierNet=open(nomFichierNet, 'w')

	ligne=fichier.readline()
	etaitRetourChariot=False
	while(ligne!=''):
		if(ligne!='\n'):
			fichierNet.write(ligne)
			etaitRetourChariot=False
		else:
			if(not etaitRetourChariot):
				fichierNet.write(ligne)
			etaitRetourChariot=True
		ligne=fichier.readline()
	#os.remove(nomFichier)
	os.rename(nomFichierNet, nomFichier)
