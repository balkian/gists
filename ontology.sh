
if [ $# -lt 3 ]
  then
    REMOTE=gsi-web@web-home.dit.upm.es:lib/www/gsi/ontologies/
  else
    REMOTE=$3
fi

if [ $# -lt 2 ]
  then
    DIR=~/Doctorado/Ontologies/Onyx
  else
    DIR=$2
fi

if [ $# -lt 1 ]
  then
    ONTO=onyx
  else
    ONTO=$1
fi

echo "Generating docs for $ONTO from: $DIR"

python specgen6.py --indir=$DIR --ns='http://www.gsi.dit.upm.es/ontologies/$ONTO/ns#'  --prefix=$ONTO --ontofile=$ONTO.owl --outdir=$DIR/spec/latest --templatedir= --outfile=index.html
echo "Uploading to $REMOTE"
rsync -r --links --copy-unsafe-links $DIR/spec/ $REMOTE