# INFO pour lancer le script
#1) Se placer dans le répertoire /ConstructionCorpusTabulaire/Codes/
#2) Lancer ce script
#3) donner les noms des corpus (et pas le chemin d'acces) sans extension [le corpus doit se trouver dans /ConstructionCorpusTabulaire

# CORPUS texte, sans l'extension
corpus=$1

echo "\n${titre}######################################################################################################"
echo "                    SECTION 1 : CRÉATION DU CONLL MINIMAL (TALISMANE + SEM)"
echo "######################################################################################################${reset}"
# Ajoutez des colonnes au tabulaire seulement en section 2

# ---> TALISMANE
echo "\n${bleu}• Talismane : vectorisation du corpus et ajout des attributs morphosyntaxiques... ${reset}"
echo $corpus'.txt --> '$corpus'_talismane.txt'
cd ./../../../../outils/talismane-distribution-3/
java -Xmx1G -jar -Dconfig.file=talismane-fr-3.0.0b.conf talismane-core-3.0.0b.jar encoding=UTF8 inFile=./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/$corpus'.txt' outFile=./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/$corpus'_talismane.txt'
cd ./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/
if [ -f ./$corpus'_talismane.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi