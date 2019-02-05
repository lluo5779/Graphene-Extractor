#!/bin/bash
./spaceMaker.sh
pushd ../../Graphene-3.0.0/graphene-cli

FORMAT="SERIALIZED"
OPERATION="RE"

for inFilePath in ../inputs/files_to_run/*
	do 
		echo "$inFilePath"
		inFile=$(basename $inFilePath)
		inFile="${inFile%.*}"
		echo "'$inFile'"
		
		mvn exec:java -Dexec.args="--operation ${OPERATION} --output FILE '${inFile}-${OPERATION}-${FORMAT}.txt' --simformat ${FORMAT} --reformat ${FORMAT} --doCoreference false --isolateSentences true --input FILE $inFilePath" -Dconfig.file="../conf/graphene.conf"
		# mvn exec:java -Dexec.args="--operation RE --output FILE '../outputs/${inFile}-RE.txt' --reformat DEFAULT --doCoreference true --input FILE $inFilePath" -Dconfig.file="../conf/graphene.conf"
		break
	done


