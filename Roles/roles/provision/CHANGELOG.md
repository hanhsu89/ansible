Cuonglq - 19/02/2019

File edited
- roles/users/vars/main.yml

## Changed

* Cụm Pay
  - Cập nhập IP 192.168.35.0/24 (thay thế 10.0.0.0/24)
  - Chuyển tất cả về thành một block (trước để phân tán)
  - Cập nhập cụm ELK PAY
  - Add user `deploy`
* Appvn-Prod
  - Chuyển tất cả về thành một block
  - Cập nhập Store-Appvn
  - Add user `deploy`
* Appvn-SG
  - Chuyển tất cả về thành một block
  - Cập nhập lại tên
  - Add user `deploy`

## Removed
- Xóa cụm Appvn-store cũ (8 server)

