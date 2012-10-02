#! /usr/bin/python
import time

bin = [0 for i in range(1000)]
bin_step = 50
found_start = False
found_autup = False

for i in range(4,-1,-1):
   if i == 0 :
      file_to_parse = '/var/log/WMSMONITOR.log'
   else:
      file_to_parse = '/var/log/WMSMONITOR.log' + '.' + str(i)

   f = open(file_to_parse)

   line = True
   while line:
      line = f.readline()
      if line.find("This is the WMSM") != -1:
         linesp = line.split()
         t1 = linesp[0] + ' ' + linesp[1]
         #print 't1=',t1
         found_start = True
      if found_start and (line.find("STARTING AUTOUPDATE") != -1):
         linesp = line.split()
         t2 = linesp[0] + ' ' +linesp[1]
         found_autup = True
         #print 't2 =', t2
      if line.find("Whole data_") != -1:
         linesp = line.split()
         data = linesp[0] + ' ' +linesp[1]
         seconds = linesp[9]
         fsec = float(seconds)
         nbin = int(fsec / bin_step)
         bin[nbin] = bin[nbin] + 1
         if found_start and found_autup:
            other = ' | ' + t1 + ' | ' + t2
         else:
            other = ''
         print data + ' |  ' + seconds + other
         found_start = False
         found_autup = False
   f.close()

for i in range(30):
   print str(i*50) + '-' + str((i+1) * 50) + ' : ' + str(bin[i])
