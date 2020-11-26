#!/usr/bin/python
# Script for checking global hardware health of host running VMware ESX/ESXi
#
# Licence : GNU General Public Licence (GPL) http://www.gnu.org/
# Pre-req : pywbem
# Based on the Nagios-Check 
# http://www.claudiokuenzler.com/ithowtos/nagios_check_esxi_wbem.php
# On Ubuntu and Debian Squezee use 'aptitude install python-pywbem'
# On other systems download it from http://sourceforge.net/projects/pywbem/ 
# unpack and then try 'python setup.py build' and 'python setup.py install'

import argparse
import sys
import pywbem
import re

parser = argparse.ArgumentParser(description='Retrieve hardware health state from VMWare ESX(i) server')
parser.add_argument('-u','--user',
                    help='Username for the connection to ESX(i) Server. If not given, "root" is used.',
                    required=False, default='root')
parser.add_argument('-p','--password',
                    help='Password for the connection to ESX(i) Server.',
                    required=True)
parser.add_argument('-i','--host',
                    help='IP or Hostname of ESX(i) Server',
                    required=True)
parser.add_argument('-v','--verbose',
                    help='Be more verbose.',
                    required=False, action='store_true' )
parser.add_argument('-s','--show-inventory',
                    help='Show the discovered items with formated output.',
                    required=False, action='store_true' )
parser.add_argument('-x','--zabbix-out',
                    help='Print output formated for piping to zabbix_sender',
                    required=False, action='store_true' )
parser.add_argument('-d','--item-discovery',
                    help='Print json list for Zabbix low level item discovery',
                    required=False, action='store_true' )
parser.add_argument('-z','--zabbix-hostname',
                    help='Name of host in Zabbix. If not given, host (-h/--host) will be used',
                    required=False)
parser.add_argument('-n','--item-name',
                    help='Name of Item as configured in Zabbix Server. If not given, "vmware.hardwarehealthstate" is used.',
                    default='vmware.hardwarehealthstate', required=False)
parser.add_argument('-k','--discovery-item-name',
                    help='Name of Item for discovery as configured in Zabbix Server. If not given, "vmware.hardwareitems" is used.',
                    required=False, default='vmware.hardwareitems')
                    
args = vars(parser.parse_args())
if args['zabbix_hostname']:
    zabbix_hostname = args['zabbix_hostname']
else:
    zabbix_hostname = args['host']
    

# define classes to check 'OperationStatus' instance
ClassesToCheck = [
	'OMC_SMASHFirmwareIdentity',
	'CIM_Chassis',
	'CIM_Card',
	'CIM_ComputerSystem',
	'CIM_NumericSensor',
	'CIM_Memory',
	'CIM_Processor', 
	'CIM_RecordLog',
	'OMC_DiscreteSensor',
	'OMC_Fan',
	'OMC_PowerSupply',
	'VMware_StorageExtent',
	'VMware_Controller',
	'VMware_StorageVolume',
	'VMware_Battery', 
	'VMware_SASSATAPort'
]

def heartbeat(status):
    if args['verbose'] == False:
        print(zabbix_hostname+"\t"+args['item_name']+"[heartbeat]\t "+str(status))

def verboseoutput(message):
	if args['verbose']:
		print message

discovery = []
		
# connection to host
verboseoutput("Connection to "+args['host'])
wbemclient = pywbem.WBEMConnection("https://"+args['host'], (args['user'], args['password']), 'root/cimv2',no_verification=True)

for classe in ClassesToCheck :
	try:
		instance_list = wbemclient.EnumerateInstances(classe)
	except pywbem.cim_operations.CIMError,args:
		verboseoutput("Unknown CIM Error: %s" % args)
		heartbeat(0)
	except pywbem.cim_http.AuthError,arg: 
		verboseoutput("GLobal exit set to CRITICAL. AuthError. ")
		heartbeat(0)
		sys.exit()
	else:	
		for instance in instance_list :
		    #print(instance)
			elementName = instance['ElementName'].replace(':','')
			if instance['HealthState'] is not None:
				elementStatus = instance['HealthState']
				# Build list for item discovery
				discovery.append('{ "{#ITEM_KEY}":"'+elementName.replace(' ','')+'","{#ITEM_NAME}":"'+elementName+'" }')
				if args['show_inventory']:
					print(elementName.ljust(70)+" HealthState = %d" % elementStatus)
				elif args['zabbix_out']:
				    #args['item_discovery'] = False
				    print(zabbix_hostname+"\t"+args['item_name']+"["+elementName.replace(' ','')+"]\t"),
				    print(elementStatus)

# Print a heartbeat  
if args['zabbix_out']:
    heartbeat(1)

# Print the json decoded itemlist for item discovery rules
if args['item_discovery']:
    print(zabbix_hostname+"\t"+args['discovery_item_name']+"\t"+'{	"data":['),
    print(','.join(discovery)),
    print('] }')
