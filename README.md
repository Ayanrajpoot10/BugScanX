
---

# 🌐 BugScanX - Advanced Network Toolkit for SNI Bughost Analysis


**BugScanX is a specialized toolkit by Ayan Rajpoot for identifying SNI bug hosts often used in free internet configurations. This script offers a range of utilities to analyze subdomains, scan IP addresses, retrieve DNS records, and more.**

--- 

## 🚀 Features
BugScanX provides robust tools to analyze networks and find SNI bug hosts:

1. **🖥️ Subdomains Scanner** - Scans subdomains to identify potential SNI bug hosts.
2. **📡 IP Addresses Scanner** - Scans IPs to locate SNI bug hosts on specific addresses.
3. **🌐 Subdomains Finder** - Finds active subdomains associated with a target domain.
4. **🔍 Domains Hosted on Same IP** - Lists domains hosted on the same IP as a target.
5. **💡 Host OSINT** - Performs OSINT checks for gathering open-source info on a host.
6. **🧰 TXT Toolkit** - Retrieves and analyzes TXT DNS records for security insights.
7. **🔓 Open Port Checker** - Scans open ports on a given IP or domain.
8. **📜 DNS Records** - Fetches A, MX, TXT, and other DNS records of a domain.
9. **📖 Help** - Provides usage instructions for each tool.
10. **⛔ Exit** - Cleanly exits the program.

---

## 🎨 UI Design

- **🌈 Colorful & Dynamic** – A bright, engaging interface that makes using the tool fun.  
- **😊 Emoji-Powered** – Emojis are integrated throughout, adding personality and making the experience more interactive.  
- **🚀 Modern & Minimalist** – Clean, intuitive design for a smooth, user-friendly experience.  
- **⚡ Fast & Responsive** – Instant feedback, no lag, and optimized for smooth navigation.

---

## 📥 Installation

### Requirements
Ensure Python 3.x is installed on your system.

### Automated Dependency Installation
BugScanX automatically installs all required modules and libraries on the first run, including:
- **requests**
- **colorama**
- **ipaddress**
- **pyfiglet**
- **socket**
- **ssl**
- **beautifulsoup4**
- **dnspython**
- **multithreading**

### Manual Installation (Optional)
If you prefer to install dependencies manually, run:
```bash
pip install requests colorama ipaddress pyfiglet socket ssl beautifulsoup4 dnspython multithreading
```

### Clone the Repository
```bash
git clone https://github.com/ayanrajpoot10/BugScanX.git
cd BugScanX
```

--- 


## 🛠️ Usage
Run the script:
```bash
python bugscanx.py
```

### Menu
Select a feature by entering its corresponding number:
```plaintext
 [1] 🖥️   Subdomains Scanner 
 [2] 📡  IP Addresses Scanner
 [3] 🌐  Subdomains Finder
 [4] 🔍  Domains Hosted on Same IP
 [5] 💡  Host OSINT 
 [6] 🧰  TXT Toolkit
 [7] 🔓  Open Port Checker
 [8] 📜  DNS Records
 [9] 📖  Help
 [10]⛔  Exit
```

## 📂 Example Usage
- **Subdomains Scanner**: Input a domain to enumerate subdomains and check for SNI bug host potential.
- **IP Addresses Scanner**: Input IPs to retrieve relevant information such as geolocation and hosting details.
- **DNS Records**: Get A, MX, TXT, and other DNS records for deeper domain insights.

## 📘 Documentation
Detailed documentation is available in the `docs/` directory.

## 🔒 License
This project is licensed under the MIT License.

## 🤝 Contributing
Contributions are welcome! Open an issue or submit a pull request.

## 📞 Support
For support, join our Telegram channel: [BugScanX](https://t.me/BugScanX)

---

Enjoy using **BugScanX** for efficient SNI bug host discovery and network analysis!
