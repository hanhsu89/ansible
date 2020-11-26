#!/bin/bash
# Install FTP on Ubuntu && CentOS

check_permission()
{
	if [ $(id -u) -ne 0 ]
	then 
		echo "Permission denied! You need login as root ^^"
		exit $1
	fi
}

check_distro()
{
	os=$(lsb_release -is)
	echo $os
}

install_package()
{
	if [ $(check_distro) == 'Ubuntu' ]
	then
		apt-get update
		apt-get -y install vsftpd
	elif [ $(check_distro) == 'CentOS' ]
	then
		yum -y update
		yum -y install vsftpd
	else 
		echo "Unsupport this OS! :/" 
	fi
}

main()
{
	check_permission
	install_package
}

main
