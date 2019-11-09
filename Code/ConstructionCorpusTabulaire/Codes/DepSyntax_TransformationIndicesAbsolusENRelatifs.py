import sys, csv

if (len(sys.argv) > 1) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	reader=csv.reader(fichier, delimiter='\t', quotechar=None)

	nomFichierDepRel='depRel_'+sys.argv[1]
	fichierDepRel=open(nomFichierDepRel, 'a')

	listeElmPhrase=[] #liste de listes. Liste des attributs de chaque tokens, attributs repertories en liste
	cpt=0
	for ligne in reader :
		if (len(ligne)>0):
			listeElmPhrase.append([att for att in ligne])
		else:
			i=0
			while(i<len(listeElmPhrase)):
				indiceAbs=listeElmPhrase[i][4]
				indiceRel='0'
				j=0
				while(j<len(listeElmPhrase)):
					if(listeElmPhrase[j][0]==indiceAbs):
						indiceRel=str(j-i)
					j+=1
				fichierDepRel.write(listeElmPhrase[i][0]+'\t'+listeElmPhrase[i][1]+'\t'+listeElmPhrase[i][2]+'\t'+listeElmPhrase[i][3]+'\t'+listeElmPhrase[i][4]+'\t'+indiceRel+'\t'+listeElmPhrase[i][5]+'\t'+listeElmPhrase[i][6]+'\t'+listeElmPhrase[i][7]+'\t'+listeElmPhrase[i][8]+'\n')
				i+=1

			fichierDepRel.write('\n')
			listeElmPhrase=[]
		cpt+=1
	if(len(listeElmPhrase)>0):
		i=0
		while(i<len(listeElmPhrase)):
			indiceAbs=listeElmPhrase[i][4]
			indiceRel='0'
			j=0
			while(j<len(listeElmPhrase)):
				if(listeElmPhrase[j][0]==indiceAbs):
					indiceRel=str(j-i)
				j+=1
			fichierDepRel.write(listeElmPhrase[i][0]+'\t'+listeElmPhrase[i][1]+'\t'+listeElmPhrase[i][2]+'\t'+listeElmPhrase[i][3]+'\t'+listeElmPhrase[i][4]+'\t'+indiceRel+'\t'+listeElmPhrase[i][5]+'\t'+listeElmPhrase[i][6]+'\t'+listeElmPhrase[i][7]+'\t'+listeElmPhrase[i][8]+'\n')
			i+=1
		fichierDepRel.write('\n')
		
	fichier.close()
	fichierDepRel.close()