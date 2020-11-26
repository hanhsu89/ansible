# Deploy


1. Deploy code cho server cũ

    ```bash
    $ ansible-playbook -i after_hosts site.yml --limit='Appota-logs' -u manhnv --tags=users
    ```

- Nếu server mới đã config ssh_port thì thêm IP port vào file `after_hosts`

    ```bash
    $ ansible-playbook -i after_hosts site.yml --limit='Appota-logs' -u root -k --tags=users
    $ ansible-playbook -i after_hosts site.yml --limit='Appota-logs' -u manhnv -k --ask-become-pass --tags=users
    ```
    - thêm `-k` nếu server cũ đang dùng passwd
    - thêm `--ask-become-pass` nếu dùng với user thường + sudo

- ***hosts file:*** các server mới cài đặt chưa config ssh_port (port 22 default)
- ***after_hosts:*** host sau khi được thêm ssh_port 
- ***--tags="users":*** Execute tất cả task đước gắn tags này (VD: users, accounts, install_sudo...)
- ***--untagged="install_sudo":*** vd không execute với task được gắn tag này
- ***--limit="Appota-logs":*** Giới hạn các host,ip được execute (VD: chỉ push user với cụm Appota-logs được định nghĩa trong inventory và users var)
- ***-u: manhnv*** Chạu với user nào đã push từ trước (nếu user đó không bị giới hạn sudo)

2. Deploy cho server mới

- Thêm IP server mới vào file `hosts` và `roles/users/vars/main.yml`

- Chạy lệnh:

    ```bash
    $ ansible-playbook -i hosts site.yml --limit='<ip_server>' -u root -k
    ```

3. Thêm user mới:

- Thêm publish key vào `roles/users/file/publish/<user>.pub`
- Thêm "name" trong `roles/user/vars/main.yaml` (Giống manhnv )
- Thêm IP vào server trong `roles/user/vars/main.yml`

Note: Tên user khi thêm vào ở mọi vị trí phải giống nhau