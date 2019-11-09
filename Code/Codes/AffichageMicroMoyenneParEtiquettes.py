import sys, os, re, csv

if (len(sys.argv) > 0) :
	nom=sys.argv[1]
	fic=open(nom, 'r')

	listeAnnotations=[]
	ligne = fic.readline()
	# On récupère toutes les étiquettes différentes
	while (ligne != ''):
		ligne=ligne.replace('\n', '').split('\t')
		if(ligne[len(ligne)-2] not in listeAnnotations):
			listeAnnotations.append(ligne[len(ligne)-2])
		if(ligne[len(ligne)-1] not in listeAnnotations):
			listeAnnotations.append(ligne[len(ligne)-1])
		ligne = fic.readline()
	fic.close()

	# Création d'un dictionnaire qui aura pour clef les étiquettes et pour valeur les métriques associées
	dicoAnnotations={}
	nb=0
	for etiq in listeAnnotations : 
		nbAnn=0
		nbBonnesAnn=0
		nbAnnAttendues=0
		nbAnnAttribuees=0
		fic=open(nom, 'r')
		ligne = fic.readline()
		while (ligne != ''):
			ligne=ligne.replace('\n', '').split('\t')
			if(ligne[len(ligne)-2]==etiq):
				nbAnn+=1
			if(ligne[len(ligne)-2]==ligne[len(ligne)-1] and ligne[len(ligne)-2]==etiq) :
				nbBonnesAnn+=1
			if(ligne[len(ligne)-2]==etiq):
				nbAnnAttendues+=1
			if(ligne[len(ligne)-1]==etiq):
				nbAnnAttribuees+=1
			ligne = fic.readline()
		precision=(nbBonnesAnn/nbAnnAttribuees)*100 if nbAnnAttribuees!=0 else -1
		rappel=(nbBonnesAnn/nbAnnAttendues)*100 if nbAnnAttendues!=0 else -1
		fmesure=2*(precision*rappel)/(precision+rappel) if (precision+rappel)!=0 else -1
		dicoAnnotations[etiq]=[nbAnn, precision, rappel, fmesure]
		fic.close()

	
	nb=0
	p=0
	r=0
	fm=0
	for etiq in dicoAnnotations.keys():
		if(dicoAnnotations[etiq][0]!=-1 and dicoAnnotations[etiq][1]!=-1):
			p+=dicoAnnotations[etiq][0]*dicoAnnotations[etiq][1]
		if(dicoAnnotations[etiq][0]!=-1 and dicoAnnotations[etiq][2]!= -1):
			r+=dicoAnnotations[etiq][0]*dicoAnnotations[etiq][2]
		if(dicoAnnotations[etiq][0]!=-1 and dicoAnnotations[etiq][3]!=-1):
			fm+=dicoAnnotations[etiq][0]*dicoAnnotations[etiq][3]
		nb+=dicoAnnotations[etiq][0]

	pp=round(p/nb,2)
	rr=round(r/nb,2)
	#fmesure=str(round(fm/nb,2)).replace('.',',')
	fmesure=str(round(2*(pp*rr)/(pp+rr) ,2)).replace('.',',')

	#print('\nmicro-average\t'+pp+'\t'+rr+'\t'+fmesure)
	print('micro-average\t'+str(pp).replace('.',',')+'\t'+str(rr).replace('.',',')+'\t'+fmesure)
	csvfile=open('micro.txt', 'a',encoding='utf-8')
	csvfile.write(str(pp).replace('.',',')+'\t'+str(rr).replace('.',',')+'\t'+fmesure+'\t')
	csvfile.close()
