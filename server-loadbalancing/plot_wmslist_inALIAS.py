#! /usr/bin/python
# Main program to call sensor functions
import os, commands, sys, fpformat
sys.path.append('/opt/WMSMonitor/collector/bin/')
import readconf_func
confvar=readconf_func.readconf()
import MySQLdb

def plot_wmslist_inALIAS():
        '''plot_wmslist_inALIAS() -> utility to plot on file the list 
           of wms in aliases defined for your site 
        '''

        fileout=open('/var/www/html/wmsmon/main/wmspoolinfo.txt','w')
        fileout.write('GENERAL INFO ABOUT CNAF WMS/LB INSTANCES POOL ON: ' + commands.getoutput('date'))

        print "Starting db connection"
        try:
            db = MySQLdb.connection(host=confvar.get('WMSMON_DB_HOST'),user=confvar.get('WMSMON_DB_USER'),passwd=confvar.get('WMSMON_DB_PWD'),db=confvar.get('WMSMON_DB_NAME'))

        except Exception,e:
            stri2= "ERROR CONNECTING TO WMSMonitor DB: " + str(e)
            print stri2 
            print "ERROR: Please check mysql daemon is running and connection parameters are correct!"
            sys.exit(1)

        #+++++++++++++++++++++++++++++
        try:
              querystr="select alias_name, numout, subtest_enable, idalias from admin_loadbalancing where enable_flag=1;"
              
              #INITIALIZATION
              aliases=[]
              numout=[]
              subtest_enable=[]
              idalias=[]
              
              db.query(querystr) 
              r = db.store_result()
              row = r.fetch_row(10000)
              host_vo_dict = {}
              if len(row) > 0:
                 for line in row:
                 #host_vo_dict[hostname]=[idhost,vo,service]
                    aliases.append(line[0])
                    numout.append(line[1])
                    subtest_enable.append(line[2])
                    idalias.append(line[3])          
        except Exception,e:
              str2= "ERROR READING ALIAS LIST FROM WMSMonitor DB: " + str(e)
              print str2
              sys.exit(1)
        
        try:
            querystr="select hostname,vo,service from admin_host_labels inner join hosts on hosts.idhost=admin_host_labels.idhost where admin_host_labels.active='1' and service='WMS';"
            db.query(querystr) 
            r = db.store_result()
            row = r.fetch_row(10000) 
            if len(row) > 0:
               for line in row:
                   print line
        except Exception,e:
              str2= "ERROR HOSTS LIST FROM WMSMonitor DB: " + str(e)
              sys.exit(1)
        
        for ik in range(len(aliases)):
           fileout.write('\n\nALIAS: ' + aliases[ik] + '\n')
           try: 
              wmslist=[]        
              querystr="select hostname from hosts join admin_wms_alias_list on hosts.idhost=admin_wms_alias_list.idwms where idalias=" + idalias[ik] +  " and spare_label='0';"
              db.query(querystr) 
              r = db.store_result()
              row = r.fetch_row(10000)
              if len(row) > 0:
                 for line in row:
                 #host_vo_dict[hostname]=[idhost,vo,service]
                    wmslist.append(line[0])

           except Exception,e:
              print "ERROR READING WMS LIST FROM WMSMonitor DB: " + str(e)
              print "ERROR: Please check query and DB status"
              sys.exit(1)      

           fileout.write('ASSOCIATED WMS LIST: ' + str(wmslist))
           fileout.write('\nWMS CURRENTLY IN THE ALIAS:\n')
           fileout.write(commands.getoutput("for a in `host " + aliases[ik] + ".grid.cnaf.infn.it |awk '{print $4}'` ; do host $a|awk '{print $5}'; done"))
           fileout.write('\n\n')
            
            
plot_wmslist_inALIAS()
