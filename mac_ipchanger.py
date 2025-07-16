#!/usr/bin/env python3

import subprocess
import random
import re
import os

# Banner
def show_banner():
    print("==========================================")
    print("     █▀▀ █░░█ █▀▄▀█ █▀▀ █▀▀█ █▀▀ █▀▀█")
    print("     █░░ █░░█ █░▀░█ █▀▀ █▄▄▀ █▀▀ █▄▄█")
    print("     ▀▀▀ ░▀▀▀ ▀░░░▀ ▀▀▀ ▀░▀▀ ▀▀▀ ▀░░▀")
    print("        MAC & IP Changer Script")
    print("          MADE BY ELITEHACKER")
    print("==========================================\n")

# Detect network interfaces
def get_interfaces():
    result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    output = result.stdout.decode()
    interfaces = re.findall(r'^([a-zA-Z0-9]+): flags', output, re.MULTILINE)
    return [iface for iface in interfaces if iface != 'lo']

# Generate random MAC address
def generate_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0x00, 0xFF) for _ in range(5))

# Run a shell command
def run_cmd(cmd):
    subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# Get current IP of interface
def get_ip(interface):
    result = subprocess.run(['ip', '-o', '-4', 'addr', 'show', interface], stdout=subprocess.PIPE)
    match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout.decode())
    return match.group(1) if match else "No IP"

# Main function
def main():
    show_banner()

    interfaces = get_interfaces()
    if not interfaces:
        print("[!] No network interfaces found.")
        return

    print("Available Interfaces:")
    for idx, iface in enumerate(interfaces, 1):
        print(f"{idx}. {iface}")

    try:
        choice = int(input("Select interface number to spoof MAC: "))
        if choice < 1 or choice > len(interfaces):
            raise ValueError
    except ValueError:
        print("[!] Invalid selection.")
        return

    iface = interfaces[choice - 1]
    new_mac = generate_mac()

    print(f"\n[*] Changing MAC address of {iface} to {new_mac}")
    run_cmd(f"sudo ifconfig {iface} down")
    run_cmd(f"sudo ifconfig {iface} hw ether {new_mac}")
    run_cmd(f"sudo ifconfig {iface} up")

    print("[*] Releasing and requesting new IP...")
    run_cmd(f"sudo dhclient -r {iface}")
    run_cmd(f"sudo dhclient {iface}")

    new_ip = get_ip(iface)
    print("\n==========================================")
    print(f"[+] Interface      : {iface}")
    print(f"[+] New MAC Address: {new_mac}")
    print(f"[+] New IP Address : {new_ip}")
    print("==========================================")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[!] Please run this script as root (sudo).")
    else:
        main()
