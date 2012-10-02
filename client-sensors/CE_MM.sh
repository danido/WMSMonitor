#!/bin/bash

# USAGE: ./CE_MM.sh <workload_manager_events.log file> <output_file>

hour=`date "+%H %M" | awk '{print $1}'`
if [ $hour == "00" ]; then
DATE=`date --date="1 day ago" "+%d %b"`
DATE2=`date --date="1 day ago" "+%Y-%m-%d"`
else
DATE=`date "+%d %b"`
DATE2=`date "+%Y-%m-%d"`
fi
#echo $DATE

FILEDATE=`date "+%d%b%Y"`
#FILENAME=/opt/WMSMonitor/sensors/tmp/CE_MM.txt
FILENAME=$2
echo "START OF FILE" > $FILENAME
echo "DATE = "$DATE2 >> $FILENAME

# this is the new command to fix pending jobs bug
#/var/log/wms/workload_manager_events.log
#grep 'MM for job' /var/log/wms/workload_manager_events.log* |grep "$DATE" |awk '{print $10 " " $11}' | uniq | awk '{print $2}' | sed 's/(/ /'| sed 's/\// /'|awk '{print $1}' |sort -g|uniq -c  >> $FILENAME

grep 'MM for job' $1* |grep "$DATE" |awk '{print $10 " " $11}' | uniq | awk '{print $2}' | sed 's/(/ /'| sed 's/\// /'|awk '{print $1}' |sort -g|uniq -c  >> $FILENAME

echo "END OF FILE" >> $FILENAME

#echo "FILE CREATED = "$FILENAME
