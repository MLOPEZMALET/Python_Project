#coding: utf-8

import sys, csv, os

def ContientID(chaine):
	resChar=False
	resChiffre=False
	for caractere in chaine :
		if (caractere=='_'):
			resChar=True
		if (caractere in '0123456789'):
			resChiffre=True
	return (resChar and resChiffre)

def ContientPonctuation(chaine):
	res=False
	for caractere in chaine :
		if (caractere in ',?;.:/=+%*-_)![]'):
			res=True
	return res

def SupprimeRetourChariot(chaine):
	if(chaine!='\n'):
		return chaine[0:len(chaine)-1]
	else:
		return '\n'
def ContientEspace(chaine):
	if (' ' in chaine):
		return True
	else:
		return False

if (len(sys.argv) > 3) :
	#AJUSTEMENT GLOBAL DES LIGNES SEM ET TALISMANE (VIA LE FICHIER _VECT)
	nomFichierVect=sys.argv[1]
	fichierVect=open(nomFichierVect, 'r')
	nomFichierSEM=sys.argv[2]
	fichierSEM=open(nomFichierSEM, 'r')
	listeLignesFichierVect=fichierVect.readlines()
	listeLignesFichierSEM=fichierSEM.readlines()

	nomFichierSEM_net='net_'+sys.argv[2]
	fichierSEM_net=open(nomFichierSEM_net,'w')


	cptVect=0
	cptSEM=0
	while(cptVect<len(listeLignesFichierVect) and cptSEM<len(listeLignesFichierSEM)):
		ligneVect=SupprimeRetourChariot(listeLignesFichierVect[cptVect])
		ligneSEM=SupprimeRetourChariot(listeLignesFichierSEM[cptSEM])
		if(ContientPonctuation(ligneVect)):
			if(ContientID(ligneVect)):
				fichierSEM_net.write(ligneVect+'\t'+'ID'+'\t'+'O'+'\n')
				cptVect+=1
				cptSEM+=1
			else:
				fichierSEM_net.write(ligneVect+'\t'+'PONCT'+'\t'+'O'+'\n')
				cptVect+=1
				cptSEM+=1
		else:
			if(ligneVect=='\n'):
				fichierSEM_net.write('\n')
				cptVect+=1
				cptSEM+=1
			else:
				if(ContientEspace(ligneVect)):
					fichierSEM_net.write(ligneVect+'\t'+'POStag_T'+'\t'+'O'+'\t'+'O'+'\n')
					cptVect+=1
					cptSEM+=1
				else:
					#Recherche de l'élément vers le haut (indice négatif) 
					cptNeg=0
					while(ligneVect not in SupprimeRetourChariot(listeLignesFichierSEM[cptSEM-cptNeg]) and cptSEM-cptNeg>1) :
						cptNeg+=1
					resNeg=False
					if(ligneVect in SupprimeRetourChariot(listeLignesFichierSEM[cptSEM-cptNeg])):
						resNeg=True

					#Recherche de l'élément vers le bas (indice positif)
					cptPos=0
					while(ligneVect not in SupprimeRetourChariot(listeLignesFichierSEM[cptSEM+cptPos]) and cptSEM+cptPos<len(listeLignesFichierSEM)-1) :
						cptPos+=1
					resPos=False
					if(ligneVect in SupprimeRetourChariot(listeLignesFichierSEM[cptSEM+cptPos])):
						resPos=True

					#Ecriture
					if(resNeg==True and resPos==False):
						cptSEM=cptSEM-cptNeg
						fichierSEM_net.write(SupprimeRetourChariot(listeLignesFichierSEM[cptSEM])+'\n')
					if(resNeg==False and resPos==True):
						cptSEM=cptSEM+cptPos
						fichierSEM_net.write(SupprimeRetourChariot(listeLignesFichierSEM[cptSEM])+'\n')
					if(resNeg==True and resPos==True):
						if(cptNeg<=cptPos):
							cptSEM=cptSEM-cptNeg
							fichierSEM_net.write(SupprimeRetourChariot(listeLignesFichierSEM[cptSEM])+'\n')
						else:
							cptSEM=cptSEM+cptPos
							fichierSEM_net.write(SupprimeRetourChariot(listeLignesFichierSEM[cptSEM])+'\n')
					if(resNeg==False and resPos==False):
						fichierSEM_net.write(ligneVect+'\t'+'POStag_T'+'\t'+'O'+'\t'+'O'+'\n')
					cptSEM+=1
					cptVect+=1
	fichierVect.close()
	fichierSEM.close()
	fichierSEM_net.close()

	#INTEGRATION DES INFORMATIONS SEM ET TALISMANE
	nomFichierTalismane=sys.argv[3]
	fichierTalismane=open(nomFichierTalismane, 'r')
	ficSEM_net=open(nomFichierSEM_net, 'r')
	nomFichierSEM_net_uni='uni_net_'+sys.argv[2]
	fichierSEM_uniformise=open(nomFichierSEM_net_uni, 'w')

	listeElmFichierTalismane=fichierTalismane.readlines()
	listeElmFichierSEM_net=ficSEM_net.readlines()
	i=0
	while(i<len(listeElmFichierSEM_net)):
		ligneSEM_net=SupprimeRetourChariot(listeElmFichierSEM_net[i])
		listeElmLigneSEM=ligneSEM_net.split('\t')
		ligneTalisme=SupprimeRetourChariot(listeElmFichierTalismane[i])
		listeElmLigneTalismane=ligneTalisme.split('\t')
		if(ligneSEM_net=='\n'):
			fichierSEM_uniformise.write('\n')
		else:
			if ('POStag_T' not in ligneSEM_net):
				fichierSEM_uniformise.write(ligneTalisme+'\t'+listeElmLigneSEM[len(listeElmLigneSEM)-3]+'\t'+listeElmLigneSEM[len(listeElmLigneSEM)-2]+'\t'+listeElmLigneSEM[len(listeElmLigneSEM)-1]+'\n')
			else:
				fichierSEM_uniformise.write(ligneTalisme+'\t'+listeElmLigneTalismane[3]+'\t'+listeElmLigneSEM[len(listeElmLigneSEM)-2]+'\t'+listeElmLigneSEM[len(listeElmLigneSEM)-1]+'\n')
		i+=1
	fichierTalismane.close()
	ficSEM_net.close()
	fichierSEM_uniformise.close()

	#SUPPRESSION DES INFORMATIONS INUTILES
	nomFichierAggrege='uni_net_'+sys.argv[2]
	fichierAggrege=open(nomFichierAggrege, 'r')
	reader=csv.reader(fichierAggrege, delimiter='\t', quotechar=None)
	nomFichierAggrege_net=sys.argv[4]
	fichierAggrege_net=open(nomFichierAggrege_net, 'w')

	for ligne in reader:
		if(len(ligne)>12):
			fichierAggrege_net.write(ligne[0]+'\t'+ligne[1]+'\t'+ligne[2]+'\t'+ligne[3]+'\t'+ligne[6]+'\t'+ligne[7]+'\t'+ligne[10]+'\t'+ligne[11]+'\t'+ligne[12]+'\n')
		else:
			fichierAggrege_net.write('\n')
	fichierAggrege.close()
	fichierAggrege_net.close()

	#SUPPRESSION DES FICHIERS TEMPORAIRES AYANT AIDES A LA CONSTRUCTION DE L'AGGREGATION
	#os.remove(nomFichierSEM_net)
	#os.remove(nomFichierSEM_net_uni)