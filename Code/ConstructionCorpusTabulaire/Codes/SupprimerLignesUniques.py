import unicodedata, sys, os

if (len(sys.argv) > 0) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	nomFichierNet='ligneUniqOK_'+nomFichier
	fichierNet=open(nomFichierNet, 'w')

	conll=fichier.readlines()
	etaitLigneVide=False
	i=0
	while (i<len(conll)-1) :
		if(conll[i]!='\n'):
			if(not (conll[i-1]=='\n' and conll[i+1]=='\n')) :
				fichierNet.write(conll[i])
			etaitLigneVide=False
		else:
			if(etaitLigneVide==False):
				fichierNet.write(conll[i])
			etaitLigneVide=True
		i+=1
	fichierNet.write(conll[len(conll)-1])