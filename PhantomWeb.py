import os
import subprocess
import re

# Colors for text formatting
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

# Function to print colored text
def print_color(text, color):
    print(color + text + Color.RESET)

from termcolor import colored

name = "Rahul Kumar"
linkedin = "@rahul-kumar8176"

banner_text = '''
██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗██╗    ██╗███████╗██████╗ 
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║██║    ██║██╔════╝██╔══██╗
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║██║ █╗ ██║█████╗  ██████╔╝
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║██║███╗██║██╔══╝  ██╔══██╗
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║╚███╔███╔╝███████╗██████╔╝
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝ ╚══╝╚══╝ ╚══════╝╚═════╝                                                                              
'''
colored_line = colored("-" * 100, "green")
colored_banner = colored(banner_text, "green")
colored_name = colored(name, "yellow")
colored_linkedin = colored(linkedin, "blue")


print(colored_line)
print(colored_banner)
print("\t\t" + colored_name)
print("\t\t" + colored_linkedin)
print(colored_line)
print("\n")

url = input("Enter the URL: ")

# Create necessary directories if they don't exist
directories = [
    os.path.join(url, "recon"),
    os.path.join(url, "recon", "scans"),
    os.path.join(url, "recon", "httprobe"),
    os.path.join(url, "recon", "potential_takeovers"),
    os.path.join(url, "recon", "wayback"),
    os.path.join(url, "recon", "wayback", "params"),
    os.path.join(url, "recon", "wayback", "extensions")
]

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create empty files if they don't exist
files = [
    os.path.join(url, "recon", "httprobe", "alive.txt"),
    os.path.join(url, "recon", "final.txt")
]

for file in files:
    if not os.path.isfile(file):
        open(file, "w").close()

print_color("[+] Harvesting subdomains with assetfinder...", Color.YELLOW)
subprocess.run(["assetfinder", url], stdout=open(os.path.join(url, "recon", "assets.txt"), "w"))

subprocess.run(["cat", os.path.join(url, "recon", "assets.txt")], stdout=subprocess.PIPE)

subprocess.run(["grep", url], stdin=open(os.path.join(url, "recon", "assets.txt")), stdout=open(os.path.join(url, "recon", "final.txt"), "a"))

os.remove(os.path.join(url, "recon", "assets.txt"))

print_color("[+] Double checking for subdomains with amass...", Color.YELLOW)
subprocess.run(["amass", "enum", "-d", url], stdout=open(os.path.join(url, "recon", "f.txt"), "w"))
subprocess.run(["sort", "-u", os.path.join(url, "recon", "f.txt")], stdout=open(os.path.join(url, "recon", "final.txt"), "a"))
os.remove(os.path.join(url, "recon", "f.txt"))

print_color("[+] Removing Duplicate Entries From the Final.txt", Color.YELLOW)
final_file = os.path.join(url, "recon", "final.txt")

# Read the contents of the file
with open(final_file, "r") as file:
    lines = file.readlines()

# Remove duplicate entries
lines = list(set(lines))

# Write the unique entries back to the file
with open(final_file, "w") as file:
    file.writelines(lines)

print_color("[+] Probing for alive domains...", Color.YELLOW)
subprocess.run(["cat", os.path.join(url, "recon", "final.txt")], stdout=subprocess.PIPE)
subprocess.run(["httprobe", "-s", "-p", "https:443"], stdin=open(os.path.join(url, "recon", "final.txt"), "r"), stdout=open(os.path.join(url, "recon", "httprobe", "a.txt"), "w"))

subprocess.run(["sort", "-u", os.path.join(url, "recon", "httprobe", "a.txt")], stdout=open(os.path.join(url, "recon", "httprobe", "alive.txt"), "w"))

os.remove(os.path.join(url, "recon", "httprobe", "a.txt"))

print_color("[+] Checking for possible subdomain takeover...", Color.YELLOW)
potential_takeovers_file = os.path.join(url, "recon", "potential_takeovers", "potential_takeovers.txt")
if not os.path.isfile(potential_takeovers_file):
    open(potential_takeovers_file, "w").close()

subprocess.run(["subjack", "-w", os.path.join(url, "recon", "final.txt"), "-t", "100", "-timeout", "30", "-ssl",
                "-c", "/usr/share/subjack/fingerprints.json", "-v", "3", "-o", potential_takeovers_file])

print_color("[+] Scanning for open ports...", Color.YELLOW)

with open(os.path.join(url, "recon", "httprobe", "alive.txt"), "r") as file:
    urls = [line.strip() for line in file]

# Remove "http://" or "https://" and strip the URLs
stripped_urls = list(set([url.replace("http://", "").replace("https://", "").split(":")[0] for url in urls]))

# Perform Nmap scan for each unique URL
with open(os.path.join(url, "recon", "scans", "nmapscan.txt"), "w") as output_file:
    for stripped_url in stripped_urls:
        # Perform Nmap scan on the stripped URL with script scan and version detection
        print_color("[*] Running Nmap scan for the URL " + stripped_url, Color.GREEN)
        subprocess.run(["nmap", "-T4", "-sC", "-sV", "-oN", "-", stripped_url], stdout=output_file)

print_color("[+] Scraping wayback data...", Color.YELLOW)

# Read the content of the final.txt file
final_txt_path = os.path.join(url, "recon", "final.txt")
with open(final_txt_path, "rb") as f:
    final_txt_content = f.read()

# Pass the content as input to the waybackurls command
wayback_output_path = os.path.join(url, "recon", "wayback", "wayback_output.txt")
subprocess.run(["waybackurls"], input=final_txt_content, stdout=open(wayback_output_path, "w"))
lines = open(os.path.join(url, "recon", "wayback", "wayback_output.txt")).readlines()
unique_lines = list(set(lines))
with open(os.path.join(url, "recon", "wayback", "wayback_output.txt"), "w") as f:
    f.writelines(unique_lines)

print_color("[+] Pulling and compiling all possible params found in wayback data...", Color.YELLOW)
wayback_output_path = os.path.join(url, "recon", "wayback", "wayback_output.txt")
lines = open(wayback_output_path).readlines()

params = []
param_regex = r"\?([^=]+)="

for line in lines:
    matches = re.findall(param_regex, line)
    if matches:
        params.append(line.strip())

unique_params = list(set(params))

wayback_params_path = os.path.join(url, "recon", "wayback", "params", "wayback_params.txt")
with open(wayback_params_path, "w") as f:
    f.write("\n".join(unique_params))

print_color("[+] Unique Parameters Found:", Color.GREEN)
for line in unique_params:
    print_color(line, Color.GREEN)

print_color("[+] Pulling and compiling js/php/aspx/jsp/json files from wayback output...", Color.YELLOW)
extensions = {
    "js": "js",
    "html": "jsp",
    "json": "json",
    "php": "php",
    "aspx": "aspx",
    "png": "png"
}

for line in lines:
    ext = line.rsplit(".", 1)[-1].strip()
    if ext in extensions:
        ext_file = os.path.join(url, "recon", "wayback", "extensions", extensions[ext] + ".txt")
        with open(ext_file, "a") as f:
            f.write(line)

for ext in extensions.values():
    temp_file = os.path.join(url, "recon", "wayback", "extensions", ext + "1.txt")
    final_file = os.path.join(url, "recon", "wayback", "extensions", ext + ".txt")

    # Check if the temporary file exists before attempting to remove it
    if os.path.exists(temp_file):
        subprocess.run(["sort", "-u", temp_file], stdout=open(final_file, "w"))
        os.remove(temp_file)
