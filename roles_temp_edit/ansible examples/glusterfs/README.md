# GlusterFS

1. Install GlusterFS

    Edit blockinfile edit /etc/hosts before run

    ```ansible-playbook -i after_hosts playbook.yml --limit='glusterfs_example' --tags=install_glusterfs
    ```

2. Install Heketi

    ```ansible-playbook -i after_hosts playbook.yml --limit='glusterfs_example' --tags=install_heketi
    ```