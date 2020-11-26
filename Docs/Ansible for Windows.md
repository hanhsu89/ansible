# Ansible and Windows

https://github.com/nduytg/Ansible-Windows

https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html#winrm-encryption

https://cloudcraft.info/ansible-quan-tri-windows-server-2012/
https://cloudcraft.info/ansible-quan-tri-windows-server-2012-voi-ansible-phan-2/


Config
---

===> Basic
là giao thức chứng thực đơn giản, chỉ dùng username/password. Đây cũng là giao thức kém bảo mật nhất, dữ liệu nếu truyền qua HTTP thì có thể dễ dàng bị bẻ khóa. Chỉ hỗ trợ chứng thực bằng Local Account trên từng máy. Dùng cho môi trường Test/Dev, KHÔNG DÙNG CHO MÔI TRƯỜNG PRODUCTION

Cấu hình trên Ansible
	ansible_user: LocalUsername
	ansible_password: PasswordLocalUser
	ansible_connection: winrm
	ansible_winrm_transport: basic

Cấu hình trên Windows
Giao thức này mặc định là tắt, để bật lên thì ta dùng lệnh sau:
	Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value $true


===> Certificate
Đây là cách chứng thực dùng cặp certificate – private key, tương tự như dùng SSH key pair trên linux. Tuy nhiên format file và quá trình tạo key có chút khác biệt.

Cấu hình trên Ansible
	ansible_connection: winrm
	ansible_winrm_cert_pem: /path/to/certificate/public/key.pem
	ansible_winrm_cert_key_pem: /path/to/certificate/private/key.pem
	ansible_winrm_transport: certificate

Cấu hình trên Windows
Giao thức này mặc định là tắt, để bật lên thì ta dùng lệnh sau:
	Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $true



#=====================

#ansible_user: ansible
#ansible_password: 123@Hanhsu
#ansible_connection: winrm
#ansible_winrm_cert_pem: /etc/ansible/certs/cert.pem
#ansible_winrm_cert_key_pem: /etc/ansible/certs/cert_key.pem
#ansible_winrm_transport: certificate


ansible_user: ansible
ansible_password: 123@Hanhsu
ansible_connection: winrm
ansible_winrm_transport: basic
ansible_winrm_server_cert_validation: ignore


#=====================
- name: Install  notepad++ from chocolatey
  hosts: win-db
  tasks:
    - name: Install Notepad++
      win_chocolatey:
        name: notepadplusplus
        state: latest