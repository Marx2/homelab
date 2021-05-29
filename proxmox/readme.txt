Adding new node:
- add DHCP entry in router
- add Pi-hole Local DNS entry
- install Proxmox
- add SSH keys: 
  ssh-copy-id root@<new host>
- remove search... from /etc/resolv.conf 
- add packages:
  apt-get install aptitude mc
- disable paid repositories
  mv /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/pve-enterprise.list.disabled
- add free reposittory: pve-no-subscription.list
  deb http://download.proxmox.com/debian/pve buster pve-no-subscription
- update:
  apt-get update
  apt-get dist-upgrade
- unattended upgrades:
  apt-get install unattended-upgrades apt-listchanges
- add wireguard: https://nixvsevil.com/posts/wireguard-in-proxmox-lxc/
  apt install pve-headers
  vi /etc/apt/sources.list
  add  deb http://deb.debian.org/debian buster-backports main
  apt update
  apt install -t buster-backports wireguard-dkms
  modprobe wireguard
  echo "wireguard" >> /etc/modules-load.d/modules.conf
- reboot
- add to Proxmox cluster

- swap only if no free RAM:
add to /etc/sysctl.conf:
vm.swappiness=0

switch off swap:
- identify:
swapon -s
- disable
swapoff /dev/dm-0