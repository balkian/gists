#!/bin/bash
tosend=""
for i in *.log; do
    dir=$(echo $i | awk '{split($1,a,"_"); print a[1]}');
    if [ ! -d $dir ]; then
        mkdir $dir;
    fi;
    mv $i $dir;
    tosend="$tosend\n$dir"
done
for i in $(echo -e $tosend | uniq);do
    echo Compressing $i
    tar -zcvf $i.tar.gz $i
    scp $i.tar.gz user@server
done