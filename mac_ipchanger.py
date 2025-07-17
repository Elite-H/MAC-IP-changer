#!/usr/bin/env python3

import subprocess
import random
import re
import os
import time
import sys
from datetime import datetime

# Colors
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

# Global variable to store original MAC addresses
original_macs = {}

# Banner
def show_banner():
    print(f"{RED}=========================================={RESET}")
    print(f"{RED}     █▀▀ █░░█ █▀▄▀█ █▀▀ █▀▀█ █▀▀ █▀▀█")
    print(f"     █░░ █░░█ █░▀░█ █▀▀ █▄▄▀ █▀▀ █▄▄█")
    print(f"     ▀▀▀ ░▀▀▀ ▀░░░▀ ▀▀▀ ▀░▀▀ ▀▀▀ ▀░░▀")
    print(f"        {CYAN}MAC & IP Changer Script{RESET}")
    print(f"          {RED}MADE BY ELITEHACKER{RESET}")
    print(f"{RED}=========================================={RESET}\n")

# Detect network interfaces
def get_interfaces():
    try:
        result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output = result.stdout.decode()
        interfaces = re.findall(r'^([a-zA-Z0-9]+): flags', output, re.MULTILINE)
        return [iface for iface in interfaces if iface != 'lo']
    except:
        return []

# Generate random MAC address
def generate_mac(vendor=None):
    if vendor == "cisco":
        return "00:01:42:%02x:%02x:%02x" % (random.randint(0x00, 0xFF), random.randint(0x00, 0xFF), random.randint(0x00, 0xFF))
    elif vendor == "apple":
        return "00:03:93:%02x:%02x:%02x" % (random.randint(0x00, 0xFF), random.randint(0x00, 0xFF), random.randint(0x00, 0xFF))
    elif vendor == "samsung":
        return "00:12:47:%02x:%02x:%02x" % (random.randint(0x00, 0xFF), random.randint(0x00, 0xFF), random.randint(0x00, 0xFF))
    else:
        return "02:%02x:%02x:%02x:%02x:%02x" % (random.randint(0x00, 0xFF), random.randint(0x00, 0xFF), random.randint(0x00, 0xFF), random.randint(0x00, 0xFF), random.randint(0x00, 0xFF))

# Run a shell command with error handling
def run_cmd(cmd, show_output=False):
    try:
        if show_output:
            subprocess.run(cmd, shell=True, check=True)
        else:
            subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Get current MAC of interface
def get_mac(interface):
    try:
        result = subprocess.run(['ifconfig', interface], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        match = re.search(r'ether ([0-9a-fA-F:]{17})', output)
        return match.group(1) if match else "Unknown"
    except:
        return "Unknown"

# Store original MAC address
def store_original_mac(interface):
    if interface not in original_macs:
        original_macs[interface] = get_mac(interface)

# Get current IP of interface
def get_ip(interface):
    try:
        result = subprocess.run(['ip', '-o', '-4', 'addr', 'show', interface], stdout=subprocess.PIPE)
        match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout.decode())
        return match.group(1) if match else "No IP"
    except:
        return "No IP"

# Get network info
def get_network_info(interface):
    info = {
        'mac': get_mac(interface),
        'ip': get_ip(interface),
        'gateway': get_gateway(),
        'dns': get_dns()
    }
    return info

