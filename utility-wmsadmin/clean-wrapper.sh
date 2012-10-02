#!/bin/bash
# BY alessandro.cavalli@cnaf.infn.it

# 2005-10-07


usage()
{
   cat <<EOF
Usage:
       clean-wrapper.sh [--go]

       is a wrapper to put clean-sandbox.sh
       into the crontab.
       Only if you launch it with "--go" option
       it will start to delete Sandbox dirs
       older than one month.
       Logs in /var/log/clean-sandbox.log

EOF
}

if [ "$1" != "--go" ] ; then
   usage
   exit
fi


#CLEAN_DATE=`date --date='1 week ago' +%Y%m%d`
CLEAN_DATE=`date --date='1 week ago' +%Y%m%d`
/root/bin/clean-sandbox.sh $CLEAN_DATE --remove >> /var/log/clean-sandbox.log 2>&1
