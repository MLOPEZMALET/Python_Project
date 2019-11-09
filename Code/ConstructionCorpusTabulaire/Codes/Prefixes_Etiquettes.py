import sys, os

def ModifieValeurListe(liste, indice, nvValeur):
	nvListe=[]
	for i in range(0, len(liste)):
		if(i==indice):
			nvListe.append(nvValeur)
		else:
			nvListe.append(liste[i])
	return nvListe

def EcrireExemple(fichier, exemple):
	for ligne in exemple :
		for i in range(0, len(ligne)-1) :
			fichier.write(ligne[i]+'\t')
		fichier.write(ligne[len(ligne)-1]+'\n')
	fichier.write('\n')

def VIDE(exemple):
	nvEx=[]
	for ligne in exemple:
		nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, ligne[len(ligne)-1].replace('B#', '').replace('I#', '').replace('L#', '')))
	return nvEx


def BIO(exemple):
	nvEx=[]
	ann_prec=''
	for ligne in exemple :
		ann=ligne[len(ligne)-1]
		if(ann=='Vide'):
			nvEx.append([x for x in ligne])
		else:
			if(not '#' in ann): #ie pas de préfixe
				if (ann_prec=='' or ann_prec=='VIDE'):
					nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'B#'+ann))
				else:
					if(ann_prec==ann):
						nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'I#'+ann))
					else:
						nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'B#'+ann))
			else: #ie BIO ou BILOU
				if('#' in ann_prec):
					if(ann_prec.split('#')[1]!=ann.split('#')[1]): #pas le même thème
						nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'B#'+ann.split('#')[1]))
					else:
						nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'I#'+ann.split('#')[1]))
				else:
					nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'B#'+ann.split('#')[1]))
		ann_prec=ann
	return nvEx

def BILOU(exemple):
	nvEx=[]
	ann_prec=''
	for i in range(0, len(exemple)):
		ligne=exemple[i]
		ann=ligne[len(ligne)-1]
		ann_suiv=exemple[i+1][len(exemple[i+1])-1] if i < len(exemple)-1 else ''
		if(ann=='Vide'):
			nvEx.append([x for x in ligne])
		else:
			if(not '#' in ann): #ie pas de préfixe
				if (ann_prec=='' or ann_prec=='VIDE'):
					nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'B#'+ann))
				else:
					if(ann_prec==ann):
						if(ann==ann_suiv):
							nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'I#'+ann))
						else:
							nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'L#'+ann))
					else:
						nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'B#'+ann))
			else: #ie BIO ou BILOU
				if('#' in ann_prec):
					if(ann_prec.split('#')[1]!=ann.split('#')[1]): #pas le même thème
						nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'B#'+ann.split('#')[1]))
					else:
						if('#' in ann_suiv) :
							if(ann.split('#')[1]==ann_suiv.split('#')[1]):
								nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'I#'+ann.split('#')[1]))
							else:
								nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'L#'+ann.split('#')[1]))
						else:
							nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'L#'+ann.split('#')[1]))
				else:
					nvEx.append(ModifieValeurListe(ligne, len(ligne)-1, 'B#'+ann.split('#')[1]))
		ann_prec=ann

	return nvEx



if (len(sys.argv) > 1) :
	nomFichier=sys.argv[1]
	fichier=open(nomFichier, 'r')
	notation=sys.argv[2] #BIO, BILOU et VIDE

	listeExemplesCRF=[] #Liste des exemples
	exemple=[] #Liste des lignes de chaque exemple
	ligne=fichier.readline()
	while(ligne!=''):
		if(ligne!='\n'):
			exemple.append(ligne.replace('\n', '').split('\t'))
		else:
			listeExemplesCRF.append(exemple)
			exemple=[]
		ligne=fichier.readline()
		if(ligne==''):
			listeExemplesCRF.append(exemple)

	nom_nvFichier='.'+nomFichier.split('.')[len(nomFichier.split('.'))-2]+'_'+notation+'.'+nomFichier.split('.')[len(nomFichier.split('.'))-1]
	nvFichier=open(nom_nvFichier, 'w')
	for ex in listeExemplesCRF:
		if(notation=='VIDE'):
			EcrireExemple(nvFichier, VIDE(ex))
		if(notation=='BIO'):
			EcrireExemple(nvFichier, BIO(ex))
		if(notation=='BILOU'):
			EcrireExemple(nvFichier, BILOU(ex))
	
	os.remove(nomFichier)
	os.rename(nom_nvFichier,nomFichier)
		