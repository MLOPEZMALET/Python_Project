import sys, os

#les deux fichiers sont censés avoir le même nombre de lignes
#le premier fichier contient tous les indices
if (len(sys.argv) > 2):
	fic_ss_ann=open(sys.argv[1], 'r')
	fic_ann=open(sys.argv[2], 'r')
	fic_avec_ann=open(sys.argv[1].replace('.txt', '_annote.txt'), 'w')

	ligne_ss=fic_ss_ann.readline()
	ligne_ann=fic_ann.readline()
	cpt=0
	while(ligne_ss!='' and ligne_ann!=''):
		if(ligne_ss!='\n'):
			segment_ss=ligne_ss.split('\t')[0]
			segment_ann=ligne_ann.split('\t')[0]
			print ('ss: >' +segment_ss.strip(), '< ann: >', segment_ann.strip(), '<')
			if (segment_ss.strip() == segment_ann.strip()):
				fic_avec_ann.write(ligne_ss.replace('\n', '') + '\t' + ligne_ann.split('\t')[2])
		cpt+=1
		ligne_ss=fic_ss_ann.readline()
		ligne_ann=fic_ann.readline()