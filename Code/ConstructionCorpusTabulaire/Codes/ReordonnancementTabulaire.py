import sys, os, csv

if (len(sys.argv) > 0) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	reader=csv.reader(fichier, delimiter='\t', quotechar=None)

	nomFichierNet='ordreAttOK_'+nomFichier
	fichierNet=open(nomFichierNet, 'w')

	cpt=0
	#etaitRetourChariot=False
	for ligne in reader:
		if(len(ligne)==0):
			if(cpt>0)# and etaitRetourChariot==False):
				fichierNet.write('\n')
			#etaitRetourChariot=True
		else:
			fichierNet.write(ligne[0]+'\t'+ligne[1]+'\t'+ligne[2]+'\t'+ligne[6]+'\t'+ligne[26]+'\t'+ligne[27]+'\t'+ligne[5]+'\t'+ligne[7]+'\t'+ligne[3]+'\t'+ligne[4]+'\t'+ligne[8]+'\t'+ligne[9]+'\t'+ligne[10]+'\t'+ligne[11]+'\t'+ligne[12]+'\t'+ligne[13]+'\t'+ligne[14]+'\t'+ligne[15]+'\t'+ligne[16]+'\t'+ligne[17]+'\t'+ligne[18]+'\t'+ligne[19]+'\t'+ligne[20]+'\t'+ligne[22]+'\t'+ligne[21]+'\t'+ligne[23]+'\t'+ligne[25]+'\t'+ligne[24]+'\n')
			#etaitRetourChariot=False
		cpt+=1