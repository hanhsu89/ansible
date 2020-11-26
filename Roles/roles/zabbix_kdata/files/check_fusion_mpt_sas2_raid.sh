#!/bin/bash

#
# Checks the status of the hardware raid.
# Checkresults are returned integer.
# The script expects one parameter: The check you want to perform .
# The second parameter, the adapter number, is optional. If adapter number is missing, 0 is set.
#

SAS2IRCU_BIN=/usr/sbin/sas2ircu

# Check if SAS2IRCU is installed and executable
if [ -e $SAS2IRCU_BIN ]
then
    true
else
    echo "SAS2IRCU missing";
    exit 1
fi

# Set the adapternumber
if [ $2 ]
then
    ADAPTER=$2
else
    ADAPTER="0"
fi

SAS2IRCU="sudo $SAS2IRCU_BIN $ADAPTER DISPLAY"

case $1 in
    mediaerrors)
        # Return the total number of disk which has reported a state other then Optimal.
        $SAS2IRCU|grep -A3 "Device is a Hard disk"|grep State|grep -vc "Optimal (OPT)"
    ;;
    raiderrors)
        # Return the number of arrays which do not have state "Okay"
        $SAS2IRCU|grep "Status of volume"|grep -vc "Okay (OKY)"
    ;;
    firmware)
        # Return the version of the firmware
	$SAS2IRCU |grep "Firmware version"|cut -d":" -f2|tr -d " "
    ;;
esac
