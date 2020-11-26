How to use the playbook
-----------------------

#### The simplest way: 
`ansible-playbook -i inventory.ini -e @user_secret.yml setup-everything.yml`

#### The hard way:

- **Preparing environment:** `ansible-playbook -i inventory.ini -e @user_secret.yml setup-infra.yml`
- **Message Queue:** `ansible-playbook -i inventory.ini -e @user_secret.yml setup-message-queue.yml`
- **Corosync & Pacemaker:** `ansible-playbook -i inventory.ini -e @user_secret.yml setup-corosync-pacemaker.yml`
- **Database Server:** `ansible-playbook -i inventory.ini -e @user_secret.yml os-database.yml`
- **Identity Service:** `ansible-playbook -i inventory.ini -e @user_secret.yml os-keystone-setup.yml`
- **Image Service:** `ansible-playbook -i inventory.ini -e @user_secret.yml os-glance-setup.yml`
- **Compute Service:** `ansible-playbook -i inventory.ini -e @user_secret.yml os-nova-setup.yml`
- **Network Service:** `ansible-playbook -i inventory.ini -e @user_secret.yml os-neutron-setup.yaml`
- **Block Storage Service:** `ansible-playbook -i inventory.ini -e @user_secret.yml os-cinder-setup.yml`