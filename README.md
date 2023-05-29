# PhantomWeb
This script is designed to automate the reconnaissance process for a target website and perform various security-related checks. It helps in identifying subdomains, probing for alive domains, checking for possible subdomain takeover, scanning for open ports, and scraping Wayback Machine data. The script is written in Python.

## Features
* Harvest subdomains using assetfinder and amass.
* Probe for alive domains using httprobe.
* Check for possible subdomain takeover using subjack.
* Scan for open ports using nmap.
* Scrape Wayback Machine data using waybackurls.
* Pull and compile parameters found in Wayback data.
* Pull and compile specific file types (e.g., .js, .php, .aspx) from Wayback data.
* Generate organized output files for further analysis.
## Prerequisites
Before using this script, ensure that you have the following prerequisites installed:

* assetfinder
* amass
* httprobe
* subjack
* nmap
* waybackurls
Make sure these tools are properly set up and added to your system's PATH.

Usage
1. Clone this repository:
```
git clone https://github.com/your_username/git-recon-script.git
```
2. Navigate to the cloned directory:

```
cd git-recon-script
```
3. Run the script:

```
python git_recon_script.py
```
4. Follow the prompts and provide the necessary input.

5. The script will perform the specified recon steps and generate output files in the recon directory.

## Disclaimer
This script is provided for educational and ethical purposes only. The use of this script against any target without proper authorization may be illegal. The author is not responsible for any misuse or damage caused by this script.

## Author
* Rahul Kumar
* LinkedIn: @rahul-kumar8176
Please note that this script is provided as-is without any warranty. Use it at your own risk.
