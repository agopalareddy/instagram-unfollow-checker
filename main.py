import instaloader
import os
import customtkinter as ctk
import threading
import queue

ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Fixed height for the log textbox
LOG_FIXED_HEIGHT = 250 # Adjust as needed

class InstagramApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Instagram Unfollow Checker")
        # Adjusted height for removed checkbox
        self.geometry("500x600")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        # Give row 4 (textbox) the weight for expansion
        self.grid_rowconfigure(4, weight=1)

        # --- Variables ---
        self.username_var = ctk.StringVar()
        self.username_var.trace_add("write", self.check_session_on_username_change)

        # --- Widgets ---
        self.username_label = ctk.CTkLabel(self, text="Instagram Username:")
        self.username_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Enter username", textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")

        self.password_label = ctk.CTkLabel(self, text="Instagram Password:")
        self.password_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter password (if needed)", show="*")
        self.password_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.run_button = ctk.CTkButton(self, text="Find Non-Followers", command=self.start_instagram_check)
        self.run_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status:")
        self.status_label.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="w") # Span label

        self.status_textbox = ctk.CTkTextbox(self, state="disabled", wrap="word", height=LOG_FIXED_HEIGHT)
        self.status_textbox.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew") # Textbox now in row 4

        # --- Threading and Queue ---
        self.message_queue = queue.Queue()
        self.after(100, self.process_queue)

        # Initial session check
        self.check_session_on_username_change()

    def check_session_on_username_change(self, *args):
        """Called when username changes. Enables/disables password based on session file."""
        username = self.username_var.get()
        session_file = f"{username}.session"
        if username and os.path.exists(session_file):
            self.password_entry.configure(state="disabled", placeholder_text="Session found - Password not needed initially")
            # Clear any potentially stale password if session exists
            self.password_entry.delete(0, "end")
            self.run_button.configure(text="Find Non-Followers (Use Session)")
        else:
            self.password_entry.configure(state="normal", placeholder_text="Enter password")
            self.run_button.configure(text="Find Non-Followers")

    def log_message(self, message):
        """Adds a message to the queue for safe GUI updates."""
        self.message_queue.put(message)

    def process_queue(self):
        """Processes messages from the queue to update the GUI."""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.status_textbox.configure(state="normal")
                current_content = self.status_textbox.get("1.0", "end-1c") # Get content without trailing newline
                # Add newline only if textbox isn't empty
                prefix = "\n" if current_content else ""
                self.status_textbox.insert("end", prefix + message)
                self.status_textbox.see("end") # Scroll to the bottom
                self.status_textbox.configure(state="disabled")
        except queue.Empty:
            pass # No messages left
        finally:
            # Reschedule itself
            self.after(100, self.process_queue)

    def set_ui_state(self, state):
        """Enable or disable UI elements, respecting session state for password."""
        self.username_entry.configure(state=state)
        # Only re-enable password if no valid session file exists for current user
        username = self.username_var.get()
        session_file = f"{username}.session"
        if state == "normal" and (not username or not os.path.exists(session_file)):
             self.password_entry.configure(state="normal")
        elif state == "disabled":
             self.password_entry.configure(state="disabled")
        # else: keep password disabled if session exists and state is normal

        self.run_button.configure(state=state)

    def request_password_for_failed_session(self):
        """Called from worker thread via self.after to handle session failure."""
        self.log_message("\nError: Session is invalid or expired.")
        self.log_message("Please enter your password and click 'Find Non-Followers' again.")
        self.password_entry.configure(state="normal", placeholder_text="Enter password")
        self.run_button.configure(state="normal", text="Find Non-Followers")
        self.username_entry.configure(state="normal") # Also re-enable username entry

    def get_two_factor_code(self):
        """Prompts the user for a 2FA code using a dialog."""
        dialog = ctk.CTkInputDialog(text="Enter 2FA Code:", title="Two-Factor Authentication")
        code = dialog.get_input()
        return code

    def start_instagram_check(self):
        username = self.username_entry.get()
        password = None # Assume session login first if applicable

        if not username:
            self.log_message("Error: Please enter a username.")
            return

        # Check if password entry is enabled (meaning we NEED a password)
        if self.password_entry.cget("state") == "normal":
            password = self.password_entry.get()
            if not password:
                self.log_message("Error: Please enter your password.")
                return

        self.log_message("\n-- Starting check --")
        self.set_ui_state("disabled")

        # Simplification: Always clear for a new run
        self.status_textbox.configure(state="normal")
        self.status_textbox.delete("1.0", "end")
        self.status_textbox.configure(state="disabled")
        self.log_message("Please wait...") # Initial message after clearing

        # Run Instagram logic in a separate thread
        thread = threading.Thread(target=self.run_instagram_logic, args=(username, password), daemon=True)
        thread.start()

    def run_instagram_logic(self, username, password):
        """Handles the core Instaloader interaction in a separate thread."""
        try:
            L = instaloader.Instaloader()
            session_file = f"{username}.session"
            logged_in = False
            session_load_attempted = False

            # --- Session Loading (Try first if password wasn't provided) ---
            if not password and os.path.exists(session_file):
                session_load_attempted = True
                self.log_message(f"Attempting to load session for {username}...")
                try:
                    L.load_session_from_file(username, session_file)
                    L.test_login() # Verify session validity
                    self.log_message("Session loaded and valid.")
                    logged_in = True
                except (FileNotFoundError, instaloader.exceptions.BadCredentialsException,
                        instaloader.exceptions.ConnectionException, instaloader.exceptions.QueryReturnedNotFoundException,
                        instaloader.exceptions.TwoFactorAuthRequiredException) as e:
                    self.log_message(f"Session loading failed: {e}")
                    # Need to request password from the main thread
                    self.after(0, self.request_password_for_failed_session)
                    return # Stop thread execution here
                except Exception as e_sess:
                    # Catch unexpected session errors
                    self.log_message(f"Unexpected error during session load: {e_sess}")
                    self.after(0, self.request_password_for_failed_session)
                    return

            # --- Login (if session failed, or wasn't attempted, or password was provided) ---
            if not logged_in:
                if session_load_attempted:
                     self.log_message("Internal Error: Login flow reached unexpectedly after session failure.")
                     self.after(0, self.set_ui_state, "normal")
                     return
                elif not password:
                     self.log_message("Error: No session found and no password provided.")
                     self.after(0, self.set_ui_state, "normal") # Re-enable UI
                     return

                self.log_message("Logging in with password...")
                try:
                    L.login(username, password)
                    self.log_message("Login successful.")
                    L.save_session_to_file(session_file)
                    self.log_message(f"Session saved to {session_file}")
                    logged_in = True
                except instaloader.exceptions.TwoFactorAuthRequiredException:
                    self.log_message("Two-Factor Authentication required.")
                    two_factor_code = self.get_two_factor_code()
                    if not two_factor_code:
                         self.log_message("Error: 2FA code not provided. Aborting.")
                         self.after(0, self.set_ui_state, "normal")
                         return
                    try:
                        L.two_factor_login(two_factor_code)
                        self.log_message("2FA Login successful.")
                        L.save_session_to_file(session_file)
                        self.log_message(f"Session saved to {session_file}")
                        logged_in = True
                    except instaloader.exceptions.BadCredentialsException:
                        self.log_message("Error: Invalid 2FA code.")
                        self.after(0, self.set_ui_state, "normal")
                        return
                    except Exception as e_2fa:
                        self.log_message(f"Error during 2FA login: {e_2fa}")
                        self.after(0, self.set_ui_state, "normal")
                        return
                except instaloader.exceptions.BadCredentialsException:
                    self.log_message("Error: Invalid username or password.")
                    self.after(0, self.set_ui_state, "normal")
                    return
                except Exception as e_login:
                    self.log_message(f"Error during login: {e_login}")
                    self.after(0, self.set_ui_state, "normal")
                    return

            # --- Fetching Data --- (Only if login or session load was successful)
            if logged_in:
                try:
                    self.log_message("Fetching profile...")
                    profile = instaloader.Profile.from_username(L.context, username)

                    self.log_message("Fetching followers (this may take time)...")
                    followers = set(p.username for p in profile.get_followers())
                    self.log_message(f"Fetched {len(followers)} followers.")

                    self.log_message("Fetching followees (this may take time)...")
                    followees = set(p.username for p in profile.get_followees())
                    self.log_message(f"Fetched {len(followees)} followees.")

                    not_following_back = sorted(list(followees - followers))
                    output_filename = "not_following_back.txt"

                    self.log_message("\n--- Results ---")
                    if not_following_back:
                        self.log_message(f"Found {len(not_following_back)} accounts you follow that don't follow back:")
                        with open(output_filename, 'w') as f:
                            for user in not_following_back:
                                profile_url = f"https://www.instagram.com/{user}/"
                                self.log_message(f"- {user}")
                                f.write(profile_url + "\n")
                        self.log_message(f"\nFull list saved to {output_filename}")
                    else:
                        self.log_message("Everyone you follow follows you back!")
                        open(output_filename, 'w').close()
                        self.log_message(f"Cleared/Created file: {output_filename}")

                    self.log_message("\nCheck complete.")

                # Catch the specific rate-limit error
                except instaloader.exceptions.ConnectionException as e_conn:
                    if "401 Unauthorized" in str(e_conn) and "Please wait a few minutes" in str(e_conn):
                        self.log_message("\nError: Instagram is temporarily limiting requests from this session.")
                        self.log_message("Please wait a few minutes (or longer) and try again.")
                        self.log_message("Using the session file (if available) might help.")
                    else:
                        # Re-raise other connection errors
                        self.log_message(f"\nConnection Error: {e_conn}")
                        self.log_message("Check your internet connection.")
                        # Optionally log traceback for unexpected connection errors
                        # import traceback
                        # self.log_message(traceback.format_exc())

        except Exception as e_main:
            self.log_message(f"\nAn unexpected error occurred: {e_main}")
            import traceback
            self.log_message(traceback.format_exc())
        finally:
            # Ensure UI is re-enabled unless specific errors occurred that need user action
            # (Password prompt already handled inside login logic)
            # If logged_in is False after a session attempt, it means session failed and password was requested.
            # If logged_in is False after a password attempt, login failed.
            # If logged_in is True, the try/except block for fetching handles UI enabling.

            # Re-enable UI if login failed or if fetch completed/failed cleanly
            # Only skip re-enabling if password prompt is active due to session failure
            ui_needs_reenable = True
            if not logged_in and session_load_attempted:
                # Check if password field is enabled (meaning prompt is active)
                if self.password_entry.cget("state") == "normal":
                    ui_needs_reenable = False # Don't re-enable if waiting for password

            if ui_needs_reenable:
                 self.after(0, self.set_ui_state, "normal")

if __name__ == "__main__":
    app = InstagramApp()
    app.mainloop() 