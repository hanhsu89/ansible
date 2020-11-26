#!/usr/bin/python
# -*- coding:utf-8 -*-

####
#
# NAME:		check_smartarray.py
#
# AUTHOR:	Christophe Robert - christophe °dot° robert °at° cocoche °dot° fr
#
# DESC:		Check Hpacucli results for RAID status on Linux - hpacucli command line tool
#
#			Script compatibility : Python 2+
#			Return Values :
#				No problems - OK (exit code 0)
#				Drive status != OK but not "Failed" - WARNING (exit code 1)
#				Drive status is "Failed" - CRITICAL (exit code 2)
#
#				TODO : Script errors - UNKNOWN (exit code 3)
#
# VERSION:	1.0 - Initial dev. - 09-02-2012 (02 Sept. 2012)
#		1.1 - Correcting some errors and add comments - 09-15-2013 (15 Sept. 2013)
#			* Add SAS array to be considerated (only SATA was before)
#			* Add comments
#			* Add UNKNOWN mark - script errors 
#		1.2 - Correcting some errors - 09-24-2013 (24 Sept. 2013)
#			* Add SCSI array to be considerated
#			* Add comments
#		1.3 - Modify script from Windows PowerShell command tool to Python one's - 01-07-2015 (07 Jan. 2015)
#		1.4 - Add controller, battery and cache status checks - 01-08-2015 (08 Jan. 2015)
#		1.5 - Modify result analisys - 01-12-2015 (12 Jan. 2015)
#
####

import os
import sys
import re
from subprocess import *
import logging
import logging.handlers

class ReadHPSmartArrayStatus:

	def __init__(self, tuple, logger):
		self.nagios = tuple
		self.logger = logger

		#creation de table de hash qui permet d'associer une clé et une valeur
		self.system = {'ctrl': [], 'array': [], 'logical': [], 'physical': []}
		self.ctrl_nb = 0
		self.array_nb = 0
		self.lv_nb = 0
		self.pd_nb = 0

	def process(self):
		for element in self.nagios:
			sata = re.compile('^.*array.*SATA.*$')
			sas = re.compile('^.*array.*SAS.*$')
			scsi = re.compile('^.*array.*SCSI.*$')
			smart = re.compile('^Smart Array .*$')
			logical = re.compile('^.*logicaldrive.*$')
			physical = re.compile('^.*physicaldrive.*$')
			
			# Insert all controllers in dedicated list of dict
			if (smart.match(element)):
				self.logger.debug('--Debug-- Enter smart')
				self.logger.debug('--Debug-- Value = ' + element)
				self.ctrl_nb += 1
				self.system['ctrl'].append(element)
				self.logger.debug('--Debug-- Dict :' + str(self.system))
				
			# Insert all arrays in dedicated list of dict
			elif (sata.match(element) or sas.match(element) or scsi.match(element)):
				self.logger.debug('--Debug-- Enter array')
				self.logger.debug('--Debug-- Value = ' + element)
				self.array_nb += 1
				self.system['array'].append(element)
				self.logger.debug('--Debug-- Dict :' + str(self.system))
			
			# Insert all logicaldrives in dedicated list of dict
			elif (logical.match(element)):
				self.logger.debug('--Debug-- Enter logical')
				self.logger.debug('--Debug-- Value = ' + element)
				# Add the next logical drive to the previous array dict
				self.lv_nb += 1
				self.system['logical'].append(element)
				self.logger.debug('--Debug-- Dict :' + str(self.system))
		
			# Insert all physicaldives in dedicated list of dict
			elif (physical.match(element)):
				self.logger.debug('--Debug-- Enter physical')
				self.logger.debug('--Debug-- Value = ' + element)
				# Add the next physical drive to the previous logical drive dict
				self.pd_nb += 1
				self.system['physical'].append(element)
				self.logger.debug('--Debug-- Dict :' + str(self.system))
			
		self.logger.debug('--Debug-- Show "system" dict content')
		self.logger.debug('--Debug-- Value = ' + str(self.system))
	
		return self.system


