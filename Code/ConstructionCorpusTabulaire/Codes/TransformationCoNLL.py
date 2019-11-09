import sys, csv

def SupprimerEspace(chaine):
	nvChaine=''
	for char in chaine:
		if (char!= ' '):
			nvChaine+=char
		else:
			nvChaine+='_'
	return nvChaine

if (len(sys.argv) > 1) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	reader=csv.reader(fichier, delimiter='\t', quotechar=None)
	nomFichier_conll='conllOK_'+nomFichier
	fichier_conll=open(nomFichier_conll, 'w')

	for ligne in reader :
		if (len(ligne)>0):
			i=1
			while(i<len(ligne)-1):
				fichier_conll.write(SupprimerEspace(ligne[i])+'\t')
				i+=1
			fichier_conll.write(SupprimerEspace(ligne[len(ligne)-1])+'\n')
		else:
			fichier_conll.write('\n')

	fichier.close()
	fichier_conll.close()