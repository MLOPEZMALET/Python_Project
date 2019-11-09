import sys, os

def EcrireSegment(fichier_seg_conll, segment, cpt, listeLigneSegment, theme):
	fichier_seg_conll.write(listeLigneSegment[0].split('\t')[32]+'__'+str(cpt)+'\t'+segment+'\t'+theme+'\n')
	for ligne in listeLigneSegment:
		fichier_seg_conll.write(ligne)
	fichier_seg_conll.write('\n')

if (len(sys.argv) > 0) :
	fichier_conll=open(sys.argv[1], 'r')
	fichier_seg_conll=open(sys.argv[1].replace('.conll', '_segConll.conll'), 'w')
	
	cpt=0
	ID=''
	ID_prece=''
	token=''
	annotation=''
	segment=''
	theme=''
	ancien_segment=''
	listeLigneSegment=[]
	ligne=fichier_conll.readline()
	while(ligne!=''):
		if(ligne!='\n'):
			elm_ligne=ligne.split('\t')
			if(len(elm_ligne)>1): 
				token=elm_ligne[0]
				ID=elm_ligne[32]
				if(ID!=ID_prece):
					cpt=0
				annotation=elm_ligne[len(elm_ligne)-1].replace('\n','')
				if(annotation!='Vide'):
					if(annotation.split('#')[0]=='B'):
						if(segment!=''):
							if (segment != ancien_segment):
								EcrireSegment(fichier_seg_conll, segment, cpt, listeLigneSegment, theme)
							cpt+=1
							ancien_segment=segment
							segment=''
							listeLigneSegment=[]
						theme=annotation.split('#')[1]
						segment+=token+' '
						listeLigneSegment.append(ligne)
					else:
						segment+=token+' '
						listeLigneSegment.append(ligne)
				else:
					if(segment!=''):
						if (segment != ancien_segment):
							EcrireSegment(fichier_seg_conll, segment, cpt, listeLigneSegment, theme)
						listeLigneSegment=[]
						cpt+=1
						ancien_segment=segment
						segment=''
		else:
			if(segment!=''):
				if (segment != ancien_segment):
					EcrireSegment(fichier_seg_conll, segment, cpt, listeLigneSegment, theme)
				listeLigneSegment=[]
				cpt+=1
				ancien_segment=segment
				segment=''
		ID_prece=ID
		ligne=fichier_conll.readline()
	if(segment!=''): #Ecrire le dernier segment!
		if (segment != ancien_segment):
			EcrireSegment(fichier_seg_conll, segment, cpt, listeLigneSegment, theme)
		listeLigneSegment=[]
		cpt+=1
		ancien_segment=segment
		segment=''