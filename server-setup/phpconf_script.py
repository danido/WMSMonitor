#!/usr/bin/python
import os, commands, sys, fpformat
sys.path.append('/opt/WMSMonitor/common/')
import logging
import readconf_func

print "Reading configuration from files"
#Reading configuration from files
try:
    confvar=readconf_func.readconf();
except:
    print "Error reading configuration file: /opt/WMSMonitor/common/wmsmon_site-info.def"
    sys.exit(1)

try:
	outfile=open('/var/www/html/' + confvar.get('WEBDIR') + '/common/config.php','w')
except: 
	   
	print "Error creating php conf file: /var/www/html/", confvar.get('WEBDIR') ,"/common/config.php\n"
	print "Please check httpd is installed and directory exists...\n"
	sys.exit(1)

print "Writing the PHP configuration file"

#Writing the PHP configuration file
outfile.write('<?php\n')
outfile.write('$config->dbHost="' + confvar.get('WMSMON_DB_HOST') + '";\n')
outfile.write('$config->dbUser="' + confvar.get('WMSMON_WEB_DB_USER') + '";\n')
outfile.write('$config->dbPass="' + confvar.get('WMSMON_WEB_DB_PWD') + '";\n')
outfile.write('$config->dbDatabase="' + confvar.get('WMSMON_DB_NAME') + '";\n')
outfile.write('\n')
outfile.write('$db=mysql_connect($config->dbHost,$config->dbUser,$config->dbPass) or die("Unable to connect db");\n')
outfile.write('mysql_select_db($config->dbDatabase) or die ("Unable to select db");\n')
outfile.write('\n')
outfile.write('$config->wmsmonWebDir="' + confvar.get('WEBDIR') + '/";\n')
outfile.write('\n')
outfile.write('$config->lemonLink=' + confvar.get('LEMONFLAG') + ';\n')
outfile.write('\n')
outfile.write('$config->lemonURL="' + confvar.get('LEMONURL') + '?entity=";\n')
outfile.write('\n')
outfile.write('$config->contactEmail="' + confvar.get('WMSMON_SEVER_CONTACT_EMAIL').split('@')[0] + ' AT ' + confvar.get('WMSMON_SEVER_CONTACT_EMAIL').split('@')[1] + '";\n')
outfile.write('\n')
outfile.write('$config->protectedPages=1;\n')
outfile.write('\n')
outfile.write('?>\n')

