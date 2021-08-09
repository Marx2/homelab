OMV
problem: stale NFS file handle
solution: add inodecalc=path-hash,noforget to MergerFS options

https://github.com/trapexit/mergerfs#inodecalc
https://github.com/trapexit/mergerfs#nfs-clients-returning-estale--stale-file-handle


OMV installation:
- reconfigure timezone from UI
- add group via import:
marx;1000;
- add user via import
marx;1000;;;<password>;/bin/bash;marx;1
- install extras https://wiki.omv-extras.org/
- install plugins: flashmemory, snapraid, unionfilesystems
- reconfigure /etc/fstab for flashmemory
- fix mdadm error: https://forum.openmediavault.org/index.php?thread/21351-mdadm-no-arrays-found-in-config-file-or-automatically/&pageNo=6
  echo 'RESUME=UUID=<the UUID of your boot drive here>' > /etc/initramfs-tools/conf.d/resume
  # mdadm --detail --scan >> /etc/mdadm.conf - seems not to work as config is in /etc/mdadm/mdadm.conf (?)
  omv-salt deploy run mdadm
  update-initramfs -u
  update-grub
- make sure swap is disabled in /etc/fstab
- pass disks from silver to omv:
    qm set 103 -scsi1 /dev/disk/by-uuid/2c34fd7e-8049-4025-8d63-a990392a2478
    qm set 103 -scsi2 /dev/disk/by-uuid/c32947b3-d50b-4cc8-819e-4373f94bebab
    qm set 103 -scsi3 /dev/disk/by-uuid/47526c91-abc2-4154-a10d-f81c9c3293b9
    qm set 103 -scsi4 /dev/disk/by-uuid/1e8570fb-0c4e-49d4-89d8-9b4ebdbe943d
    qm set 103 -scsi5 /dev/disk/by-uuid/677d23f4-37c5-4f92-80f1-d8c9340523b9
    qm set 103 -scsi6 /dev/disk/by-uuid/c9efc14e-8432-453b-b618-c1ce67a5cbb3
- configure unionfilesystem (mergerfs) - add all disks
- configure snapraid:
  add parity drive
  add ata disks
- configure shared folders
/backup
/media
/media/podcasts
/kubernetes/prometheus (directly)
/recordings
- configure NFS



in Silver
lrwxrwxrwx 1 root root  10 Aug  7 08:58 2c34fd7e-8049-4025-8d63-a990392a2478 -> ../../sda1 WD 3TB
lrwxrwxrwx 1 root root  10 Aug  3 10:00 c32947b3-d50b-4cc8-819e-4373f94bebab -> ../../sdb1 Hitachi 3TB SAS
lrwxrwxrwx 1 root root  10 Aug  7 08:59 47526c91-abc2-4154-a10d-f81c9c3293b9 -> ../../sdc1 Seagate 1TB
lrwxrwxrwx 1 root root  10 Aug  7 08:59 1e8570fb-0c4e-49d4-89d8-9b4ebdbe943d -> ../../sdd1 WD 4TB
lrwxrwxrwx 1 root root  10 Aug  7 08:59 677d23f4-37c5-4f92-80f1-d8c9340523b9 -> ../../sde1 HGST
lrwxrwxrwx 1 root root  10 Aug  7 08:59 c9efc14e-8432-453b-b618-c1ce67a5cbb3 -> ../../sdf1 HGST

in OMV
lrwxrwxrwx 1 root root   9 Aug  8 18:11  hgst4-1 -> ../../sdc -> 677d23f4-37c5-4f92-80f1-d8c9340523b9 pusty
lrwxrwxrwx 1 root root   9 Aug  8 18:11  hgst4-2 -> ../../sdb -> c9efc14e-8432-453b-b618-c1ce67a5cbb3 pusty
lrwxrwxrwx 1 root root   9 Aug  8 18:11  hsas -> ../../sdf -> c32947b3-d50b-4cc8-819e-4373f94bebab media
lrwxrwxrwx 1 root root   9 Aug  8 18:11  seag1 -> ../../sde -> 47526c91-abc2-4154-a10d-f81c9c3293b9 kuberneeets prometheus
lrwxrwxrwx 1 root root   9 Aug  8 18:11  wd3 -> ../../sdg -> 2c34fd7e-8049-4025-8d63-a990392a2478 backup, media (rozne)
lrwxrwxrwx 1 root root   9 Aug  8 18:11  wd4 -> ../../sdd -> 1e8570fb-0c4e-49d4-89d8-9b4ebdbe943d pusty
