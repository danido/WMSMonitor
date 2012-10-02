#!/usr/bin/python

import os, commands, sys, fpformat,datetime,time

crl_path = '/etc/grid-security/certificates/'
cmd = 'ls -1 ' + crl_path + '*.r0'

cmd_ssl = '/usr/bin/openssl crl -noout -nextupdate -issuer -in '
crl_stream = os.popen(cmd)
message = ''

crl_error_file = './error_tmp'
m_file = open(crl_error_file,'w')

crl_white_list = ['/etc/grid-security/certificates/2e5e0e92.r0','/etc/grid-security/certificates/7b4ac91c.r0','/etc/grid-security/certificates/cba8a8ae.r0'
                 ,'/etc/grid-security/certificates/d1dac263.r0']

HUSTON_WE_HAVE_A_PROBLEM = False
for crl in crl_stream:
   if crl_white_list.count(crl[ :len(crl) - 1 ]) == 0 :
      cmd = cmd_ssl + crl
      date_stream = os.popen(cmd)
      lines = date_stream.readlines()
      issuer = ''
      for line in lines:
         if line.find('issuer') != -1 :
            issuer =  line[ 7 : len(line) -1 ]
            #print issuer
      for line in lines:
         if line.find('nextUpdate') != -1 :
            next_update_str = line[ 11 : len(line) -1 ]
            #print next_update_str
            next_update_obj = time.strptime(next_update_str,"%b %d %H:%M:%S %Y %Z")
            #date_str = time.strftime("%Y-%m-%d %H:%M:%S",next_update_obj)
            gmt_obj = time.gmtime()
            if gmt_obj > next_update_obj:
               print 'ERROR: Expired crl. CRL is: ' + crl[ : len(crl) - 1 ]
               message = message + 'ERROR: Expired crl. CRL is: ' + crl[ : len(crl) - 1 ] + '\n'
               print 'Expired on : ' + next_update_str
               message = message + 'Expired on : ' + next_update_str + '\n'
               print 'Issued by : ' + issuer
               message = message + 'Issued by : ' + issuer + '\n\n'
               HUSTON_WE_HAVE_A_PROBLEM = True

if HUSTON_WE_HAVE_A_PROBLEM == True :
   m_file.writelines(message)
   m_file.close()

   mail_cmd = '''mail -s "WMS `/bin/hostname` crl problem" daniele.cesini@cnaf.infn.it,danilo.dongiovanni@cnaf.infn.it >/dev/null < ''' + crl_error_file

   os.system(mail_cmd)

   cmd = 'rm -f ' + crl_error_file
   os.system(cmd)
