Adding new node:
- add DHCP entry in router
- add Pi-hole Local DNS entry
- set /etc/resolv.conf content to:
nameserver 192.168.1.201
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


Fix: "failed to create fsnotify watcher: too many open files"
checking: 
    sysctl fs.inotify
fixing temporarily:
    sysctl -w fs.inotify.max_user_watches=100000
    sysctl -w fs.inotify.max_user_instances=100000
fixing permanently:
add to /etc/sysctl.conf:
fs.inotify.max_user_watches=100000
fs.inotify.max_user_instances=100000


on plain Debian add missing NFS package:
nfs-common

on Proxmox 9 disable AppArmor:
1. mcedit /etc/default/grub
2.modify line to be:
GRUB_CMDLINE_LINUX_DEFAULT="quiet apparmor=0"
3. update-grub
4. reboot