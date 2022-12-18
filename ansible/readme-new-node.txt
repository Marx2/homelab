Adding new node:
- add DHCP entry in router
? add Pi-hole Local DNS entry
- add SSH keys: 
  ssh-copy-id root@<new host>
- remove search... from /etc/resolv.conf 
- add packages:
  apt-get install aptitude mc
- update:
  apt-get update
  apt-get dist-upgrade
- unattended upgrades:
  apt-get install unattended-upgrades apt-listchanges
- instal iscsi
  apt-get install open-iscsi
- reboot

- swap only if no free RAM:
add to /etc/sysctl.conf:
vm.swappiness=0

switch off swap:
- identify:
swapon -s
- disable
swapoff /dev/dm-0

Fix Longhorn problem:
apt install iptables
update-alternatives --set iptables /usr/sbin/iptables-legacy






on plain Debian add missing NFS package:
nfs-common
