# INFO pour lancer le script
#1) Se placer dans le répertoire /ConstructionCorpusApprentissage/Codes/
#2) Lancer ce script
#3) donner les noms des corpus (et pas le chemin d'acces) sans extension [le corpus doit se trouver dans /ConstructionCorpusTabulaire


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
cd ./../../../../outils/talismane-distribution-3/
java -Xmx1G -jar -Dconfig.file=talismane-fr-3.0.0b.conf talismane-core-3.0.0b.jar encoding=UTF8 tokenFilters="./filters_token/identifiant.txt" inFile=./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/$corpus'.txt' outFile=./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/$corpus'_talismane.conll'
cd ./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/
if [ -f ./$corpus'_talismane.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi

# Le corpus contient :
# IdToken - Token - Lemme - POS-tag Talismane - IdAbsTeteSyntax - FctSyntax 


# ---> SEM
echo "\n${bleu}• SEM : analyses morphosyntaxiques, POS-tags, chunks, entités nommées... ${reset}"
# Recupération des avis vectorisés selon talismane -> ce qu'on donne à SEM
echo $corpus'_talismane.conll --> '$corpus'_vect.conll'
python ./Codes/RecupererAvisVectorises.py $corpus
if [ -f ./$corpus'_vect.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi
# Utilisation de SEM
# Chunk
echo $corpus'_vect.conll --> '$corpus'_sem_chunk.conll'
cd ./../../../../outils/SEM-master/
./sem tagger ./resources/master/fr/np_chunking_ad.xml ./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/$corpus'_vect.conll' -o ./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/
cd ./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/
# On renomme le fichier de sortie de SEM
mv ./$corpus'_vect.export-1.conll' ./$corpus'_sem_chunk.conll'
if [ -f ./$corpus'_sem_chunk.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi

# Entites nommées
echo $corpus'_vect.conll --> '$corpus'_sem_ne.conll'
cd ./../../../../outils/SEM-master/
./sem tagger ./resources/master/fr/NER.xml ./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/$corpus'_vect.conll' -o ./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/
cd ./../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/
# On renomme le fichier de sortie de SEM
mv ./$corpus'_vect.export-1.conll' ./$corpus'_sem_ne.conll'
if [ -f ./$corpus'_sem_ne.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi

# Fusionner les deux fichier SEM
echo $corpus'_sem_chunk.conll + '$corpus'_sem_ne.conll --> '$corpus'_sem.conll'
python ./Codes/FusionnerSEMChunkEN.py $corpus'_sem_chunk.conll' $corpus'_sem_ne.conll' $corpus'_sem.conll'
if [ -f ./$corpus'_sem.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi

# Comme SEM réalise une segmentation du texte différente de Talismane, il faut harmoniser la segmentation
echo $corpus'_talismane.conll + '$corpus'_vect.conll + '$corpus'_sem.conll --> aggregation_talismane_sem_'$corpus'_vect.conll'
python ./Codes/UniformiserCoNLL.py $corpus'_vect.conll' $corpus'_sem.conll' $corpus'_talismane.conll' 'aggregation_talismane_sem_'$corpus'_vect.conll'
if [ -f ./'aggregation_talismane_sem_'$corpus'_vect.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi
echo '\n--> Renoihage de aggregation_talismane_sem_'$corpus'_vect.conll en '$corpus'.conll'
mv ./'aggregation_talismane_sem_'$corpus'_vect.conll' ./$corpus'.conll'


# Le corpus contient :
# IdToken - Token - Lemme - POS-tag Talismane - IdAbsTeteSyntax - FctSyntax - POS SEM - Chunck SEM - Entités Nommées SEM




echo "\n\n\n${titre}######################################################################################################"
echo "                   SECTION 2 : AJOUT DE COLONNES AU TABULAIRE (PLUGINS)"
echo "######################################################################################################${reset}"


# --> AJOUT DES INDICES -RELATIFS- DES TÊTES SYNTAXIQUES
echo "\n${bleu}• Ajout des indices -relatifs- de dépendences syntaxiques (avec les têtes syntaxiques)... ${reset}"
echo $corpus'.conll --> depRel_'$corpus'.conll'
python ./Codes/DepSyntax_TransformationIndicesAbsolusENRelatifs.py $corpus'.conll'
if [ -f ./'depRel_'$corpus'.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi
# Le corpus contient :
# IdToken - Token - Lemme - POS-tag Talismane - IdAbsTeteSyntax - IdRelTeteSyntax - FctSyntax - POS SEM - Chunck SEM - Entités Nommées SEM



# --> AJOUT DES POS-TAGS TREETAGGER
echo "\n${bleu}• Ajout des POS-tags TreeTagger (écrit et oral)... ${reset}"
echo 'depRel_'$corpus'.conll --> pourTT_depRel_'$corpus'.conll'
python ./Codes/VectoriserCorpusComplet_TreeTagger.py 'depRel_'$corpus'.conll' 'pourTT_depRel_'$corpus'.conll'
if [ -f ./'pourTT_depRel_'$corpus'.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi

cd ./../../../../outils/TreeTagger/bin
./tree-tagger ./../lib/french.par ./../../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/'pourTT_depRel_'$corpus'.conll' ./../../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/'tte_depRel_'$corpus'.conll' -token
./tree-tagger ./../lib/spoken-french.par ./../../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/'pourTT_depRel_'$corpus'.conll' ./../../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/'tto_depRel_'$corpus'.conll' -token
cd ./../../../iha/V2/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/

echo 'depRel_'$corpus'.conll, tte_depRel_'$corpus'.conll, tto_depRel_'$corpus'.conll, pourTT_depRel_'$corpus'.conll'
python ./Codes/ReunificationPOStag_TreeTagger_modif.py 'depRel_'$corpus'.conll' 'tte_depRel_'$corpus'.conll' 'tto_depRel_'$corpus'.conll' 
#python ./Codes/ReunificationPOStag_TreeTagger_modif.py 'depRel_'$corpus'.conll' 'tte_depRel_'$corpus'.conll' 'tto_depRel_'$corpus'.conll' 'pourTT_depRel_'$corpus'.conll'
# suppression des fichiers intermédiaires
#rm 'tte_depRel_'$corpus'.conll'
#rm 'tto_depRel_'$corpus'.conll'
#rm 'pourTT_depRel_'$corpus'.conll'
if [ -f ./'lex_tt_depRel_'$corpus'.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi
# Le corpus contient :
# IdToken - Token - Lemme - POS-tag Talismane - IdAbsTeteSyntax - IdRelTeteSyntax - FctSyntax - POS SEM - Chunck SEM - Entités Nommées SEM
# POS-tag TreeTagger Ecrit - POS-tag TreeTagger Oral



# --> AJOUT DES INFORMATIONS LEXICALES
echo "\n${bleu}• Ajout des informations lexicales... ${reset}"
echo 'tt_depRel_'$corpus'.conll --> lex_tt_depRel_'$corpus'.conll'
python ./Codes/AppartenanceLexique.py 'tt_depRel_'$corpus'.conll'
if [ -f ./'lex_tt_depRel_'$corpus'.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi
# Le corpus contient :
# IdToken - Token - Lemme - POS-tag Talismane - IdAbsTeteSyntax - IdRelTeteSyntax - FctSyntax - POS SEM - Chunck SEM - Entités Nommées SEM
# POS-tag TreeTagger Ecrit - POS-tag TreeTagger Oral - Lexique (x12)



# --> AJOUT DES INFORMATIONS TÊTE SYNTAXIQUE
echo "\n${bleu}• Ajout des informations sur les têtes syntaxiques... ${reset}"
echo 'lex_tt_depRel_'$corpus'.conll --> head_lex_tt_depRel_'$corpus'.conll'
python ./Codes/InfoTeteSyntaxique_modif.py 'lex_tt_depRel_'$corpus'.conll'
if [ -f ./'head_lex_tt_depRel_'$corpus'.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi
# Le corpus contient :
# IdToken - Token - Lemme - POS-tag Talismane - IdAbsTeteSyntax - IdRelTeteSyntax - FctSyntax - POS SEM - Chunck SEM - Entités Nommées SEM
# POS-tag TreeTagger Ecrit - POS-tag TreeTagger Oral - Lexique (x10) - Head lemme - Head POS Talismane - Head Fct Syntax
# Head POS SEM - Head Chunk SEM - Head entité nommée - Head POS TreeTagger Ecrit - Head POS TreeTagger Oral - Head Lexique



# --> IDENTIFIANT ET POSITION DES PHRASES DANS L'AVIS
echo "\n${bleu}• Ajout de l'identifiant de l'avis et de la position de la phrase dans l'avis... ${reset}"
echo 'head_lex_tt_depRel_'$corpus'.conll --> id_pos_head_lex_tt_depRel_'$corpus'.conll'
python ./Codes/Identifiant_PositionDansAvis.py 'head_lex_tt_depRel_'$corpus'.conll'
if [ -f ./'id_pos_head_lex_tt_depRel_'$corpus'.conll' ]; then
	echo "${vert}--> Terminé.${reset}"
else
	echo "${rouge}--> ERREUR.${reset}"
fi
# Le corpus contient :
# IdToken - Token - Lemme - POS-tag Talismane - IdAbsTeteSyntax - IdRelTeteSyntax - FctSyntax - POS SEM - Chunck SEM - Entités Nommées SEM
# POS-tag TreeTagger Ecrit - POS-tag TreeTagger Oral - Lexique (x10) - Head lemme - Head POS Talismane - Head Fct Syntax
# Head POS SEM - Head Chunk SEM - Head entité nommée - Head POS TreeTagger Ecrit - Head POS TreeTagger Oral - Head Lexique
# Identifiant avis - Indice position phrase dans avis


echo '\n--> Renoihage de en_id_pos_head_lex_tt_depRel_'$corpus'.conll en '$corpus'.conll'
mv ./'id_pos_head_lex_tt_depRel_'$corpus'.conll' ./'att_'$corpus'.conll'






echo "\n\n\n${titre}######################################################################################################"
echo "                      SECTION 3 : NETTOYAGE ET REORDONNANCEMENT DU FICHIER CONLL"
echo "######################################################################################################${reset}"

# --> SUPPRESSION DE LA PREMIÈRE COLONNE
echo "\n${bleu}• Transformation en CoNLL correct : suppression des espaces et suppression colonne 1 (indice tokens)... ${reset}"
echo 'att_'$corpus'.conll --> conllOK_att_'$corpus'.conll'
python ./Codes/TransformationCoNLL.py 'att_'$corpus'.conll'
if [ -f ./'conllOK_att_'$corpus'.conll' ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi



# Le corpus contient :
# Token - Lemme - POS-tag Talismane - IdAbsTeteSyntax - IdRelTeteSyntax - FctSyntax - POS SEM - Chunck SEM - Entités Nommées SEM
# POS-tag TreeTagger Ecrit - POS-tag TreeTagger Oral - Lexique (x10) - Head lemme - Head POS Talismane - Head Fct Syntax
# Head POS SEM - Head Chunk SEM - Head entité nommée - Head POS TreeTagger Ecrit - Head POS TreeTagger Oral - Head Lexique
# Identifiant avis - Indice position phrase dans avis



# --> SUPPRESSION DES LIGNES UNIQUES ET DES LIGNES VIDES
echo "\n${bleu}• Suppression des lignes uniques et des lignes vides... ${reset}"
echo 'conllOK_att_'$corpus'.conll --> ligneUniqOK_conllOK_att_'$corpus'.conll'
python ./Codes/SupprimerLignesUniques.py 'conllOK_att_'$corpus'.conll'
python ./Codes/SupprimerDoubleRetourChariot.py 'ligneUniqOK_conllOK_att_'$corpus'.conll'
if [ -f ./'ligneUniqOK_conllOK_att_'$corpus'.conll' ]; then
	echo "\n${vert}--> Terminé.\n${reset}"
else
	echo "\n${rouge}--> ERREUR.\n${reset}"
fi



# --> RÉORDONNANCEMENT DES ATTRIBUTS
#echo "\n${bleu}• Réordonnancement des attributs... ${reset}"
#echo 'ligneUniqOK_conllOK_att_'$corpus'.conll --> ordreAttOK_ligneUniqOK_conllOK_att_'$corpus'.conll'
#python ./Codes/ReordonnancementTabulaire.py 'ligneUniqOK_conllOK_att_'$corpus'.conll'
#if [ -f ~/Documents/WORK/Stages/AdvancedDecision/Segmentation_thematique_CRF/ConstructionCorpusTabulaire/'ordreAttOK_ligneUniqOK_conllOK_att_'$corpus'.conll' ]; then
#	echo "\n${vert}--> Terminé.\n${reset}"
#else
#	echo "\n${rouge}--> ERREUR.\n${reset}"
#fi


# --> RENOihaNGE DE LA SORTIE DU PROGRAMME
echo "\n${bleu}• Renoihange du fichier de sortie en "$corpus".conll... ${reset}"
mv ./'ligneUniqOK_conllOK_att_'$corpus'.conll' ./$corpus'.conll'


# --> SUPPRESSION DES FICHIERS INTERMÉDIAIRES
echo "\n${bleu}• Suppression des fichiers intermédiaires... ${reset}"
#rm 'att_'$corpus'.conll'
#rm 'conllOK_att_'$corpus'.conll'
#rm 'depRel_'$corpus'.conll'
#rm 'head_lex_tt_depRel_'$corpus'.conll'
#rm 'lex_tt_depRel_'$corpus'.conll'
#rm $corpus'_sem_chunk.conll'
#rm $corpus'_talismane.conll'
#rm $corpus'_vect.conll'
#rm 'tt_depRel_'$corpus'.conll'
#rm$mcorpus'_sem_ne.conll'
#rm $corpus'_sem.conll'