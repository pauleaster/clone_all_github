import os
import requests
import subprocess

# Need to execute the following commands in your terminal before running this:
# GITHUB_USERNAME=githubusername
# GITHUB_PARENT_DIR=/base/destination/dir/for/all/repos


try:
    # Read the username from the shell environment variable
    username = os.environ["GITHUB_USERNAME"]

    # Read the parent directory from the shell environment variable
    parent_dir = os.environ["GITHUB_PARENT_DIR"]
    print(f"username={username}")
    print(f"parent_dir={parent_dir}")
except:
    print("Failed to read the einvironemnt vars")
    exit(-1)
# Create the parent directory if it doesn't already exist
os.makedirs(parent_dir, exist_ok=True)

# Set the base URL for the GitHub REST API
base_url = "https://api.github.com"

def checkout_remote_branches(repo_dir):
    os.chdir(repo_dir)
    subprocess.run(["git", "fetch", "--all"])
    branches_output = subprocess.check_output(["git", "branch", "-r"])
    branches = branches_output.decode().split("\n")
    print(branches)
    for branch in branches:
        if branch.strip() != "origin/HEAD" and not branch.strip().startswith("origin/tags"):
            this_branch = branch.strip()
            if len(this_branch) > 0:
                print(f"git checkout --track {branch.strip()}")
                subprocess.run(["git", "checkout", "--track", branch.strip()])

# Construct the API endpoint to retrieve the list of repositories for the user
repos_endpoint = f"{base_url}/users/{username}/repos"

# Send a GET request to the API endpoint and parse the JSON response
response = requests.get(repos_endpoint)
repos = response.json()

# Clone or pull each repository locally using Git
for repo in repos:
    repo_dir = os.path.join(parent_dir, repo["name"])
    if os.path.isdir(repo_dir):
        print(f"Updating {repo['name']}...")
        os.chdir(repo_dir)
        subprocess.run(["git", "pull"])
        checkout_remote_branches(repo_dir)
    else:
        print(f"Cloning {repo['name']}...")
        subprocess.run(["git", "clone", repo["clone_url"], repo_dir])
        checkout_remote_branches(repo_dir)
