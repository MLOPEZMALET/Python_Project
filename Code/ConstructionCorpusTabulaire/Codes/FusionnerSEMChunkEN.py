import unicodedata, sys, os

if (len(sys.argv) > 2) :
	ficChunk=open(sys.argv[1], 'r')
	ficEN=open(sys.argv[2], 'r')
	ficAg=open(sys.argv[3], 'w')

	ligneC=ficChunk.readline()
	ligneE=ficEN.readline()

	while(ligneC!='' and ligneE!=''):
		if(ligneC!='\n' and ligneE!='\n'):
			ficAg.write(ligneC.split('\t')[0]+'\t'+ligneC.split('\t')[1]+'\t'+ligneC.split('\t')[2].replace('\n','')+'\t'+ligneE.split('\t')[2].replace('\n','')+'\n')
		else:
			ficAg.write('\n')
		ligneC=ficChunk.readline()
		ligneE=ficEN.readline()
