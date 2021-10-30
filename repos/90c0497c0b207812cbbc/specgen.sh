#!/bin/bash
if [ $# -lt 1 ]
  then
    echo "Usage: $0 <ONTO> <FORMAT> <VERSION> <DIR> <NS>"
    echo "Example: $0 onto owl latest /tmp/Onto http://example.com/ontologies owl"
    exit
  else
    ONTO=$1
fi
if [ $# -lt 2 ]
  then
    FORMAT=owl
  else
    FORMAT=$2
fi
if [ $# -lt 3 ]
  then
    VERSION=latest
  else
    VERSION=$3
fi
if [ $# -lt 4 ]
  then
    DIR=~/Doctorado/Ontologies/$ONTO
  else
    DIR=$4
fi
if [ $# -lt 5 ]
  then
    NS=http://www.gsi.dit.upm.es/ontologies/$ONTO/ns#
  else
    NS=$5
fi

SPECPATH=~/Doctorado/tools/specgen6

echo "Generating docs for $ONTO from: $DIR"
echo "Namespace: $NS"

cp -r $DIR/spec $DIR/spec_backup
rm -rf $VERSION/
mkdir $DIR/spec/$VERSION
python2 $SPECPATH/specgen6.py --indir=$DIR --ns=$NS  --prefix=$ONTO --ontofile=$ONTO.$FORMAT --outdir=$DIR/spec/$VERSION --templatedir=$DIR --outfile=index.html
cd $DIR/spec
cp ../$ONTO.$FORMAT $VERSION/
ln -s $ONTO.$FORMAT $VERSION/ns
cp -R ../img $VERSION/
cp ../style.css $VERSION/
rm index.html img style.css ns $ONTO.$FORMAT
ln -s $VERSION/index.html .
ln -s $VERSION/$ONTO.$FORMAT $ONTO.$FORMAT
ln -s $VERSION/$ONTO.$FORMAT ns
ln -s $VERSION/img img
ln -s $VERSION/style.css style.css