class GetErrors:

	def __init__(self, buffer, logger):
		self.errors = {'CRITICAL': [], 'WARNING': [], 'UNKNOWN': []}
		self.tocheck = buffer
		self.logger = logger
		self.nb_ctrl = 0
		self.nb_array = 0
		self.nb_logical = 0
		self.nb_physical = 0
		
	def check(self):
		sata = re.compile('^.*array.*SATA.*$')
		sas = re.compile('^.*array.*SAS.*$')
		scsi = re.compile('^.*array.*SCSI.*$')
		logical = re.compile('^.*logicaldrive.*$')
		physical = re.compile('^.*physicaldrive.*$')

		# For each controller found, check errors and find S/N
		for i in range(len(self.tocheck['ctrl'])):
			self.logger.debug('--Debug-- Controller : ' + str(self.tocheck['ctrl'][i]))
			self.nb_ctrl += 1

			#self.logger.debug('--Debug-- S/N : ' + self.tocheck['ctrl'][i].split('sn: ')[1].split(')')[0])
			self.logger.debug('--Debug-- Slot : ' + self.tocheck['ctrl'][i].split('Slot ')[1].split(' ')[0])
			ctrl_status = Popen(['sudo', 'hpacucli', 'ctrl', 'slot=' + self.tocheck['ctrl'][i].split('Slot ')[1].split(' ')[0], 'show', 'status'], stdout=PIPE)
			res = ctrl_status.communicate()[0]
			ctrl_status.stdout.close()
			
			ctrl = []
			for r in res.splitlines():
				r = r.lstrip()
				logger.debug(str(r))
				if (r != ''):
					ctrl.append(r)

			self.logger.debug('--Debug-- Controller internal status : ' + str(ctrl))
			for element in ctrl:
				if re.compile('.*Status:.*').match(element):
					self.logger.debug('--Debug-- Controller element status : ' + element)
					if element.split(': ')[1].split('\n')[0] != 'OK':
						self.errors['WARNING'].append(element)

		# For each array found, check errors
		for i in range(len(self.tocheck['array'])):
			self.logger.debug('--Debug-- Enter "array"')
			self.logger.debug('--Debug-- Value = ' + str(self.tocheck['array'][i]))
			self.nb_array += 1
			
		# For each logicaldrive found, check errors
		for i in range(len(self.tocheck['logical'])):
			self.logger.debug('--Debug-- Enter "logicaldrive"')
			self.logger.debug('--Debug-- Value = ' + str(self.tocheck['logical'][i]))
			self.nb_logical += 1
			
			if re.compile('^.*OK.*$').match(self.tocheck['logical'][i]):
				self.logger.debug(re.compile('^.*OK.*$').match(self.tocheck['logical'][i]))
				pass
			elif re.compile('^.*Failed.*$').match(self.tocheck['logical'][i]):
				self.logger.debug(re.compile('^.*Failed.*$').match(self.tocheck['logical'][i]))
				self.errors['CRITICAL'].append(self.tocheck['logical'][i])
			elif re.compile('^.*Recover.*$').match(self.tocheck['logical'][i]):
				self.logger.debug(re.compile('^.*Recover.*$').match(self.tocheck['logical'][i]))
				self.errors['WARNING'].append(self.tocheck['logical'][i])
			else:
				self.logger.debug(self.tocheck['logical'][i])
				self.errors['UNKNOWN'].append(self.tocheck['logical'][i])
			
		# For each logicaldrive found, check errors
		for i in range(len(self.tocheck['physical'])):						
			self.logger.debug('--Debug-- Enter "physicaldrive"')
			self.logger.debug('--Debug-- Value = ' + str(self.tocheck['physical'][i]))
			self.nb_physical += 1
			
			if re.compile('^.*OK.*$').match(self.tocheck['physical'][i]):
				self.logger.debug(re.compile('^.*OK.*$').match(self.tocheck['physical'][i]))
				pass
			elif re.compile('^.*Failed.*$').match(self.tocheck['physical'][i]):
				self.logger.debug(re.compile('^.*Failed.*$').match(self.tocheck['physical'][i]))
				self.errors['CRITICAL'].append(self.tocheck['physical'][i])
			elif re.compile('^.*Rebuilding.*$').match(self.tocheck['physical'][i]):
				self.logger.debug(re.compile('^.*Rebuilding.*$').match(self.tocheck['physical'][i]))
				self.errors['WARNING'].append(self.tocheck['physical'][i])
			else:
				self.logger.debug(self.tocheck['physical'][i])
				self.errors['UNKNOWN'].append(self.tocheck['physical'][i])
		
		self.logger.debug('--Debug-- Errors dict : ' + str(self.errors))
		return self.errors, self.nb_ctrl, self.nb_array, self.nb_logical, self.nb_physical
	

