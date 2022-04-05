make sure certificate exists on new nodes

upgrade xamanning role:
ansible-galaxy install xanmanning.k3s -p ./roles --force

run playbook for k3s
ansible-playbook -u root k3s_ha.yml -i inventory/k3s/hosts.yml