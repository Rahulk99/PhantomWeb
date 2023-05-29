import os
import subprocess
import platform
import sys

# Colors for text formatting
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

# Function to print colored text
def print_color(text, color):
    print(color + text + Color.RESET)

# List of required tools
tools = [
    "assetfinder",
    "amass",
    "httprobe",
    "subjack",
    "nmap"
]

# Install the tools
def install_tools():
    for tool in tools:
        print_color(f"Installing {tool}...", Color.YELLOW)
        command = ""
        if platform.system() == "Windows":
            command = f"choco install {tool} -y"
        elif platform.system() == "Linux":
            command = f"sudo apt-get install {tool} -y"
        elif platform.system() == "Darwin":
            command = f"brew install {tool}"
        else:
            print_color(f"Unsupported operating system: {platform.system()}", Color.RED)
            sys.exit(1)

        try:
            subprocess.run(command, shell=True, check=True)
            print_color(f"{tool} installed successfully", Color.GREEN)
        except subprocess.CalledProcessError:
            print_color(f"Failed to install {tool}", Color.RED)

    # Install waybackurls using go install
    print_color("Installing waybackurls...", Color.YELLOW)
    try:
        subprocess.run("go install github.com/tomnomnom/waybackurls@latest", shell=True, check=True)
        print_color("waybackurls installed successfully", Color.GREEN)
    except subprocess.CalledProcessError:
        print_color("Failed to install waybackurls", Color.RED)

# Configure the PATH variable
def configure_path():
    path_var = os.getenv("PATH", "")
    for tool in tools:
        tool_path = subprocess.check_output(f"which {tool}", shell=True, universal_newlines=True).strip()
        if tool_path:
            path_var += ":" + os.path.dirname(tool_path)
    
    # Add Go binaries to PATH
    go_path = os.getenv("GOPATH", "")
    if go_path:
        go_bin_path = os.path.join(go_path, "bin")
        if os.path.isdir(go_bin_path):
            path_var += ":" + go_bin_path

    # Update the PATH variable
    if platform.system() == "Windows":
        try:
            subprocess.run(f'setx PATH "{path_var}"', shell=True, check=True)
            print_color("PATH variable updated successfully", Color.GREEN)
        except subprocess.CalledProcessError:
            print_color("Failed to update PATH variable", Color.RED)
    else:
        profile_file = ""
        if platform.system() == "Linux":
            profile_file = "~/.bashrc"
        elif platform.system() == "Darwin":
            profile_file = "~/.bash_profile"
        
        with open(os.path.expanduser(profile_file), "a") as file:
            file.write(f'\nexport PATH="{path_var}"\n')

        print_color("PATH variable updated successfully", Color.GREEN)

# Display a message indicating manual installation may be required
print_color("**************************************************", Color.GREEN)
print_color("************* TOOLS INSTALLATION SCRIPT **********", Color.GREEN)
print_color("**************************************************", Color.GREEN)
print_color("\nThis script is provided as a convenience, but it may not work on all systems or environments.", Color.YELLOW)
print_color("If the installation fails or you encounter any issues, please manually install the following tools:", Color.YELLOW)
for tool in tools:
    print(f"- {tool}")
print("\nManual installation instructions can be found in the documentation.\n")

# Install the tools
install_tools()

# Configure the PATH variable
configure_path()

print_color("Installation and configuration complete.", Color.GREEN)
