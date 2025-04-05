import instaloader
import os
from dotenv import load_dotenv

def main():
    """
    Logs into Instagram, fetches follower and following lists,
    identifies users the authenticated user follows but who don't follow back,
    and saves their profile URLs to a text file.
    Handles session persistence and 2FA.
    """
    load_dotenv()

    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print("Error: INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD must be set in the .env file.")
        return

    L = instaloader.Instaloader()

    session_file = f"{username}.session"

    try:
        if os.path.exists(session_file):
            L.load_session_from_file(username, session_file)
            print(f"Loaded session for {username}")
            L.test_login()
            print("Session is valid.")
        else:
            raise FileNotFoundError("Session file not found, attempting login.")

    except (FileNotFoundError, instaloader.exceptions.BadCredentialsException, instaloader.exceptions.TwoFactorAuthRequiredException) as e:
        print(f"Could not load session or session invalid: {e}. Logging in...")
        try:
            L.login(username, password)
            print(f"Login successful for {username}.")
            L.save_session_to_file(session_file)
            print(f"Session saved to {session_file}")
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            two_factor_code = input("Enter the 2FA code: ")
            try:
                L.two_factor_login(two_factor_code)
                print(f"2FA Login successful for {username}.")
                L.save_session_to_file(session_file)
                print(f"Session saved to {session_file}")
            except instaloader.exceptions.BadCredentialsException:
                print("Error: Invalid 2FA code or other login issue.")
                return
            except Exception as e_2fa:
                 print(f"An error occurred during 2FA login: {e_2fa}")
                 return
        except instaloader.exceptions.BadCredentialsException:
            print("Error: Invalid username or password.")
            return
        except Exception as e_login:
            print(f"An error occurred during login: {e_login}")
            return

    try:
        profile = instaloader.Profile.from_username(L.context, username)

        print("Fetching followers...")
        followers = set(p.username for p in profile.get_followers())
        print(f"Fetched {len(followers)} followers.")

        print("Fetching followees...")
        followees = set(p.username for p in profile.get_followees())
        print(f"Fetched {len(followees)} followees.")

        not_following_back = followees - followers
        output_filename = "not_following_back.txt"

        if not_following_back:
            print(f"\nAccounts you follow that don't follow you back (saving to {output_filename}):")
            with open(output_filename, 'w') as f:
                # Sort for consistent output
                for user in sorted(list(not_following_back)):
                    profile_url = f"https://www.instagram.com/{user}/"
                    print(user) # Keep printing to console
                    f.write(profile_url + "\n")
            print(f"\nList saved to {output_filename}")
        else:
            print("\nEveryone you follow follows you back!")
            # Ensure the file is empty if there are no non-followers
            open(output_filename, 'w').close()
            print(f"Created empty file: {output_filename}")

    except Exception as e_fetch:
        print(f"An error occurred while fetching data: {e_fetch}")

if __name__ == "__main__":
    main() 