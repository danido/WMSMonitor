cd /root/Sandbox
export diskusage=`df -h |grep /dev/sda3 |awk '{ print $5 }'| sed -e 's/%//'`;
export CLEANDATE=`date +%Y%m%d_%H%M_`
echo "Date $CLEANDATE - Percentage of Disk Used: $diskusage"
if [ $diskusage -gt 80 ]; then 
	cat /var/log/globus-gridftp.log \
	| grep " TYPE=STOR " \
	| sed -e 's/ NBYTES=/ /' -e 's/ FILE=/ /' \
	| awk '{if ($10 > 30000000) print $7}' \
	| while read file
	do
	 if [ -f "$file" ]; then
	   ls -lh $file >> ${CLEANDATE}Removed_Files.log
	   sizetmp=`ls -l $file  |awk '{print $5}'`
	   if [ $sizetmp -gt 100000000 ]; then
		 echo "removing file of size: " $sizetmp
                 echo ${CLEANDATE}Removed_Files.txt
	         echo "rm -f $file" >>  ${CLEANDATE}Removed_Files.txt
           fi
         fi
	 done
	if [ -f "${CLEANDATE}Removed_Files.txt" ]; then
 		chmod +x ${CLEANDATE}Removed_Files.txt
		echo "removing files"
	        ./${CLEANDATE}Removed_Files.txt
  	fi
fi

