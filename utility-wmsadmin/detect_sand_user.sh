cd /root/Sandbox
export diskusage=`df -h |grep /dev/sdb3 |awk '{ print $5 }'| sed -e 's/%//'`;
export CLEANDATE=`date +%Y%m%d_%H%M_`
echo "Date $CLEANDATE - Percentage of Disk Used: $diskusage"
if [ $diskusage -gt 80 ]; then
        echo "detecting big files" 
	cat /var/log/globus-gridftp.log \
	| grep " TYPE=STOR " \
	| sed -e 's/ NBYTES=/ /' -e 's/ FILE=/ /' \
	| awk '{if ($10 > 100000000) print $7}' \
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
        if [ -f "${CLEANDATE}Removed_Files.log" ]; then

           cat ${CLEANDATE}Removed_Files.log \
           |awk '{print $3 " " $5 " " $9}' \
           |sed 's/\/var\/glite\/SandboxDir\// /' \
           |sed 's/\// /'|sed 's/\// /' \
           |awk '{print $1 " " $2 " " $4}' \
           |sed 's/https_3a_2f_2f/ https\:\/\//' \
           |sed 's/_3a9000_2f/\:9000\//' \
           |sed 's/_5f/_/' \
           |while read map1 sizefile jobid
           do
             /opt/glite/examples/glite-lb-job_status $jobid \
             | grep  "+UserSubjectName" \
             | while read user
             do 
               echo "$map1 $sizefile $jobid  $user" >> ${CLEANDATE}Removed_Files_USERMAPPING.log
             done
           done
        fi
      
fi

