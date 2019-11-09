import csv, sys

def RenvoieIndiceDiscretPosition(numPhrase, tailleAvis) :
	indice=''
	ratio=int(numPhrase)/int(tailleAvis)
	if(numPhrase=='1' or ratio<0.2) :
		indice='debut'
	else:
		if(numPhrase==tailleAvis or ratio>0.8):
			indice='fin'
		else:
			indice='milieu'
	return indice

if (len(sys.argv) > 0) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	reader=csv.reader(fichier, delimiter='\t', quotechar=None)
	nomFichierIndice='indicePos_'+nomFichier
	fichierIndice=open(nomFichierIndice, 'w')

	listeFichier=[]
	for ligne in reader :
		if(len(ligne)==0):
			listeFichier.append('\n')
		else:
			listeFichier.append(ligne)

	nbPhrases=0
	etaitVide=True
	id_avis=''
	listeAvis=[]
	for ligne in listeFichier :
		if (len(ligne)>1) :
			if('___FRONTIERE___' in ligne[0]):
				if(len(listeAvis)>0) : 
					for i in range(0, len(listeAvis)):
						if(listeAvis[i]=='\n'):
							fichierIndice.write('\n')
						else:
							if(len(listeAvis[i])>1):#Ajout
								indicePhrase=''
								for j in range(0, len(listeAvis[i])-1):
									fichierIndice.write(listeAvis[i][j]+'\t')
									indicePhrase=listeAvis[i][j+1]
								fichierIndice.write(id_avis+'\t')
								fichierIndice.write(RenvoieIndiceDiscretPosition(indicePhrase,nbPhrases) + '\n') #listeAvis[len(listeAvis)-1][len(listeAvis[len(listeAvis)-1])-1]) + '\n') 
					nbPhrases=0
					listeAvis=[]
				id_avis=ligne[0].split('___')[2]
			else:
				listePhrase=[]
				if(etaitVide):
					nbPhrases+=1
				for elm in ligne:
					listePhrase.append(elm)
				listePhrase.append(str(nbPhrases))
				listeAvis.append(listePhrase)
				etaitVide=False
		else:
			listeAvis.append('\n')
			etaitVide=True

	if(len(listeAvis)>0) :
		for i in range(0, len(listeAvis)):
			if(listeAvis[i]=='\n'):
				fichierIndice.write('\n')
			else:
				indicePhrase=''
				for j in range(0, len(listeAvis[i])-1):
					fichierIndice.write(listeAvis[i][j]+'\t')
					indicePhrase=listeAvis[i][j+1]
				fichierIndice.write(id_avis+'\t')
				fichierIndice.write(RenvoieIndiceDiscretPosition(indicePhrase,nbPhrases) + '\n')