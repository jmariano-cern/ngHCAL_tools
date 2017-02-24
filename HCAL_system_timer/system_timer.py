#!/usr/bin/python

from os import system as call
from sys import argv

BE_crate = argv[1]
uHTR_slot = argv[2]
adc_cut = 15

templatefile_name = './template'
scriptfile_name = './script'
logfile_name = './log'

templatefile = open(templatefile_name,'r')
lines_in = templatefile.readlines()
templatefile.close()

call('rm ' + logfile_name)
call('touch ' + logfile_name)

print 'Getting data from crate ' + str(BE_crate) + ' , uHTR ' + str(uHTR_slot) + ' at:'

for i in range (25):
    call('rm ' + scriptfile_name)
    call('touch ' + scriptfile_name)

    scriptfile = open(scriptfile_name,'w')
    for line_in in lines_in:
        if line_in.find('$PIPELINE') != -1:
            scriptfile.write(line_in.strip().replace('$PIPELINE',str(i*10)) + '\n')
        else:
            scriptfile.write(line_in.strip() + '\n')
    scriptfile.close()

    print "Pipeline: " + str(i*10)
    call('uHTRtool.exe -c ' + str(BE_crate) + ':' + str(uHTR_slot) + ' -s ' + scriptfile_name + ' > /dev/null')
    call('echo PIPELINE ' + str(i*10) + ' >> ' + logfile_name)
    call('uHTRtool.exe -c ' + str(BE_crate) + ':' + str(uHTR_slot) + ' -s spy > /dev/null')
    call('uHTRtool.exe -c ' + str(BE_crate) + ':' + str(uHTR_slot) + ' -s spy >> ' + logfile_name)

searchfile = open(logfile_name,'r')
searchlines = searchfile.readlines()

print 'Data acquired.'
print 'Searching for TSs with ADC > ' + str(adc_cut) + '...'
line_num = 0
for searchline in searchlines:
    line_num = line_num + 1
    if searchline.find('ADC') != -1:
#        print searchline.split('ADC')[1].split()[0]
        if (int(searchline.split('ADC')[1].split()[0]) > adc_cut) and (int(searchline.split('ADC')[1].split()[0]) != 128) and (int(searchline.split('ADC')[1].split()[0]) != 129):# and int(searchline.split('ADC')[1].split()[0]) < 150:
            print str(line_num) + ': ' + searchline.strip() 
    if searchline.find('PIPELINE') != -1:
        print searchline.strip() + ':'
