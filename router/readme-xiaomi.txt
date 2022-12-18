https://github.com/mikeeq/xiaomi_ax3200_openwrt


how to factory reset:
1. Press the Reset button on the back of the device. Hold it for a few seconds. 
2. Now the LED on the front of the device will light up and turn from blue to yellow.
3. Release Reset Button and give XIAOMI Redmi AX6 WiFi Router a few moments to reboot completely

With the method I applied, two devices are required.

If an ethernet cable is connected from the lan port of the device to which the method will be applied to the wan port of the second RB01, and the second device is returned to its factory settings from the button, it is added to the first device in mesh mode (mode 3). So the main device will be in mode 4.

First we will confirm that the device is in netmode 4 from this link.

Login to the router, in another tab use your token with link

http://192.168.31.1/cgi-bin/luci/;stok={token}/api/xqnetwork/get_netmode

If result is {"netmode":4,"code":0} proceed;

Note: Only use this method when the router is connected to the computer via ethernet connection. Because wifi connection will not be available from the first command, when you restart after the 3rd command, wifi connection will be fixed. After the procedure is complete, I recommend that you reset the device back to factory settings.

1- Login to the router, in another browser tab use your token with link;

http://192.168.31.1/cgi-bin/luci/;stok={token}/api/misystem/set_sys_time?timezone=%20%27%20%3B%20zz%3D%24%28dd%20if%3D%2Fdev%2Fzero%20bs%3D1%20count%3D2%202%3E%2Fdev%2Fnull%29%20%3B%20printf%20%27%A5%5A%25c%25c%27%20%24zz%20%24zz%20%7C%20mtd%20write%20-%20crash%20%3B%20

Link returns with result {"code":0}

Restart the router from the interface

2- When the device is turned on login to the router, in another browser tab use your new token with link;

http://192.168.31.1/cgi-bin/luci/;stok={token}/api/misystem/set_sys_time?timezone=%20%27%20%3B%20bdata%20set%20telnet_en%3D1%20%3B%20bdata%20set%20ssh_en%3D1%20%3B%20bdata%20set%20uart_en%3D1%20%3B%20bdata%20commit%20%3B%20

Link returns with result {"code":0}

3- After this, open another browser tab use same token (used in the second step) with link;

http://192.168.31.1/cgi-bin/luci/;stok={token}/api/misystem/set_sys_time?timezone=%20%27%20%3b%20mtd%20erase%20crash%20%3b%20

Link returns with result {"code":0}

Restart the router from the interface.

After reboot check the result with the link;

http://192.168.31.1/cgi-bin/luci/api/xqsystem/bdata

{"ssh_en":"1"..."telnet_en":"1"..."uart_en":"1"...}

Enabling telnet on second device;

First you need to factory reset both devices. You need to start the process again by assuming the device to which the procedure will be applied as the first device, telnet enabled device as the second device.

After resetting the device to factory settings, power on both devices. Skip the initial setup screen only in first device, after connecting the first device's lan port to the other device's wan port with ethernet cable it will become netmode 4 in five seconds.

After the all process is complete, factory reset both devices.


Hi, first, you need to factory reset both devices. You need to start the process again by assuming the device to which the procedure will be applied as the first device, telnet enabled device as the second device.

After resetting the device to factory settings, power on both devices, skip the initial setup screen only in first device, after connecting the first device's lan port to the other device's wan port, it will become netmode 4 in five seconds.

After the all process is complete, factory reset both devices.







Hey, I got a repro and a fix :slight_smile:
with both my routers, after writing the crash partition and enabling telnet with your clever hack, my routers are in factory mode : no password needed for telnet and reset button does not do anything except showing a message on the console "BUTTON:reset ACTION:pressed".
without a way to use reset, I cannot but any other router in netmode 4

here is a fix:
deleting the crash partition from telnet with
`mtd erase crash
fixed it , I could then use the reset button to switch the other router to netmode 4, and perform the procedure.
I then needed the password calculated from the serial number to perform the upgrade this router.
Thanks again for the help, I hope my experience with help others as well if you want to include it in your instructions.