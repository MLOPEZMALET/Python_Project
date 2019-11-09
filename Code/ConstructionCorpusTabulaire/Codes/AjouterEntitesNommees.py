import unicodedata, sys, os

if (len(sys.argv) > 1) :
	tabulaire=open(sys.argv[1], 'r')
	resEN=open(sys.argv[2], 'r')
	tabulaireEN=open('en_'+sys.argv[1], 'w')

	ligneTabulaire=tabulaire.readline()
	ligneEN=resEN.readline()
	while(ligneTabulaire!='' and ligneEN!=''):
		if(ligneTabulaire!='\n' and ligneEN!='\n'):
			for att in ligneTabulaire.split('\t') :
				tabulaireEN.write(att.replace('\n', '')+'\t')
			tabulaireEN.write(ligneEN.split('\t')[len(ligneEN.split('\t'))-1].replace('\n','')+'\n')
		else:
			tabulaireEN.write('\n')
		ligneTabulaire=tabulaire.readline()
		ligneEN=resEN.readline()