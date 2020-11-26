## Cài đặt vsftpd trên CentOS 7

### Update và install gói vsftpd 

	# yum check-update
	# yum -y install vsftpd

### Cấu hình

Để khôi phục lại file cấu hình mặc đinh nếu ta cấu hình sai mà không rõ biết cách sửa thì ta cần backup file cấu hình

	# cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf.bak
	
Bắt đầu cấu hình :

	# vi /etc/vsftpd/vsftpd.conf
	
Một số cấu hình khuyến cáo :

	anonymous_enable=NO 
	ascii_upload_enable=YES
	ascii_download_enable=YES
	chroot_local_user=YES
	allow_writeable_chroot=YES
	pasv_enable=Yes
	pasv_min_port=40000
	pasv_max_port=40100
	
### Restart lại vsftpd

	# systemctl restart vsftpd
	
### Đổi port vsftpd

        # vi /etc/vsftp/vsftpd.conf
	# listen_port=2020
        # ftp_data_port=2121

### Thêm dịch vụ FTP trong firewall để cho phép mở cổng ftp 

	# firewall-cmd --permanent --add-service=ftp
	# firewall-cmd --reload
	
Nếu thấy phức tạp, trong quá trình luyện tập bạn có thể stop firewall bằng lệnh 

	# systemctl stop firewalld
	
### Tạo user 

	# groupadd ftpaccess
	# useradd -m locvu -s /sbin/nologin -g ftpaccess
	# passwd locvu
	
	# chown root /home/locvu
	# chmod 750 /home/locvu
	
	# mkdir /home/locvu/www
	# chown locvu:ftpaccess /home/locvu/www

	
	
### THam khảo 

http://www.krizna.com/centos/setup-ftp-server-centos-7-vsftp/
