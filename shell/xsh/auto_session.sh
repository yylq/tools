#!/bin/bash
hostfile =$1
myPath="./session/"
tabfile="./back.xsh"
if [ ! -d "$myPath" ]; then 
    echo $myPath
    mkdir "$myPath" 
fi 
cd $myPath && rm -rf * && cd ..
hosts=`cat $hostfile`

for one in $hosts ; do
    new=$myPath$one".xsh"
    echo $new
    parten="s/\(Host=\).*/\1$one/"
    #echo $parten
    if [ ! -f "$new" ]; then
        rm -rf $new && cp $ $new 
        #echo "sed -i '$parten' $new"
        sed -i $parten $new
    fi 
    
done 
