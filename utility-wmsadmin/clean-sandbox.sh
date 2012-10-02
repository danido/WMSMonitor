#!/bin/bash
# BY alessandro.cavalli@cnaf.infn.it

# 2005-07-13  1st release, move only
# 2005-10-07  unattended remove (for crontab)


usage()
{
   cat <<EOF
Usage:
       clean-sandbox.sh <DATE> [DESTINATION DIR]
       or
       clean-sandbox.sh <DATE> --remove

       Where DATE is required and in format
       YYYYMMDD

       Job directories will be moved if older than DATE.
       They will be put in DESTINATION DIR if specified
       otherwise in /root/oldSandboxes

       With "--remove" they will be removed without
       asking any confirmation (for crontab).
EOF
}

if [ -z "$1" ] ; then
   usage
   exit
fi

LIMIT_DATE=$1


if [ "$2" != "--remove" ] ; then

   cat <<EOF

###########################
##                       ##
##    SANDBOX  CLEANUP   ##
##                       ##
###########################

BE CAREFUL!!!
JOB DIRECTORIES WILL BE MOVED
IF OLDER THAN
 $LIMIT_DATE
(YYYYMMDD)

ARE YOU SURE? [y/N]
EOF

   read ans1 <&0
   if [ "$ans1" != "y" ] ; then
      exit
   fi

   echo "ARE YOU *REALLY* SURE? [y/N]"
   read ans2 <&0
   if [ "$ans2" != "y" ] ; then
      exit
   fi

   if [ -z "$2" ] ; then
      DEST_ROOT=/root/oldSandboxes
      if [ ! -d /root/oldSandboxes ] ; then
         mkdir /root/oldSandboxes
      fi
   else
      DEST_ROOT=$2/`hostname`_oldSandboxes
      if [ ! -d $DEST_ROOT ] ; then
         mkdir $DEST_ROOT
      fi
   fi

   echo
   echo "Moving to $DEST_ROOT ..."
   echo

else
   STARTING_TIME=`date +%Y%m%d_%H%M%S`
   echo "##############################################"
   echo "Sandbox Cleanup starting time: $STARTING_TIME"
   echo "##############################################"
fi


for SANDBOX_DIR in `ls -1d /var/glite/SandboxDir/*`
do
   cd $SANDBOX_DIR

   if [ "$2" != "--remove" ] ; then

      SANDBOX_REL=`echo $SANDBOX_DIR|awk -F'/' '{print $5}'`
      DEST_DIR=$DEST_ROOT/$SANDBOX_REL
      if [ ! -d $DEST_DIR ] ; then
         mkdir $DEST_DIR
      fi

      ls -ltrd --time-style=+%Y%m%d * 2> /dev/null |awk '{print $6" "$7}'| \
       while read data nome ; do if [ $data -lt $LIMIT_DATE ]; then echo "moving job dir dated: $data  named: $nome"; mv -f $nome $DEST_DIR ; fi; done

   else

      REMOVE_TIME=`date +%Y%m%d_%H%M%S`

      ls -ltrd --time-style=+%Y%m%d * 2> /dev/null |awk '{print $6" "$7}'| \
       while read data nome ; do if [ $data -lt $LIMIT_DATE ]; then echo "$REMOVE_TIME - Removing job dir dated: $data  named: $nome"; rm -rf $nome; fi; done

   fi
done

if [ "$2" = "--remove" ] ; then
   ENDING_TIME=`date +%Y%m%d_%H%M%S`
   echo "##############################################"
   echo "Sandbox Cleanup ending time: $ENDING_TIME"
   echo "##############################################"
fi

