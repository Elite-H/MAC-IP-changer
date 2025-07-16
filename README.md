==============================
   MAC/IP CHANGER TOOL
        MADE BY ELITEHACKER
==============================

This tool allows you to:
✅ Change the MAC address of a selected network interface
✅ Request a new IP address via DHCP (dhclient)

---------------
 Requirements:
---------------
- Python 3
- Linux OS
- `ifconfig` and `dhclient` must be installed
- Root access (run with sudo)

----------------------
 How to Use the Tool:
----------------------

1. Open your terminal.

2. Make the script executable:
   chmod +x elite_mac_ip_changer.py

3. Run the script as root:
   sudo ./elite_mac_ip_changer.py

4. The script will:
   - Show all available interfaces
   - Ask which one you want to change
   - Generate and assign a new random MAC
   - Request a new IP using dhclient

---------------------
 Sample Output:
---------------------
Available Interfaces:
1. wlan0
2. eth0

Select interface number to spoof MAC: 1

[*] Changing MAC address of wlan0 to 02:6A:91:3F:44:2D
[*] Releasing and requesting new IP...

[+] Interface      : wlan0
[+] New MAC Address: 02:6A:91:3F:44:2D
[+] New IP Address : 192.168.1.115

-------------------------
  Author: ELITEHACKER 😎
-------------------------

