import os
import kaggle
import argparse
import subprocess
import json

def download_df(df: str, usr_name: str, key: str):
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Authenticate to Kaggle
    k = kaggle.KaggleApi({"username": usr_name, "key": key})
    k.authenticate()
    print("kaggle.com: authenticated")
    
    # Download and unzip the dataset
    k.dataset_download_cli(df, unzip=True, path="data")
    print(f"Dataset '{df}' downloaded and extracted to 'data' directory.")

def push_to_github(repo_name: str):
    # Clone the repository
    subprocess.run(["git", "clone", f"https://github.com/username/{repo_name}.git"], check=True)
    
    # Move downloaded files to repo
    subprocess.run(["mv", "data/*", repo_name], check=True)
    
    # Change to the repo directory
    os.chdir(repo_name)
    
    # Commit and push changes
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Add Kaggle dataset"], check=True)
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='Kaggle username', type=str, required=True)
    parser.add_argument('--key', help='Kaggle access key', type=str, required=True)
    parser.add_argument('--df', help='Dataset name from kaggle.com', type=str, required=True)
    parser.add_argument('--repo', help='GitHub repository name', type=str, required=True)
    args = parser.parse_args()

    # Store API token in kaggle.json
    api_token = {"username": args.username, "key": args.key}
    with open(os.path.expanduser('~/.kaggle/kaggle.json'), 'w') as file:
        json.dump(api_token, file)
    os.chmod(os.path.expanduser('~/.kaggle/kaggle.json'), 0o600)

    # Download the dataset
    download_df(args.df, args.username, args.key)
    
    # Push changes to GitHub
    push_to_github(args.repo)



