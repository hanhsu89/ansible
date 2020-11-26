rsync -Pav $(find /home/light1/{{ game_server }}/db/ -name "database.ld.*" -cmin -30)  root@192.168.31.10:/data/{{ game_server }}/

