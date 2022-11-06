https://longhorn.io/docs/1.1.0/deploy/install/install-with-helm/

Longhorn does leverage iSCSI, so extra configuration of the node may be required. This may include the installation of open-iscsi or iscsiadm depending on the distribution.

- label all nodes:
kubectl label nodes wuwek node.longhorn.io/create-default-disk=true

- removing label:
kubectl label node cobra node.longhorn.io/create-default-disk-


- Prepare disks:
gdisk /dev/sdb
- create new Linux partition
mkfs /dev/sdb1
- label it
e2label /dev/sdb1 longhorn
- find UUID
blkid
- make dir
mkdir /longhorn
- define in /etc/fstab
UUID=xxx   /longhorn  ext4   defaults    0   0
- mount
mount /longhorn

- make sure iscsi package is installed
apt-get install open-iscsi
