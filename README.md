# Instagram Unfollow Checker

This GUI application logs into your Instagram account, fetches your follower and following lists, and identifies accounts you follow that do not follow you back.

## Features

*   **Modern User Interface:** Easy-to-use graphical interface.
*   Logs into Instagram using your credentials (entered in the app).
*   Handles 2-Factor Authentication (2FA) via a pop-up prompt.
*   Saves login sessions (`<username>.session` file) to avoid repeated logins.
*   Handles expired/invalid sessions by prompting for password.
*   Fetches your followers and the accounts you follow (followees).
*   Displays status updates and results directly in the app window.
*   Saves the list of non-followers (as profile URLs) to `not_following_back.txt`.

## Prerequisites

*   An Instagram account.
*   (Optional) Python 3.x if running from source.

## Installation & Setup

There are two ways to use this tool:

1.  **Download the Application (Recommended for most users):**
    *   Go to the [**Releases page**](https://github.com/agopalareddy/instagram-unfollow-checker/releases) of this repository.
    *   Find the latest release.
    *   Under "Assets", download the appropriate `.zip` file for your operating system (Windows, macOS, or Linux).
    *   Unzip the downloaded file.
    *   Run the executable file found inside the unzipped folder (e.g., `main.exe` on Windows, `main` on macOS/Linux).
    *   No further installation (like Python or dependencies) is needed.

2.  **Run from Source (For developers):**
    *   **Clone the repository:**
        ```bash
        git clone https://github.com/agopalareddy/instagram-unfollow-checker.git
        cd instagram-unfollow-checker
        ```
    *   **Install dependencies:**
        ```bash
        pip install -r requirements.txt
        ```

## Usage

1.  **If using the Downloaded Application:**
    *   Double-click the executable file (e.g., `main.exe` on Windows, `main` on macOS/Linux) that you extracted from the downloaded `.zip` file.

2.  **If running from Source:**
    *   Run the script from your terminal:
        ```bash
        python main.py
        ```

**Using the Application:**

1.  Enter your Instagram **Username**.
2.  The application will check if a saved session file exists for that username.
    *   If a session **is found**, the password field will be disabled. Click **"Find Non-Followers (Use Session)"**.
    *   If a session **is not found**, enter your **Password** and click **"Find Non-Followers"**.
3.  The application will display status messages in the text box below.
4.  If you are using a session and it has **expired or is invalid**, you will be prompted to enter your password and click the button again.
5.  If **2-Factor Authentication** is required, a pop-up window will appear asking for your code.
6.  Once the process is complete, the accounts that don't follow you back will be listed in the status box.
7.  The full list of profile URLs for non-followers will also be saved to `not_following_back.txt` in the same directory as the application.

## Output File

The `not_following_back.txt` file will be created or updated in the same directory where you run the application. It contains a list of Instagram profile URLs, one per line, for the accounts you follow that do not follow you back.

## Data Safety and Privacy

*   **Credentials:** Your Instagram username and password are used *only* to log in to Instagram via the `instaloader` library. They are required by Instagram for accessing your follower/following lists.
*   **Storage:**
    *   Login credentials (username/password) are **never** stored permanently by this application.
    *   A **session file** (`<your_username>.session`) is saved locally on your device after a successful login. This file contains session cookies provided by Instagram, allowing the application to resume your session later without needing your password again. It helps avoid repeated logins and potential security flags from Instagram. This file is stored only on your computer.
    *   The list of non-followers is saved to `not_following_back.txt` locally on your device.
*   **Transmission:** Your credentials and session data are sent *only* to Instagram's servers as part of the standard login and data fetching process managed by the `instaloader` library. No credential or personal data is sent to any other third party or server.
*   **Privacy:** All operations occur locally on your machine. Your follower lists, following lists, and the resulting list of non-followers remain private on your computer.

## Disclaimer

Automating interactions with Instagram may be against their Terms of Service. Use this script responsibly and at your own risk. Frequent or aggressive use might lead to account restrictions. 