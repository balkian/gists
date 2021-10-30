#!/bin/bash
if [ $# -lt 1 ]
  then
    echo "Please, specify an ontology"
    exit 0
  else
    ONTO=$1
fi
if [ $# -lt 2 ]
  then
    DIR=~/Doctorado/Ontologies/$ONTO/spec/
  else
    DIR=$2
fi

if [ $# -lt 3 ]
  then
    REMOTE=ontologies@gsi.dit.upm.es:$ONTO/
  else
    REMOTE=$3
fi

echo "Uploading to $REMOTE"
#scp -r $DIR $REMOTE
sftp $REMOTE -b <<EOF
mput -r $DIR
EOF