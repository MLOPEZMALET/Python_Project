import sys, os, csv

if (len(sys.argv) > 2) :
	fichierCorpus=open(sys.argv[1], 'r')
	reader=csv.reader(fichierCorpus, delimiter='\t', quotechar=None)

	fichierTT1=open(sys.argv[2], 'r')
	listeLigneTT1=fichierTT1.readlines()
	cpt1=0
	fichierTT2=open(sys.argv[3], 'r')
	listeLigneTT2=fichierTT2.readlines()
	cpt2=0

	with open('tt_'+sys.argv[1], 'w') as fic:
		for ligne in reader:
			if(len(ligne)>0) :
				for i in range(0, len(ligne)) :
					fic.write(ligne[i]+'\t')
				ligneTT1=listeLigneTT1[cpt1].split('\t')
				POS1=ligneTT1[1].replace('\n', '')
				ligneTT2=listeLigneTT2[cpt2].split('\t')
				POS2=ligneTT2[1].replace('\n', '')
				fic.write(POS1+'\t'+POS2+'\n')
				cpt1+=1
				cpt2+=1
			else:
				fic.write('\n')
