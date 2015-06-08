#!/bin/bash
if [ $# -lt 1 ]
  then
    ONTO=onyx
  else
    ONTO=$1
fi
if [ $# -lt 2 ]
  then
    VERSION=latest
  else
    VERSION=$2
fi
if [ $# -lt 3 ]
  then
    DIR=~/Doctorado/Ontologies/Onyx
  else
    DIR=$3
fi
if [ $# -lt 4 ]
  then
    NS=http://www.gsi.dit.upm.es/ontologies/$ONTO/ns#
  else
    NS=$4
fi

SPECPATH=~/Doctorado/tools/specgen6

echo "Generating docs for $ONTO from: $DIR"
echo "Namespace: $NS"

cp -r $DIR/spec $DIR/spec_backup
rm -rf $VERSION/
mkdir $DIR/spec/$VERSION
python $SPECPATH/specgen6.py --indir=$DIR --ns=$NS  --prefix=$ONTO --ontofile=$ONTO.owl --outdir=$DIR/spec/$VERSION --templatedir=$DIR --outfile=index.html
cd $DIR/spec
rm index.html ns $ONTO.owl
ln -s $VERSION/index.html .
ln -s $VERSION/$ONTO.owl $ONTO.owl
ln -s $VERSION/$ONTO.owl ns
ln -s ../img $VERSION/img
ln -s ../style.css $VERSION/style.css