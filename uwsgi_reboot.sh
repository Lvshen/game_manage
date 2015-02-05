#!/bin/sh

MY_PATH=$(cd `dirname $0`; pwd)
cd $MY_PATH

DATE=`date +%F_%T`
PORT=$(sed -n '2p' uwsgi.xml | awk -F'[:|<]' '{print $3}')
PID=(`lsof -i:$PORT | awk '/[0-9]/{print $2}'`)
if [ -n "$PID" ];then
for P in ${PID[@]};do
kill -9 $P
done
sleep 1s
if [ -e django.log ];then
cp django.log django.log.$DATE
rm -f django.log
fi
uwsgi -x uwsgi.xml
else
uwsgi -x uwsgi.xml
fi
