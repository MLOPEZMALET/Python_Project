#INFO
#1) Se placer dans le répertoire AdvancedDecision/ConstructionCorpusApprentissage/Codes/
#2) Lancer ce script
#3) donner les noms des corpus (et pas le chemin d'acces) sans extansion [le corpus sont dans AdvancedDecision/ConstructionCorpusApprentissage/]
rouge=`tput setaf 1`
vert=`tput setaf 2`
bleu=`tput setaf 4`
reset=`tput sgr0`
corpus=$1 #nom du corpus sans l'extansion
corpusAnnote=$2 #nom du fichier complet, avec l'extension

alias python='python3'


#SUPPRESSION DES EMOTICONES
echo "\n${bleu}####################################"
echo "ETAPE 0 : SUPPRESSION DES EMOTICONES"
echo "####################################${reset}"
echo '\n--> Modification du fichier '$corpus'.txt\n'
cd ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/
python ./Codes/RemplacerSmiley.py $corpus'.txt'

if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$corpus'.txt' ]; then
	echo "\n${vert}--> Terminé.${reset}\n"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi





#TALISMANE
#Segmentation en phrases et en mots (vectorisation)
#Entree : corpus d'avis vierges
#Sortie : CoNLL : IndiceToken, Token, Lemme, POS, SyntacticHead, SyntacticLabel
echo "\n${bleu}####################################################################"
echo "ETAPE 1 : VECTORISATION DES AVIS ET ANALYSES SYNTAXIQUES (TALISMANE)"
echo "####################################################################${reset}"
echo '\n--> Création du fichier '$corpus'_talismane.txt\n'
cd ~/../../Applications/talismane-distribution-3/
TALISMANEFichierSortie=$corpus'_talismane.txt'
java -Xmx1G -jar -Dconfig.file=talismane-fr-3.0.0b.conf talismane-core-3.0.0b.jar encoding=UTF8 tokenFilters="./filters_token/identifiant.txt" inFile=./../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$corpus.txt outFile=./../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$TALISMANEFichierSortie
if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$TALISMANEFichierSortie ]; then
	echo "\n${vert}--> Terminé.${reset}\n"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi





#SCRIPT PYTHON RECUPERATION CORPUS VECTORISE
#Entree : fichier de sortie de Talismane
#Sortie : fichier de sortie de Talismane pour lequel on n'a gardé que la deuxième colonne (les tokens)
echo "\n${bleu}##############################################################################"
echo "ETAPE 2 : RECUPERATION DES AVIS VECTORISES (SCRIPT RecupererAvisVectorises.py)"
echo "##############################################################################${reset}"
echo '\n--> Création du fichier '$corpus'_vect.txt\n'
PYTHONFichierVect=$corpus'_vect.txt'
cd ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/
python ./Codes/RecupererAvisVectorises.py $corpus
if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$PYTHONFichierVect ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi





#SEM 
#Entree : corpus vectorisé
#Sortie : corpus vectorisé avec POS et Chunk 
echo "\n${bleu}########################################################"
echo "ETAPE 3 : ANALYSES MORPHOSYNTAXIQUES, POS ET CHUNK (SEM)"
echo "########################################################${reset}"
echo '\n--> Création du fichier '$corpus'_sem.txt\n'
cd ~/../../Applications/SEM-master/
SEMFichierEntree=$corpus'_vect.txt'
./sem tagger ./resources/master/fr/np_chunking_ad.xml ./../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$SEMFichierEntree -o ./../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/
SEMFichierSortie=$corpus'_vect.export-1.conll'
SEMFichierSortieRenomme=$corpus'_sem.txt'
mv ./../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$SEMFichierSortie ./../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$SEMFichierSortieRenomme
if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$SEMFichierSortieRenomme ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi





#SCRIPT PYTHON UNIFORMISATION DES FICHIERS CoNLL
#Entree : 1) le corpus vectorisé selon la segmentation Talismane (sortie de l'étape 2) 2) la sortie de SEM (étape 3)
#Sortie : fichier_SEM uniformisé selon la segmentation Talismane
echo "\n${bleu}########################################################################################################"
echo "ETAPE 4 : UNIFORMISATION DES FICHIERS CoNLL SELON LA SEGMENTATION TALISMANE (Script UniformiserCoNLL.py)"
echo "########################################################################################################${reset}"
echo '\n--> Création du fichier aggregation_talismane_sem_'$corpus'_vect.txt\n'
cd ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/
python ./Codes/UniformiserCoNLL.py $PYTHONFichierVect $SEMFichierSortieRenomme $TALISMANEFichierSortie
FichierHarmonise='aggregation_talismane_sem_'$corpus'_vect.txt'
if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$FichierHarmonise ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi





#SCRIPTE PYTHON QUI REMPLACE LES INDICES ABSOLUS DES TETES SYNTAXIQUES PAR DES INDICES RELATIFS
#Entree : le fichier agregeant les informations de Talismane et de SEM
#Sortie : le même fichier mais avec des indices de dépendances syntaxiques relatifs et plus absulus
echo "\n${bleu}#########################################################################################"
echo "ETAPE 5 : TRANSFORMATION DES INDICES ABSOLUS DE DÉPENDANCE SYNTAXIQUE EN INDICES RELATIFS"
echo "#########################################################################################${reset}"
echo '\n--> Modification du fichier aggregation_talismane_sem_'$corpus'_vect.txt\n'
python ./Codes/DepSyntax_TransformationIndicesAbsolusENRelatifs.py $FichierHarmonise
DepRel_FichierHarmonise='depRel_'$FichierHarmonise
if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$DepRel_FichierHarmonise ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi





