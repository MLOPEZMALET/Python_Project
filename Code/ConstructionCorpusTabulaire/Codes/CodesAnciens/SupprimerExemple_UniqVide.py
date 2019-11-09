import unicodedata, sys, os, csv

if (len(sys.argv) > 0) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	reader=csv.reader(fichier, delimiter='\t', quotechar=None)

	nomFichierNet='net_'+nomFichier
	fichierNet=open(nomFichierNet, 'w')

	listeElmExemple=[]
	for ligne in reader:
		if(len(ligne)>0):
			listeElmExemple.append(ligne)
		else:
			existenceDiaise=False
			for ligne in listeElmExemple:
				if('#' in ligne[len(ligne)-1]):
					existenceDiaise=True
			if(existenceDiaise==True):
				for ligne in listeElmExemple:
					for i in range(0, len(ligne)-2):
						fichierNet.write(ligne[i]+'\t')
					fichierNet.write(ligne[len(ligne)-1]+'\n')
				fichierNet.write('\n')
			listeElmExemple=[]
		
	os.remove(nomFichier)
	os.rename(nomFichierNet, nomFichier)