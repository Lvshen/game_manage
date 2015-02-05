#!/bin/bash
dir=`dirname $0`
cd $dir
url=`pwd`
cd $url
DIR=/tmp/protocol
DATE=`date +%F_%T`
FILE='*.py*'
DIR1="${DIR}/${DATE}"
mkdir -pv $DIR1 > /dev/null 2>&1
mv $FILE $DIR1 && rm -rf $DIR1
