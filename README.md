# Instagram Unfollow Checker

This script logs into your Instagram account, fetches your follower and following lists, and identifies accounts you follow that do not follow you back.

## Features

*   Logs into Instagram using your credentials.
*   Handles 2-Factor Authentication (2FA).
*   Saves login sessions to avoid repeated logins.
*   Fetches your followers and the accounts you follow (followees).
*   Compares the lists to find accounts you follow that don't follow you back.
*   Saves the list of these accounts (as profile URLs) to `not_following_back.txt`.

## Prerequisites

*   Python 3.x
*   An Instagram account (with username and password)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url> # Replace <repository-url> after creating the repo
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create and configure the `.env` file:**
    *   Rename or copy the `.env.example` file (if provided) to `.env`.
    *   Alternatively, create a new file named `.env` in the project root.
    *   Add your Instagram credentials:
        ```dotenv
        INSTAGRAM_USERNAME=your_instagram_username
        INSTAGRAM_PASSWORD=your_instagram_password
        ```
    **Important:** The `.env` file is included in `.gitignore` to prevent accidental commit of your credentials.

## Usage

Run the script from your terminal:

```bash
python main.py
```

*   The first time you run it, you might be prompted for your 2FA code.
*   After successful login, a session file (`<your_username>.session`) will be created to speed up future logins.
*   The script will fetch follower/following data (this might take some time depending on the number of accounts).
*   Finally, it will print the accounts that don't follow you back to the console and save their profile URLs in the `not_following_back.txt` file.

## Output File

The `not_following_back.txt` file will contain a list of Instagram profile URLs, one per line, for the accounts you follow that do not follow you back. You can often Alt+Click (or Cmd+Click on macOS) these URLs in modern text editors/terminals to open them directly in your browser.

## Disclaimer

Automating interactions with Instagram may be against their Terms of Service. Use this script responsibly and at your own risk. Frequent or aggressive use might lead to account restrictions. 