# Get default gateway
def get_gateway():
    try:
        result = subprocess.run(['ip', 'route', 'show', 'default'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        match = re.search(r'via (\d+\.\d+\.\d+\.\d+)', output)
        return match.group(1) if match else "Unknown"
    except:
        return "Unknown"

# Get DNS servers
def get_dns():
    try:
        with open('/etc/resolv.conf', 'r') as f:
            dns_servers = re.findall(r'nameserver\s+(\d+\.\d+\.\d+\.\d+)', f.read())
            return dns_servers if dns_servers else ["Unknown"]
    except:
        return ["Unknown"]

# Change MAC address
def change_mac(interface, new_mac):
    print(f"\n{YELLOW}[*]{RESET} Changing MAC address of {GREEN}{interface}{RESET} to {GREEN}{new_mac}{RESET}")
    
    if not run_cmd(f"sudo ifconfig {interface} down"):
        print(f"{RED}[!]{RESET} Failed to bring interface down")
        return False
    
    if not run_cmd(f"sudo ifconfig {interface} hw ether {new_mac}"):
        print(f"{RED}[!]{RESET} Failed to change MAC address")
        run_cmd(f"sudo ifconfig {interface} up")
        return False
    
    if not run_cmd(f"sudo ifconfig {interface} up"):
        print(f"{RED}[!]{RESET} Failed to bring interface up")
        return False
    
    # Verify MAC change
    current_mac = get_mac(interface)
    if current_mac.lower() == new_mac.lower():
        print(f"{GREEN}[+]{RESET} MAC address successfully changed to {GREEN}{new_mac}{RESET}")
        return True
    else:
        print(f"{RED}[!]{RESET} MAC address change failed (Current: {current_mac})")
        return False

# Change IP address
def change_ip(interface):
    print(f"\n{YELLOW}[*]{RESET} Releasing and requesting new IP for {GREEN}{interface}{RESET}")
    
    if not run_cmd(f"sudo dhclient -r {interface}"):
        print(f"{RED}[!]{RESET} Failed to release IP address")
        return False
    
    if not run_cmd(f"sudo dhclient {interface}"):
        print(f"{RED}[!]{RESET} Failed to obtain new IP address")
        return False
    
    new_ip = get_ip(interface)
    if new_ip != "No IP":
        print(f"{GREEN}[+]{RESET} New IP address: {GREEN}{new_ip}{RESET}")
        return True
    else:
        print(f"{RED}[!]{RESET} Failed to obtain new IP address")
        return False

# Reset MAC to original
def reset_mac(interface):
    if interface in original_macs:
        original_mac = original_macs[interface]
        print(f"\n{YELLOW}[*]{RESET} Resetting MAC address of {GREEN}{interface}{RESET} to original: {GREEN}{original_mac}{RESET}")
        
        if not run_cmd(f"sudo ifconfig {interface} down"):
            print(f"{RED}[!]{RESET} Failed to bring interface down")
            return False
        
        if not run_cmd(f"sudo ifconfig {interface} hw ether {original_mac}"):
            print(f"{RED}[!]{RESET} Failed to reset MAC address")
            run_cmd(f"sudo ifconfig {interface} up")
            return False
        
        if not run_cmd(f"sudo ifconfig {interface} up"):
            print(f"{RED}[!]{RESET} Failed to bring interface up")
            return False
        
        # Verify MAC reset
        current_mac = get_mac(interface)
        if current_mac.lower() == original_mac.lower():
            print(f"{GREEN}[+]{RESET} MAC address successfully reset to original: {GREEN}{original_mac}{RESET}")
            return True
        else:
            print(f"{RED}[!]{RESET} MAC address reset failed (Current: {current_mac})")
            return False
    else:
        print(f"{RED}[!]{RESET} No original MAC address stored for {interface}")
        return False

# Reset IP address
def reset_ip(interface):
    print(f"\n{YELLOW}[*]{RESET} Resetting IP address for {GREEN}{interface}{RESET}")
    return change_ip(interface)  # Same as getting a new IP

# Spoof MAC and IP
def spoof_network(interface, vendor=None):
    store_original_mac(interface)
    new_mac = generate_mac(vendor)
    if not change_mac(interface, new_mac):
        return False
    
    time.sleep(2)  # Wait for MAC change to take effect
    
    if not change_ip(interface):
        return False
    
    return True

# Reset network to original
def reset_network(interface):
    if not reset_mac(interface):
        return False
    
    time.sleep(2)  # Wait for MAC reset to take effect
    
    if not reset_ip(interface):
        return False
    
    return True

# Print network information
def print_network_info(info):
    print(f"\n{CYAN}=== Network Information ==={RESET}")
    print(f"{YELLOW}MAC Address:{RESET} {info['mac']}")
    print(f"{YELLOW}IP Address:{RESET} {info['ip']}")
    print(f"{YELLOW}Gateway:{RESET} {info['gateway']}")
    print(f"{YELLOW}DNS Servers:{RESET} {', '.join(info['dns'])}")
    print(f"{CYAN}=========================={RESET}")

# Main menu
def main_menu():
    print(f"\n{CYAN}Main Menu:{RESET}")
    print(f"{YELLOW}1.{RESET} Spoof MAC & IP Address")
    print(f"{YELLOW}2.{RESET} Reset to Original MAC & IP")
    print(f"{YELLOW}3.{RESET} Exit")
    
    try:
        choice = input(f"{YELLOW}[?]{RESET} Select an option [1-3]: ")
        return int(choice)
    except ValueError:
        return -1

# Main function
def main():
    show_banner()

    interfaces = get_interfaces()
    if not interfaces:
        print(f"{RED}[!]{RESET} No network interfaces found.")
        return

    print(f"{CYAN}Available Interfaces:{RESET}")
    for idx, iface in enumerate(interfaces, 1):
        current_ip = get_ip(iface)
        print(f"{YELLOW}{idx}.{RESET} {GREEN}{iface}{RESET} - {current_ip}")

    try:
        choice = int(input(f"\n{YELLOW}[?]{RESET} Select interface number: "))
        if choice < 1 or choice > len(interfaces):
            raise ValueError
    except ValueError:
        print(f"{RED}[!]{RESET} Invalid selection.")
        return

    iface = interfaces[choice - 1]
    
    while True:
        option = main_menu()
        
        if option == 1:  # Spoof
            print(f"\n{YELLOW}MAC Vendor Options:{RESET}")
            print(f"{YELLOW}1.{RESET} Random (default)")
            print(f"{YELLOW}2.{RESET} Cisco")
            print(f"{YELLOW}3.{RESET} Apple")
            print(f"{YELLOW}4.{RESET} Samsung")
            
            try:
                vendor_choice = input(f"{YELLOW}[?]{RESET} Select MAC vendor [1-4] (default: 1): ") or "1"
                vendor_choice = int(vendor_choice)
                if vendor_choice == 1:
                    vendor = None
                elif vendor_choice == 2:
                    vendor = "cisco"
                elif vendor_choice == 3:
                    vendor = "apple"
                elif vendor_choice == 4:
                    vendor = "samsung"
                else:
                    raise ValueError
            except ValueError:
                print(f"{RED}[!]{RESET} Invalid selection. Using random MAC.")
                vendor = None

            # Show current network info
            current_info = get_network_info(iface)
            print_network_info(current_info)

            # Confirm action
            confirm = input(f"\n{YELLOW}[?]{RESET} Continue with spoofing? [y/N]: ").lower()
            if confirm != 'y':
                print(f"{YELLOW}[*]{RESET} Operation cancelled.")
                continue

            # Perform spoofing
            if spoof_network(iface, vendor):
                # Show new network info
                new_info = get_network_info(iface)
                print_network_info(new_info)
                
                # Save log
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open('mac_ip_changer.log', 'a') as f:
                    f.write(f"[{timestamp}] SPOOF - Interface: {iface}\n")
                    f.write(f"  Old MAC: {current_info['mac']} -> New MAC: {new_info['mac']}\n")
                    f.write(f"  Old IP: {current_info['ip']} -> New IP: {new_info['ip']}\n\n")
                
                print(f"\n{GREEN}[+]{RESET} Network spoofing completed successfully!")
            else:
                print(f"\n{RED}[!]{RESET} Network spoofing failed.")
        
        elif option == 2:  # Reset
            # Show current network info
            current_info = get_network_info(iface)
            print_network_info(current_info)

            # Confirm action
            confirm = input(f"\n{YELLOW}[?]{RESET} Continue with reset? [y/N]: ").lower()
            if confirm != 'y':
                print(f"{YELLOW}[*]{RESET} Operation cancelled.")
                continue

            # Perform reset
            if reset_network(iface):
                # Show new network info
                new_info = get_network_info(iface)
                print_network_info(new_info)
                
                # Save log
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open('mac_ip_changer.log', 'a') as f:
                    f.write(f"[{timestamp}] RESET - Interface: {iface}\n")
                    f.write(f"  Changed MAC: {current_info['mac']} -> Original MAC: {new_info['mac']}\n")
                    f.write(f"  Current IP: {current_info['ip']} -> New IP: {new_info['ip']}\n\n")
                
                print(f"\n{GREEN}[+]{RESET} Network reset completed successfully!")
            else:
                print(f"\n{RED}[!]{RESET} Network reset failed.")
        
        elif option == 3:  # Exit
            print(f"\n{YELLOW}[*]{RESET} Exiting...")
            break
        
        else:
            print(f"{RED}[!]{RESET} Invalid option selected.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(f"{RED}[!]{RESET} Please run this script as root (sudo).")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!]{RESET} Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}[!]{RESET} An error occurred: {str(e)}")
        sys.exit(1)
