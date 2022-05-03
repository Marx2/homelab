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
  deb http://download.proxmox.com/debian/pve bullseye pve-no-subscription
- update:
  apt-get update
  apt-get dist-upgrade
- unattended upgrades:
  apt-get install unattended-upgrades apt-listchanges
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

Fix Longhorn problem:
update-alternatives --set iptables /usr/sbin/iptables-legacy

on plain Debian add missing NFS package:
nfs-common
