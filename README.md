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

    **macOS Users - Important Note:**
    Due to macOS security features (Gatekeeper), you might need to take an extra step the first time you run the application:
    1.  Right-click (or Control-click) the `main` application file.
    2.  Select "Open" from the menu.
    3.  You might see a warning saying the app is from an unidentified developer. Click "Open" again in this warning dialog.
    4.  If you don't see the "Open" option or the warning doesn't allow opening, go to **System Settings** > **Privacy & Security**.
    5.  Scroll down to the "Security" section.
    6.  You should see a message about the blocked application (`main`). Click the "**Open Anyway**" button next to it. You might need to enter your administrator password.
    7.  After doing this once, you should be able to open the application normally by double-clicking it in the future.

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

## Troubleshooting

*   **"401 Unauthorized" / "Please wait a few minutes" Error:** If you see an error message mentioning "401 Unauthorized" and "Please wait a few minutes", this means Instagram has temporarily limited requests from your account or session. This often happens when fetching large lists or after recent logins. Please wait some time (minutes to hours) and try running the application again. Using the saved session file might help reduce the frequency of this error.
*   **Invalid Session:** If the application asks for your password even though a session file exists, it means the saved session has expired or been invalidated by Instagram. Simply enter your password to log in again.
*   **Other Errors:** Ensure you have a stable internet connection. If you encounter other errors, especially after updating the application, consider deleting the existing `<username>.session` file and logging in fresh.

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