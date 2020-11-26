1. Sử dụng CSF
 - Thay đổi giá trị trong ./vars/main.yml tương ứng
 - Thêm host cần chạy và role trong inventory  
 - ansible-playbook -i inventory playbook.yml --limit='master' -u root 
2. Các giá trị trong vars/main.yml 
- csf_binary: Nơi chứa perl script 
- csf_folder: Nơi build mã nguồn csf 
- csf_version: version của csf
- csf_config_file: File config chính
- csf_allow_config_file: File config chứa list IP allow, mặc định all port, In và Out 
- csf_deny_config_file: File config chứa list IP deny 
- csf_allow_ui_file: List IP allow access vào UI 
    #config sample 
- testing_mode: Chế độ test, reset mỗi 5 phút  bởi LFD 
- restrict_syslog: Cài đặt giới hạn đọc log 
- restrict_ui: Cài đặt giới hạn thay đỏi config từ UI 
    #access
- tcp_in: Các cổng mở mặc định chấp nhật kết nối vào 
- tcp_out: Các cổng cho phép kết nối đi ra 
- udp_in: Các cổng Udp vào 
- udp_out: Các cổng udp ra 
- icmp_in: ICMP IN
- icmp_out: ICMP out 
    #interface to apply 
- eth_apply: NIC to apply 
- eth_skip: NIC to ignore 
    #options 
- connect_tracking: Limit connect, rate
- process_tracking: Process check
- port_tracking: check port
- account_tracking: check /etc/password 
    #UI interface 
- ui_interface_master: Bật UI trên master
- ui_interface_slave: Tắt UI trên slave 
- ui_interface_port: Cổng UI , mặc định csf tự thêm luật 
- ui_interface: Interface cho ui
- ui_interface_user: User csf UI 
- ui_interface_password: password csf UI 
- ui_interface_access_private: Sử dụng ui.allow riêng 
- ui_interface_ip_access: Access từ IP riêng
    #lfd cluster 
- cluster_master: Mastter của cụm LFD 
- cluster_slave: slave của cụm LFD 
- cluster_port: Port của các thành viên 
- cluster_key: key của cluster
- cluster_block: Tự động gửi các config 
- cluster_config_master: ko nhận config trên master
- cluster_config_slave: nhận config trên slave
    #sshd port
- port_sshd: port sshd
    #file 

- custom_ip_access: IP ngoại lệ