
alias python='python3'

# Récupération du nom du corpus
corpus=$1
# Récupération du nombre de partitions déjà créées par l'utilisateur 
nombrePartitions=$2
# Récupération du nom de la série de modèle à créer
serieModels=$3

# Création des partitions
cd ./../CORPUS/
corpus1=${corpus%.txt}'_polaLarge.txt'
corpus2=${corpus%.txt}'_intense.txt'
cp $corpus $corpus1 # On duplique le copus d'origine car on change les étiquettes pour Polarité large
python ./Codes/TransformationEtiquette.py $corpus1 'TresNegatif' 'Negatif' # Transformation d'étiquette
python ./Codes/TransformationEtiquette.py $corpus1 'TresPositif' 'Positif' # Transformation d'étiquette
cp $corpus $corpus2 # On duplique le corpus d'origine car on change les étiquettes pour Intensité
python ./Codes/TransformationEtiquette.py $corpus2 'TresNegatif' 'Intense' # Transformation d'étiquette
python ./Codes/TransformationEtiquette.py $corpus2 'TresPositif' 'Intense' # Transformation d'étiquette
python ./Codes/TransformationEtiquette.py $corpus2 'Negatif' 'Faible' # Transformation d'étiquette
python ./Codes/TransformationEtiquette.py $corpus2 'Positif' 'Faible' # Transformation d'étiquette
cd ./../Codes


echo '--------------------------------------------'
echo 'RÉSULTATS DES APPRENTISSAGES POUR LA SÉRIE '$serieModels
echo '--------------------------------------------\n'

for i in `seq 1 $nombrePartitions`;
	do
		echo '--> PARTITION '$i

		# PARTIE POLARITÉ LARGE
		# Partitions
		cd ./../CORPUS/
		python ./Codes/CrossValidation_CreationPartition.py $corpus1 $nombrePartitions
		cd ./../Codes

		# Récupération des noms des corpus d'entrainement et de test
		corpus_train='./../CORPUS/TRAIN/'$i'_train.txt'
		corpus_test='./../CORPUS/TEST/'$i'_test.txt'

		# Vectorisation des corpus
		python VectorisationSegments.py $corpus_train ./../Lexiques/Positif.txt ./../Lexiques/Negatif.txt ./../Lexiques/Opinion.txt ./../Lexiques/MotsVides.txt ./../Lexiques/LabelTreeTagger.txt ./../Lexiques/LabelFctSyntaxTalismane.txt ./../Lexiques/LabelChuncksSEM.txt ./../Lexiques/LabelENSEM.txt
		python VectorisationSegments.py $corpus_test ./../Lexiques/Positif.txt ./../Lexiques/Negatif.txt ./../Lexiques/Opinion.txt ./../Lexiques/MotsVides.txt ./../Lexiques/LabelTreeTagger.txt ./../Lexiques/LabelFctSyntaxTalismane.txt ./../Lexiques/LabelChuncksSEM.txt ./../Lexiques/LabelENSEM.txt

		# Récupération des noms de fichiers vectorisés
		corpus_train_vect='./../CORPUS/TRAIN/'$i'_train_vect.txt'
		corpus_test_vect='./../CORPUS/TEST/'$i'_test_vect.txt'

		# Apprentissage du SVM avec le corpus d'entrainement
		python ApprentissageSVMs_hybride.py $corpus_train_vect './../MODELS/'$i'_model_polaLarge_'$serieModels'.pkl' 'linear'

		# Test du modèle appris sur les données tests
		python TestSVMs_hybride.py $corpus_test_vect './../MODELS/'$i'_model_polaLarge_'$serieModels'.pkl' './../CORPUS/TEST/RES_MODELS/'$i'_res_model_polaLarge'$serieModels'.txt'

		# PARTIE INTENSITE
		# Partitions
		cd ./../CORPUS/
		python ./Codes/CrossValidation_CreationPartition.py $corpus2 $nombrePartitions
		cd ./../Codes

		# Récupération des noms des corpus d'entrainement et de test
		corpus_train='./../CORPUS/TRAIN/'$i'_train.txt'
		corpus_test='./../CORPUS/TEST/'$i'_test.txt'

		# Vectorisation des corpus
		python VectorisationSegments.py $corpus_train ./../Lexiques/Positif.txt ./../Lexiques/Negatif.txt ./../Lexiques/Opinion.txt ./../Lexiques/MotsVides.txt ./../Lexiques/LabelTreeTagger.txt ./../Lexiques/LabelFctSyntaxTalismane.txt ./../Lexiques/LabelChuncksSEM.txt ./../Lexiques/LabelENSEM.txt
		python VectorisationSegments.py $corpus_test ./../Lexiques/Positif.txt ./../Lexiques/Negatif.txt ./../Lexiques/Opinion.txt ./../Lexiques/MotsVides.txt ./../Lexiques/LabelTreeTagger.txt ./../Lexiques/LabelFctSyntaxTalismane.txt ./../Lexiques/LabelChuncksSEM.txt ./../Lexiques/LabelENSEM.txt

		# Récupération des noms de fichiers vectorisés
		corpus_train_vect='./../CORPUS/TRAIN/'$i'_train_vect.txt'
		corpus_test_vect='./../CORPUS/TEST/'$i'_test_vect.txt'

		# Apprentissage du SVM avec le corpus d'entrainement
		python ApprentissageSVMs_hybride.py $corpus_train_vect './../MODELS/'$i'_model_intense_'$serieModels'.pkl' 'rbf'

		# Test du modèle appris sur les données tests
		python TestSVMs_hybride.py $corpus_test_vect './../MODELS/'$i'_model_intense_'$serieModels'.pkl' './../CORPUS/TEST/RES_MODELS/'$i'_res_model_intense'$serieModels'.txt'

		# PARTIE AGREGATION DES RESULTATS
		python JoindreResultatsDeuxPhases_hybride.py './../CORPUS/TEST/RES_MODELS/'$i'_res_model_polaLarge'$serieModels'.txt' './../CORPUS/TEST/RES_MODELS/'$i'_res_model_intense'$serieModels'.txt' './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt'

		# Appel de CROTAL pour visualiser les résultats
		# Suppression du fichier s'il existe déjà
		if [ -f './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal' ]; then
			rm './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal'
		fi
		~/../../Applications/CROTAL/crotal eval './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt' >> './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal'
		python AffichageResCrotal.py './../CORPUS/TEST/RES_MODELS/Sorties_Crotal/'$i'_res_model_'$serieModels'.crotal'
		python AffichageMicroMoyenneParEtiquettes.py './../CORPUS/TEST/RES_MODELS/'$i'_res_model_'$serieModels'.txt'
		echo '\n'
	done;
