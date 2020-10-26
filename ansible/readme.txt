We use predefined role from Ansible Galaxy:
https://galaxy.ansible.com/xanmanning/k3s
https://galaxy.ansible.com/mrlesmithjr/mariadb-galera-cluster

- Install to specified folder roles:
ansible-galaxy install xanmanning.k3s -p ./roles
- Install to home
ansible-galaxy install mrlesmithjr.mariadb-galera-cluster -p ./roles

Run everything on hosts defined in inventory:

- key configuration
ssh-copy-id root@192.168.1.132

- configuration HA
ansible-playbook k3s_ha.yml -i inventory/k3s/hosts.yml
ansible-playbook -u root galera.yml -i inventory/galera/hosts.yml
#ansible-playbook -u root --ask-pass galera.yml -i inventory/galera/hosts.yml



Tips&Tricks
Encrypting string using password from textfile
ansible-vault encrypt_string --vault-password-file ~/.vault_pass_prv.txt 'secret_password' --name 'ansible_pass'
Encrypt whole file
ansible-vault encrypt registries.yaml --vault-password-file ~/.vault_pass_prv.txt
Encrypt single string, when vault file is in ansible.cfg:
ansible-vault encrypt_string  'somepassword' --name 'mariadb_mysql_root_password'


1. Create VM
2. copy SSH key
3. Install roles
4. SSH once
- set 'adminer' password
5. run playbook for galera:
ansible-playbook -u root galera.yml -i inventory/galera/hosts.yml