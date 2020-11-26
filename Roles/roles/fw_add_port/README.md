<h3>Thực hiện add port trên iptables cho server game theo yêu cầu</h3>


<h4>Add port dbgame</h4>


    ansible-playbook -i inventory playbook.yml --tags "dbgame"

<h4>Add port game</h4>

    ansible-playbook -i inventory playbook.yml --tags "game"

<h3>Thêm port trong vars/main.yml</h3>

<h4>Example</h4>

open_port_dbgame:
 
  - port: 22

    protocol: tcp

  - port: 43557

    protocol: tcp

  - port: 11407

    protocol: tcp


open_port_game:

  - port: 26000:26001

    protocol: tcp

  - port: 26002

    protocol: tcp