### Core ###

logger = logging.getLogger('check_smartarray')
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address='/dev/log')
logger.addHandler(handler)

hpacucli = Popen(['sudo', 'hpacucli', 'ctrl', 'all', 'show', 'config'], stdout=PIPE)
res = hpacucli.communicate()[0]
hpacucli.stdout.close()

nagios = []
for r in res.splitlines():
	r = r.lstrip()
	logger.debug(str(r))
	if (r != ''):
		nagios.append(r)

logger.debug('--Debug-- List command results :')
logger.debug(nagios)

nb_warning = 0
nb_critical = 0
nb_unknown = 0
tosend = ""

try:
	# Parse and analyse returned lines
	state = ReadHPSmartArrayStatus(nagios, logger)
	config = state.process()

	# Check errors
	errors = GetErrors(config, logger)
	health, nb_ctrl, nb_array, nb_logical, nb_physical = errors.check()

	logger.debug('--Debug-- Health dict : ' + str(health))
	
	if len(health['CRITICAL']):
		logger.debug('--Debug-- Enter critical')
		nb_critical += 1
		for l in range(len(health['CRITICAL'])):
			tosend += 'CRITICAL - ' + health['CRITICAL'][l] + '\n'
	elif len(health['WARNING']) and nb_critical==0:
		logger.debug('--Debug-- Enter warning')
		nb_warning += 1
		for l in range(len(health['WARNING'])):
			tosend += 'WARNING - ' + health['WARNING'][l] + '\n'
	elif len(health['UNKNOWN']) and nb_critical==0 and nb_warning==0:
		logger.debug('--Debug-- Enter unknown')
		nb_unknown += 1
		for l in range(len(health['UNKNOWN'])):
			tosend += 'UNKNOWN - ' + health['UNKNOWN'][l] + '\n'
	elif nb_ctrl == 0 or nb_array == 0 or nb_logical == 0 or nb_physical == 0:
		logger.debug('--Debug-- Enter unknown')
		nb_unknown += 1
		tosend += 'UNKNOWN - One of element of these : controller (' + str(nb_ctrl) + '), array (' + str(nb_array) + '), logicaldrive (' + str(nb_logical) + ') or physicaldrive (' +str(nb_physical) + ') is missing !\n'
	else:
		tosend = 'OK - RAID status is good - Nb Ctrl : ' + str(nb_ctrl) + ' - Nb Array : ' + str(nb_array) + ' - Nb logicaldrive : ' + str(nb_logical) + ' - Nb physicaldrive : ' + str(nb_physical)

	tosend = tosend.strip('^\n')
	logger.debug(str(tosend))

except Exception as e:
	tosend = str(e)
	logger.debug('--Debug-- Exception : ' + tosend)
	print('--Debug-- Exception : ' + tosend)

finally:
	print(str(tosend))
	if nb_critical != 0:
		raise SystemExit, 2
	elif nb_warning != 0:
		raise SystemExit, 1
	elif nb_unknown != 0:
		raise SystemExit, 3
	else:
		raise SystemExit, 0

sys.exit(0)