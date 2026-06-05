General approach to devices:
vendor:device

PCI:
lspci -nn
00:02.0 VGA compatible controller [0300]: Intel Corporation Device [8086:3185] (rev 03)
class: 0300
vendor: 8086
device: 3185


USB:
lsusb
Bus 001 Device 009: ID 1cf1:0030 Dresden Elektronik
vendor: 1cf1
device: 0030

lsusb -v
  bDeviceClass            2 Communications
class: 02