#SCRIPTE PYTHON QUI ATTRIBUT DES VALEURS BOOLEENNES SI LE TOKEN APPARTIENT A UN LEXIQUE
#Entree : le fichier le plus complet (etape 5)
#Sortie : le même fichier avec les valeurs booléennes
echo "\n${bleu}########################################################################"
echo "ETAPE 6 : INTÉGRATION DES INFORMATIONS LEXICALES ET INFO TETE SYNTAXIQUE"
echo "########################################################################${reset}"
echo '\n--> Création du fichier lex_aggregation_talismane_sem_'$corpus'_vect.txt\n'
python ./Codes/AppartenanceLexiques_InfoTeteSyntaxique.py $DepRel_FichierHarmonise
lex_fichier='lex_'$DepRel_FichierHarmonise
if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$lex_fichier ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi





#TRANSFORMATION DU DERNIER FICHIER EN CoNLL TEL QUE ACCEPTÉ PAR GATE
echo "\n${bleu}#########################################"
echo "ETAPE 7 : TRANSFORMATION EN FICHIER CoNLL"
echo "#########################################${reset}"
echo '\n--> Création du fichier '$corpus'.conll\n'

python ./Codes/TransformationCoNLL.py $lex_fichier

cp 'conll_'$lex_fichier $corpus'.conll'
rm 'conll_'$lex_fichier

if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$corpus'.conll' ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi




#AJOUT DES INDICES DE POSITION DE CHAQUE PHRASE DANS L'AVIS
echo "\n${bleu}####################################################################"
echo "ETAPE 8 : AJOUT DES INDICES DE POSITION DE CHAQUE PHRASE DANS L'AVIS"
echo "####################################################################${reset}"
echo '\n--> Modification du fichier '$corpus'.conll\n'

python ./Codes/Identifiant_IndicePositionPhraseDansAvis.py $corpus'.conll'

rm $corpus'.conll'
mv 'indicePos_'$corpus'.conll' $corpus'.conll'
python ./Codes/SupprimerDoubleRetourChariot.py $corpus'.conll'

if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$corpus'.conll' ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi




echo "\n${bleu}######################################################"
echo "ETAPE 9 : AJOUT DES POS TAG TREETAGGER (ECRIT ET ORAL)"
echo "######################################################${reset}"
echo '\n--> Modification du fichier '$corpus'.conll\n'

python ./Codes/VectoriserCorpusComplet_TreeTagger.py $corpus'.conll'
cd ~/../../Applications/TreeTagger/bin
./tree-tagger ./../lib/french.par ./../../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/'txt_treetagger_'$corpus'.conll' ./../../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/'treetagger_ecrit_'$corpus'.conll' -token
./tree-tagger ./../lib/spoken-french.par ./../../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/'txt_treetagger_'$corpus'.conll' ./../../../Users/JeanBaptiste_Tanguy/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/'treetagger_oral_'$corpus'.conll' -token
cd ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/
python ./Codes/ReunificationPOStag_TreeTagger.py $corpus'.conll' 'treetagger_ecrit_'$corpus'.conll' 'treetagger_oral_'$corpus'.conll' 'txt_treetagger_'$corpus'.conll'

if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$corpus'.conll' ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi






echo "\n${bleu}######################################################"
echo "ETAPE 10 : REORDONNANCEMENT DES ATTRIBUTS DU TABULAIRE"
echo "######################################################${reset}"
echo '\n--> Modification du fichier '$corpus'.conll : réordonnancement des attributs et verification des retours chariots\n'

python ./Codes/ReordonnancementTabulaire.py $corpus'.conll'

if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$corpus'.conll' ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi




#SUPPRESSION DES FICHIERS INTERMÉDIAIRES
echo "\n${bleu}###################################################################"
echo "ETAPE 11 : SUPPRESSION DES FICHIERS INTERMÉDIAIRES ET LIGNE UNIQUES"
echo "###################################################################${reset}"
echo '\n--> Suppression des fichiers :\n\t'$corpus'_talismane.txt\n\t'$corpus'_vect.txt\n\t'$corpus'_sem.txt\n\taggregation_talismane_sem_'$corpus'_vect.txt\n\tdepRel_aggregation_talismane_sem_'$corpus'_vect.txt\n\tlex_depRel_aggregation_talismane_sem_'$corpus'_vect.txt\n'


rm $corpus'_talismane.txt'
rm $corpus'_vect.txt'
rm $corpus'_sem.txt'
rm 'aggregation_talismane_sem_'$corpus'_vect.txt'
rm 'depRel_aggregation_talismane_sem_'$corpus'_vect.txt'
rm 'lex_depRel_aggregation_talismane_sem_'$corpus'_vect.txt'

if [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$corpus'_talismane.txt' ] || [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$corpus'_vect.txt' ] || [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/$corpus'_sem.txt' ] || [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/'aggregation_talismane_sem_'$corpus'_vect.txt' ] || [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/'depRel_aggregation_talismane_sem_'$corpus'_vect.txt' ] || [ -f ~/Documents/WORK/Stages/AdvancedDecision/ConstructionCorpusApprentissage/'lex_depRel_aggregation_talismane_sem_'$corpus'_vect.txt' ] ; then
	echo "\n${rouge}--> ERREUR.\n${reset}"
else	
	echo "\n${vert}--> Terminé.\n${reset}"
fi

python ./Codes/SupprimerLignesUniques.py $corpus'.conll'

echo '\n'
#EOF