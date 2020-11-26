1. Update version mới

- Đóng login, thông báo bảo trì, update CDN, update source code trên các server
ansible-playbook -i hosts roles/update_version.yml

- Mở Login, bỏ thông báo bảo trì
ansible-playbook -i hosts roles/open_login.yml

2. Setup mô trường cho server mới
ansible-playbook -i hosts play.yml
