# Instagram Unfollow Checker

This script logs into your Instagram account, fetches your follower and following lists, and identifies accounts you follow that do not follow you back.

## Features

*   Logs into Instagram using your credentials (prompts for username/password).
*   Handles 2-Factor Authentication (2FA).
*   Saves login sessions to avoid repeated logins.
*   Fetches your followers and the accounts you follow (followees).
*   Compares the lists to find accounts you follow that don't follow you back.
*   Saves the list of these accounts (as profile URLs) to `not_following_back.txt`.

## Prerequisites

*   Python 3.x (if running from source)
*   An Instagram account

## Installation & Setup

There are two ways to use this tool:

1.  **Download the Executable (Recommended for most users):**
    *   Go to the [Releases page](https://github.com/agopalareddy/instagram-unfollow-checker/releases/tag/v1.1.0) of this repository.
    *   Download the `main.exe` file (or the appropriate executable for your OS if others are provided).
    *   Place the downloaded executable in a folder of your choice.
    *   No further installation (like Python or dependencies) is needed.

2.  **Run from Source (For developers or if the executable doesn't work):**
    *   **Clone the repository:**
        ```bash
        git clone <repository-url> # Replace <repository-url>
        cd <repository-directory>
        ```
    *   **Install dependencies:**
        ```bash
        pip install -r requirements.txt
        ```

## Usage

1.  **If using the Executable:**
    *   Double-click `main.exe` (or run it from your terminal/command prompt).

2.  **If running from Source:**
    *   Run the script from your terminal:
        ```bash
        python main.py
        ```

**When you run the application:**

*   You will be prompted to enter your Instagram username and password directly in the terminal.
    *   **Note:** Your password input will be hidden for security.
*   The first time you log in successfully, you might be asked for a 2-Factor Authentication (2FA) code if you have it enabled.
*   After a successful login, a session file (`<your_username>.session`) will be created in the same directory as the application. This helps speed up future logins.
*   The script will fetch follower/following data (this might take some time).
*   Finally, it will print the accounts that don't follow you back to the console and save their profile URLs in the `not_following_back.txt` file (also created in the same directory).

## Output File

The `not_following_back.txt` file will contain a list of Instagram profile URLs, one per line, for the accounts you follow that do not follow you back. You can often Alt+Click (or Cmd+Click on macOS) these URLs in modern text editors/terminals to open them directly in your browser.

## Disclaimer

Automating interactions with Instagram may be against their Terms of Service. Use this script responsibly and at your own risk. Frequent or aggressive use might lead to account restrictions. 