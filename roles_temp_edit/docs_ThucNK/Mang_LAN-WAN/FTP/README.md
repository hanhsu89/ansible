# FTP
Ghi chép về giao thức FTP

## Mục lục 

[1. FTP là gì?](#what)

[2. Hoạt động](#activity)

[3. Cài đặt và cấu hình](#install)

[4. Bắt gói tin FTP bằng Wireshark](#wireshark)

[5. Tham khảo](#reference)

<a name="what"></a>
## 1. FTP là gì ?
FTP (File Transfer Protocol) là giao thức trao đổi tập tin qua mạng lưới truyền thông, được định nghĩa trong [RFC-959](https://tools.ietf.org/html/rfc959). FTP được xây dựng trên kiến trúc client-server và sử dụng kết nối riêng biệt giữa hai luồng điểu khiển và dữ liệu. Người dụng có thể xác thực bằng cách sử dụng username và password, cũng có thể sử dụng kết nối nặc danh nếu máy chủ cấu hình cho phép điều đó.

<a name="activity"></a>
## 2. Hoạt động 

<img src="http://i.imgur.com/V0yYH2j.png">

Khác với nhiều giao thức trong mô hình TCP/IP thông thường sử dụng 1 đường kết nối, FTP sử dụng 2 đường kết nối riêng biệt:
- Cổng 21 cho kết nối điều khiển
- Cổng 20 cho truyền tập tin
Việc sử dụng 2 đường truyền tạo sự linh hoạt nhưng cũng tạo nên sự phức tạp nhất định.

##### Mô hình hoạt động 

<img src="http://users.skynet.be/spouseele/FTP/FTP-overview.gif" alt="FTP Model">

Protocol Interpreter (PI) là thành phần quản lý kênh điều khiển, nhiệm vụ của nó là phát và nhận lệnh

Data Transfer Process (DTP) có chức năng gửi và nhận dữ liệu giữa client và server

Bên cạnh đó, phía Client còn có thêm giao diện người dùng (user interface)

##### Thứ tự tiến trình 

- FTP Client liên lạc với FTP server ở cổng 21, sử dụng giao thức TCP 
- Client xác thực trên kết nối điều khiển sử dụng username và password
- Client gửi lệnh qua kết nối điều khiển 
- Khi server nhận được lệnh, nó mở cổng 20 để truyền file
- Khi truyền xong một file, server đóng kết nối dữ liệu

<a name="install"></a>
## 3. Cài đặt và cấu hình 

Để sử dụng dịch vụ FTP, Linux sử dụng gói phần mềm có tên : **vsftpd**

#####Cài đặt trên CentOS 7 : 
https://github.com/locvx1234/FTP/blob/master/install_configue_manual_vsftpd_centos7.md

#####Cài đặt trên Ubuntu : 

	sudo apt-get install vsftpd
	
#####Cấu hình vsftpd :

	sudo vi /etc/vsftpd.conf

#####Một số thông số cần lưu ý : 

- Tắt truy cập ẩn danh :

	anonymous_enable=NO 

- Bỏ ghi chú ở tùy chọn `local_enable` và cho phép người dùng cục bộ truy cập và ghi vào thư mục :

	local_enable=YES
	
	write_enable=YES
	
- Bỏ ghi chú ở `chroot_local_user` , tất cả user sẽ hoạt động trong `chroot` của họ và sẽ không được quyền truy cập vào các phần khác của server.

	chroot_local_user=YES

- Các thông số khác

listen=YES/NO : Chế độ standalone, với các vsftpd đơn lẻ phải để YES, nếu không sẽ không thể khởi động được 

anonymous_enable=YES/NO : anonymous được phép login vào FTP Server

anon_upload_enable=YES/NO : kết hợp với write_enable=YES thì anonymous được phép upload tập tin trong thư mục cha có quyền ghi

anon_mkdir_write_enable=YES/NO : kết hợp với write_enable=YES thì anonymous được phép tạo thư mục mới trong thư mục cha có quyền ghi

dirmessage_enable=YES/NO : hiển thi ra 1 thông điệp khi người dùng di chuyển vào thư mục

chown_uploads=YES/NO : tất cả những tập tin được upload bởi user anonymous được sở hữu bởi user được chỉ ra trong chown_username

chown_username : chỉ ra user sở hữu những tập tin được upload bởi user anonymous (mặc định là user root)

chroot_local_user=YES/NO : người dùng di chuyển đến home directory của mình sau khi login vào



#####Một số file khác 

- /etc/vsftpd.ftpusers: Những user không được phép login vào **vsftpd**
- /etc/vsftpd.user_list: Cấu hình để cấm hoặc cho phép người dùng được truy cập FTP server. (Phụ thuộc vào `userlist_deny` trong file cấu hình)

##### Sau tất cả, chúng ta cần restart dịch vụ để những thay đổi có hiệu lực :

	 sudo service vsftpd restart
	 
#####Tạo thư mục và phân quyền truy cập 

- Tạo một thư mục mới bên trong `home`:

		mkdir /home/ftp

- Tạo 2 thư mục cho 2 user 

		mkdir /home/ftp/user1_dir
	
		mkdir /home/ftp/user2_dir

- Tạo 2 tài khoản 

		useradd -d /home/ftp/user1_dir user1
	
		passwd user1
	
		useradd -d /home/ftp/user1_dir user2
	
		passwd user2
	
- Thay đổi quyền sở hữu: 
	
		chown -R user1:user1 /home/ftp/user1_dir 
	
		chown -R user2:user2 /home/ftp/user2_dir 

- Thay đổi quyền truy cập cho từng user 

		chmod 750 /home/ftp/user1_dir 
	
		chmod 750 /home/ftp/user2_dir 
	
- Tạo những thay đổi cần thiết trong thư mục con

##### Giới hạn kết nối 

- Tốc độ truyền dữ liệu tối đa

		local_max_rate=10000

- Số client tối đa

		max_clients=50  

- Số kết nối tối đa cho mỗi IP

		max_per_ip=2	
		
##### Một số lab 

- Cho phép anonymous được phép truy cập FTP server

		anonymous_enable=YES

- Thay đổi thư mục gốc của FTP Server thành /data/ftp
	
Sau khi tạo thư mục cần thay đổi, thêm vào cuối file cấu hình : 
	
	anon_root=/data/ftp

- Anonymous được upload file trong /data/ftp/upload

```	
write_enable=YES
anon_upload_enable=YES
```

Cấp quyền cho nó 
	
	#chmod 755 /data/ftp/upload

- Anonymous được upload directory trong /data/ftp/upload

```
write_enable=YES
anon_mkdir_write=YES
```

- Các user local login vào Ftp Server

	local_enable=YES

- Cấm user locvx login vào server

Thêm locvx vào cuối file /etc/ftpusers (danh sách các user bị chặn)


### Truy cập vào FTP server

Do firewall trên máy chủ không cho phép dịch vụ FTP nên ta tắt firewall bằng lệnh :

	$ sudo ufw disable
	
##### Sử dụng giao diện console
Dùng Command Line ftp tới một máy chủ :

	> ftp host

<img src="http://i.imgur.com/3JlrouO.png">

Sử dụng `help` để xem các lệnh hỗ trợ

##### Browser

Nhập ftp://host để thiết lập kết nối ftp đến server 

<img src="http://i.imgur.com/LdjW5J2.png">

##### File zilla
Nhập Host, Username, Password, và Port = 21. Sau đó Quickconnect

<img src="http://i.imgur.com/cDdEeM3.png">

<a name="wireshark"></a>
## 4. Bắt gói tin FTP bằng Wireshark

Khi kết nối với máy chủ ftp (192.168.175.128) qua port 21

Nếu thành công sẽ nhận được respond 220 và sau đó là quá trình xác thực bằng username và password.

<img src="http://i.imgur.com/ctmacB2.png">

Khi copy file từ client lên server, ta thấy rằng port nhận không phải lúc nào cũng là 20 như mô tả ở trên.

Điều này liên quan đến 2 chế độ hoạt động của FTP server là Active FTP và Passive FTP. 

<img src="http://i.imgur.com/3stBfiO.png">

<a name="reference"></a>
## 5. Tham khảo

Book : Computer Networking A Top-Down Approach 6th-edition - Kurose Ross.

http://sinhvienit.net/forum/tim-hieu-ve-giao-thuc-ftp.28754.html

http://thachpham.com/hosting-domain/ftp-la-gi.html

http://kenhgiaiphap.vn/Detail/1132/Cau-hinh-ftp-server-voi-vsftpd.html

https://wiki.archlinux.org/index.php/Very_Secure_FTP_Daemon