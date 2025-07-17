# 🚀 MAC & IP Changer Tool
**A powerful Python script to spoof or reset MAC and IP addresses on Linux systems**

## 📋 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## ✨ Features

### MAC Address Spoofing
✅ Generate random MAC addresses  
✅ Vendor-specific MACs (Cisco/Apple/Samsung)  
✅ Store original MAC for easy reset  
✅ Visual verification of changes  

### IP Address Management
✅ Release current IP  
✅ Request new DHCP lease  
✅ Automatic IP renewal after MAC change  

### Reset Functionality
🔙 Restore original MAC address  
🔄 Renew IP address  
📋 View before/after network configurations  

### Extras
🎨 Color-coded terminal interface  
📝 Automatic operation logging  
🛡️ Root permission verification  

---

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/mac-ip-changer.git
   cd mac-ip-changer
   chmod +x mac_ip_changer.py
   sudo ./mac_ip_changer.py



⚠️ Troubleshooting

Issue	Solution
"No network interfaces found"	Check if ifconfig is installed (sudo apt install net-tools)
MAC change doesn't persist	Disable NetworkManager: sudo systemctl stop NetworkManager
Script won't run	Ensure Python 3 is installed (python3 --version)
Permission denied	Always run with sudo

🔐 Important Notes
❗ Legal Disclaimer
This tool is for:

Educational purposes

Privacy protection

Security research

Never use this tool on networks without explicit permission.

📜 License
MIT License - See LICENSE file for details

👨💻 Author
ELITEHACKER
"With great power comes great responsibility"
