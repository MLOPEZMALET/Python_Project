# INFO pour lancer le script
#1) Se placer dans le répertoire AdvancedDecision/ConstructionCorpusApprentissage/Codes/
#2) Lancer ce script
#3) donner les noms des corpus (et pas le chemin d'acces) sans extension [le corpus sont dans AdvancedDecision/ConstructionCorpusApprentissage/]

alias python='python3'

# AFFICHAGE
titre=`tput setaf 11`
rouge=`tput setaf 1`
vert=`tput setaf 2`
bleu=`tput setaf 4`
reset=`tput sgr0`

# CORPUS texte, sans l'extension
corpus=$1

cd ./../



echo "\n${titre}######################################################################################################"
echo "                    SECTION 1 : CRÉATION DU CONLL MINIMAL (TALISMANE + SEM)"
echo "######################################################################################################${reset}"
# Ajoutez des colonnes au tabulaire seulement en section 2


# ---> TRANSFORMATION DES EMOTICONES EN EEMMOOTTIICCOONNEE
echo "\n${bleu}• Transformation des émoticones... ${reset}"
echo $corpus'.txt --> '$corpus'.txt'
python ./Codes/RemplacerSmiley.py $corpus'.txt'
if [ -f ./$corpus'.txt' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi


# ---> TALISMANE
echo "\n${bleu}• Talismane : vectorisation du corpus et ajout des attributs morphosyntaxiques... ${reset}"
echo $corpus'.txt --> '$corpus'_talismane.conll'
cd ./../../outils/talismane-distribution-3/
java -Xmx1G -jar -Dconfig.file=talismane-fr-3.0.0b.conf talismane-core-3.0.0b.jar encoding=UTF8 tokenFilters="./filters_token/identifiant.txt" inFile=./../../Segmentation_thematique_CRF/ConstructionCorpusTabulaire/$corpus'.txt' outFile=./../../Segmentation_thematique_CRF/ConstructionCorpusTabulaire/$corpus'_talismane.conll'
cd ./../../Segmentation_thematique_CRF/ConstructionCorpusTabulaire/
if [ -f ./$corpus'_talismane.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi
