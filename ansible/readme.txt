Instal sshpass
brew install hudochenkov/sshpass/sshpass

- Use predefined role from Ansible Galaxy:
https://galaxy.ansible.com/xanmanning/k3s
https://galaxy.ansible.com/mrlesmithjr/mariadb-galera-cluster

- Install to specified folder 'roles':
ansible-galaxy install xanmanning.k3s -p ./roles
ansible-galaxy install mrlesmithjr.mariadb-galera-cluster -p ./roles
ansible-galaxy install ryankwilliams.ssh_copy_id -p ./roles

Run everything on hosts defined in inventory:

- key configuration
ssh-copy-id root@192.168.1.132

- configure Galera cluster
ansible-playbook -u root galera.yml -i inventory/galera/hosts.yml
- configure HA k3s cluster
ansible-playbook -u root k3s_ha.yml -i inventory/k3s/hosts.yml



Tips&Tricks
Encrypting string using password from textfile
ansible-vault encrypt_string --vault-password-file ~/.vault_pass_prv.txt 'secret_password' --name 'ansible_pass'
Encrypt whole file
ansible-vault encrypt registries.yaml --vault-password-file ~/.vault_pass_prv.txt
Encrypt single string, when vault file is in ansible.cfg:
ansible-vault encrypt_string  'somepassword' --name 'mariadb_mysql_root_password'
Manual restart of galera: https://galeracluster.com/library/training/tutorials/restarting-cluster.html

GALERA
1. Create VM
2. copy SSH key
3. Install roles
4. SSH once
- set 'adminer' password
5. run playbook for galera:
ansible-playbook -u root galera.yml -i inventory/galera/hosts.yml

K3S
1. Create VM - with public SSH key
LXC/Proxmox(bare metal):
2 run playbook for k3s
ansible-playbook -u root k3s_ha.yml -i inventory/k3s/hosts.yml
VM:
2 run playbook for k3s
ansible-playbook -u debian k3s_ha.yml -i inventory/k3s/hosts.yml
3 config is in /etc/rancher/k3s/k3s.yaml

###################################
Calico install:
From node:
kubectl create -f https://docs.projectcalico.org/manifests/tigera-operator.yaml
apply yaml:

# This section includes base Calico installation configuration.
# For more information, see: https://docs.projectcalico.org/v3.17/reference/installation/api#operator.tigera.io/v1.Installation
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  # Configures Calico networking.
  calicoNetwork:
    # Note: The ipPools section cannot be modified post-install.
    ipPools:
    - blockSize: 26
      cidr: 10.43.0.0/16
      encapsulation: VXLANCrossSubnet
      natOutgoing: Enabled
      nodeSelector: all()