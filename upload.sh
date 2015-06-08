#!/bin/bash
if [ $# -lt 1 ]
  then
    echo "Please, specify an ontology"
    return
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
    REMOTE=gsi-web@web-home.dit.upm.es:lib/www/gsi/ontologies/$ONTO/
  else
    REMOTE=$3
fi

echo "Uploading to $REMOTE"
rsync -r --links --copy-unsafe-links $DIR $REMOTE