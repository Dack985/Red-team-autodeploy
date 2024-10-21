import os
import subprocess
import sys

repos = [
    {"url": "https://github.com/Dack985/Headshot.git", "script": "install.sh"},
    {"url": "https://github.com/Dack985/Mimic.git", "script": "mimic-v2"},
    {"url": "https://github.com/Dack985/Cerberus-shell.git", "script": "cerberus_setup.sh", "requires_dos2unix": True}
]

def install_dependencies():
    """Install necessary dependencies like git and dos2unix."""
    try:
        # Install git if not installed
        subprocess.run(["git", "--version"], check=True)
    except subprocess.CalledProcessError:
        print("Git is not installed. Installing git...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "git"], check=True)

    subprocess.run(["sudo", "apt", "install", "-y", "dos2unix"], check=True)

def clone_repo(repo_url, folder_name):
    """Clone the GitHub repository to a folder."""
    if not os.path.exists(folder_name):
        print(f"Cloning {repo_url}...")
        subprocess.run(["git", "clone", repo_url, folder_name], check=True)
    else:
        print(f"Repository {folder_name} already cloned. Pulling latest changes...")
        subprocess.run(["git", "-C", folder_name, "pull"], check=True)

def make_executable_and_run(script_path, requires_dos2unix=False):
    """Make the script executable and run it."""
    if requires_dos2unix:
        print(f"Converting {script_path} to Unix format using dos2unix...")
        subprocess.run(["sudo", "dos2unix", script_path], check=True)

    print(f"Making {script_path} executable...")
    subprocess.run(["sudo", "chmod", "+x", script_path], check=True)

    print(f"Running {script_path}...")
    result = subprocess.run([f"./{script_path}"], check=True, capture_output=True, text=True)
    
    print(f"Output of {script_path}:\n{result.stdout}")
    print(f"{script_path} execution completed.\n")

def main():
    install_dependencies()

    for repo in repos:
        folder_name = repo['url'].split('/')[-1].replace('.git', '')
        clone_repo(repo['url'], folder_name)
        
        script_path = os.path.join(folder_name, repo['script'])
        make_executable_and_run(script_path, repo.get("requires_dos2unix", False))

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
