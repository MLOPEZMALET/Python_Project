import sys, os

def sans_prefixe(chaine):
	nvChaine=chaine.replace('B#', '')
	nvChaine=nvChaine.replace('I#', '')
	return nvChaine

def BILOU(chaine):
	listeElmExemple=[]
	tokens=chaine.split('\n')
	for t in tokens:
		att=t.split('\t')
		listeElmExemple.append(att)

	listesOK=[]
	for i in range(0, len(listeElmExemple)):
		j=0
		listeOK=[]
		while(j<len(listeElmExemple[i])-1):
			listeOK.append(listeElmExemple[i][j])
			j+=1
		if('I#' in listeElmExemple[i][len(listeElmExemple[i])-1] and listeElmExemple[i][len(listeElmExemple[i])-1]!=listeElmExemple[i+1][len(listeElmExemple[i+1])-1]):
			listeOK.append(listeElmExemple[i][len(listeElmExemple[i])-1].replace('I#', 'L#'))
		else:
			listeOK.append(listeElmExemple[i][len(listeElmExemple[i])-1])
		listesOK.append(listeOK)

	nvChaine=''
	for i in range(0, len(listesOK)):
		for j in range(0, len(listesOK[i])):
			nvChaine+=listesOK[i][j]+'\t'
		nvChaine+=listesOK[i][len(listesOK[i])-1]+'\n'

	return nvChaine



if (len(sys.argv) > 1) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	notation=sys.argv[2] #BIO, BILOU et sans_prefixe

	listeExemplesCRF=[]
	exemple=''
	ligne=fichier.readline()
	while(ligne!=''):
		if(ligne!='\n'):
			exemple+=ligne
		else:
			listeExemplesCRF.append(exemple)
			exemple=''
		ligne=fichier.readline()
		if(ligne==''):
			listeExemplesCRF.append(exemple)

	nvFichier=open(notation+'_'+nomFichier, 'w')
	for ex in listeExemplesCRF:
		if(notation=='BILOU'):
			nvFichier.write(BILOU(ex))
		if(notation=='sans_prefixe'):
			nvFichier.write(sans_prefixe(ex)+'\n')
	nvFichier.close()
		