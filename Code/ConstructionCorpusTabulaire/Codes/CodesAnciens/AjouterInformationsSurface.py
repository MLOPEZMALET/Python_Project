import unicodedata, sys, os, csv

if (len(sys.argv) > 0) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	reader=csv.reader(fichier, delimiter='\t', quotechar=None)

	nomFichierNet='net_'+nomFichier
	fichierNet=open(nomFichierNet, 'w')

	for ligne in reader:
		if(len(ligne)>0):
			token=ligne[0]
			fichierNet.write(token+'\t'+str(len(token))+'\t')
			for i in range(1,len(ligne)-2):
				fichierNet.write(ligne[i]+'\t')
			fichierNet.write(ligne[len(ligne)-1]+'\n')
		else:
			fichierNet.write('\n')
		
	os.remove(nomFichier)
	os.rename(nomFichierNet, nomFichier)