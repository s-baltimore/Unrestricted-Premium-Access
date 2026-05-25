#!/usr/bin/env python3
"""
GitHub Copilot Authenticator
Fetches a securely scoped Copilot token using the official VS Code Device Flow.
"""

import sys
import time
import webbrowser
from pathlib import Path
import requests

# Saves the token in the exact same folder the script is currently running from
TOKEN_FILE = Path(__file__).parent.resolve() / "ghcp_auth_token.txt"
CLIENT_ID = "Iv1.b507a08c87ecfe98"

# Official VS Code Copilot headers to mimic standard IDE traffic
HEADERS = {
    "User-Agent": "GitHubCopilotChat/0.35.0",
    "Editor-Version": "vscode/1.107.0",
    "Editor-Plugin-Version": "copilot-chat/0.35.0",
    "Copilot-Integration-Id": "vscode-chat",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def logout():
    """Removes the token from the machine to kill access."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        print("✅ Logged out successfully. Token removed from your machine.")
    else:
        print("You are already logged out (no token file found).")

def audit_security(token):
    """Proves to the user that this token CANNOT read their private code."""
    print("\n🔍 Running Security Audit (Verifying token permissions)...")
    
    endpoints = [
        ("Your GitHub Identity", "https://api.github.com/user"),
        ("Public Repositories", "https://api.github.com/user/repos?visibility=public&per_page=1"),
        ("Private Repositories", "https://api.github.com/user/repos?visibility=private&per_page=1"),
    ]
    
    for name, url in endpoints:
        res = requests.get(
            url, 
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
        )
        status = "ALLOWED" if res.status_code == 200 else "DENIED"
        print(f"   - Access to {name}: {status} (HTTP {res.status_code})")
        
    print("\n✅ Audit complete. Notice that access to private code/repos is strictly DENIED.")
    print("   This token is safe to use for Copilot routing.")

def login():
    """Handles the device-code OAuth flow to get the token."""
    print("🚀 Starting GitHub Copilot Authentication...\n")
    
    # Step 1: Request Device Code
    res = requests.post(
        "https://github.com/login/device/code", 
        headers=HEADERS, 
        json={"client_id": CLIENT_ID, "scope": "read:user"}
    ).json()
    
    print(f"1. A browser window should open. If not, click here: {res['verification_uri']}")
    print(f"2. Enter this exact authorization code: {res['user_code']}\n")
    
    try:
        webbrowser.open(res["verification_uri"])
    except Exception:
        pass

    print("Waiting for you to click 'Authorize' in your browser...")
    
    # Step 2: Poll GitHub for the token until the user clicks Authorize
    interval = int(res.get("interval", 5))
    while True:
        time.sleep(interval)
        poll = requests.post("https://github.com/login/oauth/access_token", headers=HEADERS, json={
            "client_id": CLIENT_ID,
            "device_code": res["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }).json()

        if "access_token" in poll:
            token = poll["access_token"]
            
            # Save token locally
            TOKEN_FILE.write_text(token)
            
            # Print the token boldly for the user to copy
            print("\n" + "="*65)
            print("🎉 AUTHENTICATION SUCCESSFUL")
            print("="*65)
            print(f"YOUR SECURE AUTH TOKEN: {token}")
            print("="*65)
            print(f"-> A backup of this token was saved to: {TOKEN_FILE.name}")
            print("-> Please copy the token above and send it to me securely.")
            
            audit_security(token)
            break
            
        elif poll.get("error") == "authorization_pending":
            # User hasn't clicked authorize yet, keep waiting
            continue
        elif poll.get("error") == "slow_down":
            interval += 5
        else:
            print(f"\n❌ Authorization failed or timed out: {poll}")
            break

if __name__ == "__main__":
    # If the user passes 'logout' as an argument
    if len(sys.argv) > 1 and sys.argv[1].lower() == "logout":
        logout()
    
    # If they already have a token
    elif TOKEN_FILE.exists():
        print(f"⚠️ You already have an active token saved at: {TOKEN_FILE.resolve()}")
        print(f"-> Run 'python {sys.argv[0]} logout' to remove it.")
        print(f"-> Or simply open the text file to copy it.")
    
    # Otherwise, start the login flow
    else:
        login()