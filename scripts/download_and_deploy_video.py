import sys
import os
import re
import urllib.request
import subprocess

def download_file(url, output_path):
    print(f"Resolving URL: {url}")
    
    # Handle Dropbox links
    if "dropbox.com" in url and "dl=0" in url:
        url = url.replace("dl=0", "dl=1")
    
    # Handle Google Drive links
    if "drive.google.com" in url:
        # Extract file ID
        match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
        if not match:
            match = re.search(r"id=([a-zA-Z0-9_-]+)", url)
        
        if match:
            file_id = match.group(1)
            url = f"https://docs.google.com/uc?export=download&id={file_id}"
            print(f"Extracted Google Drive File ID: {file_id}. Rewrote to: {url}")
    
    # Download using curl which handles redirects and user-agents better
    print(f"Downloading to {output_path}...")
    try:
        cmd = ["curl", "-L", "-o", output_path, url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Download completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading with curl: {e.stderr}")
        return False

def deploy_video(video_path):
    if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
        print("Error: Downloaded video file is empty or missing.")
        return False
    
    print("Deploying video to blog/media/vision-main.mp4...")
    target_video = "blog/media/vision-main.mp4"
    os.makedirs(os.path.dirname(target_video), exist_ok=True)
    
    # Move or copy downloaded video
    if os.path.exists(target_video):
        os.remove(target_video)
    os.rename(video_path, target_video)
    
    # Update index.html to make the Sovereign Security tab use this newly uploaded video
    index_path = "index.html"
    if os.path.exists(index_path):
        print("Updating index.html with new video source...")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace the first video source in index.html (the active one)
        new_content = content.replace(
            '<source src="blog/media/enterprise-security-vault.mp4" type="video/mp4">',
            '<source src="blog/media/vision-main.mp4" type="video/mp4">'
        )
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("index.html updated successfully.")
    
    # Take screenshot of the new setup
    print("Running screenshot verification...")
    try:
        subprocess.run(["node", "/tmp/screenshot.js"], check=True)
        print("Verification screenshot updated.")
    except Exception as e:
        print(f"Screenshot verification failed: {e}")
        
    # Push changes to git
    print("Pushing updates to GitHub...")
    try:
        subprocess.run(["git", "add", "index.html", "blog/media/vision-main.mp4", "images/video-showroom-proof.png"], check=True)
        subprocess.run(["git", "commit", "-m", "feat: deploy custom client-uploaded showroom video"], check=True)
        subprocess.run(["git", "push", "origin", "master"], check=True)
        print("Git push master succeeded. Deployed live!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 download_and_deploy_video.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    temp_path = "/tmp/downloaded_video.mp4"
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    if download_file(url, temp_path):
        if deploy_video(temp_path):
            print("DEPLOYMENT COMPLETE!")
        else:
            print("Deployment failed during video processing/git push.")
            sys.exit(1)
    else:
        print("Download failed.")
        sys.exit(1)
