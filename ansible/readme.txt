We use predefined role from Ansible Galaxy:
https://galaxy.ansible.com/xanmanning/k3s


- Install to specified folder
ansible-galaxy install xanmanning.k3s -p ./roles


Run everything on hosts defined in inventory:

- key configuration
ssh-copy-id root@192.168.1.132

- configuration HA
ansible-playbook k3s_ha.yml -i inventory/k3s/hosts.yml
ansible-playbook -u root galera.yml -i inventory/galera/hosts.yml
#ansible-playbook -u root --ask-pass galera.yml -i inventory/galera/hosts.yml



Tips&Tricks
Encrypting string using password from textfile
ansible-vault encrypt_string --vault-password-file ~/.vault_pass.txt 'secret_password' --name 'ansible_pass'
Encrypt whole file
ansible-vault encrypt registries.yaml --vault-password-file ~/.vault_pass.txt