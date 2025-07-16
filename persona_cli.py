import os
import openai
import logging
import subprocess
import pandas as pd
import csv
import json
from datetime import datetime
from dotenv import load_dotenv
from tabulate import tabulate

# ---- CONFIGURATION ----
LIS_DIR = "LIS"
ANALYSIS_DIR = "analysis"
SCRAPER_PATH = os.path.join(LIS_DIR, "gimme.py")
CONVERTER_PATH = os.path.join(LIS_DIR, "convert.py")
COOKIE_JSON_PATH = os.path.join(LIS_DIR, "lnkedin_cookies.json")
COOKIE_TXT_PATH = os.path.join(LIS_DIR, "lnkedin_cookies.txt")
POSTS_CSV_PATH = os.path.join(LIS_DIR, "user_posts_extended.csv")
PERSONA_CSV_PATH = os.path.join(LIS_DIR, "personas.csv")
LOG_DIR = os.path.join(ANALYSIS_DIR, "logs")

# --- HELPER FUNCTIONS ---

def print_header(title):
    bar = "=" * (len(title) + 8)
    print(f"\n{bar}")
    print(f"    {title.upper()}")
    print(f"{bar}")

def print_error(message):
    print(f"[!] ERROR: {message}")

def print_success(message):
    print(f"[✔] SUCCESS: {message}")

def print_info(message):
    print(f"[*] INFO: {message}")

def setup_directories_and_files():
    os.makedirs(LIS_DIR, exist_ok=True)
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(LOG_DIR, f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )

# ---- CORE FEATURES ----

def configure_cookies():
    # This function remains unchanged.
    print_header("Configure LinkedIn Cookies")
    print("Paste the full JSON content from the EditThisCookie extension.")
    print("Press Ctrl+D (Linux/macOS) or Ctrl+Z then Enter (Windows) to finish.")
    
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    cookie_json_str = "".join(lines)

    if not cookie_json_str.strip():
        print_error("No input received. Cookie configuration cancelled.")
        return

    try:
        json_obj = json.loads(cookie_json_str)
        with open(COOKIE_JSON_PATH, "w", encoding="utf-8") as jf:
            json.dump(json_obj, jf, indent=2)
        print_success(f"Cookie JSON saved to '{COOKIE_JSON_PATH}'")

        if not os.path.exists(CONVERTER_PATH):
            print_error(f"Converter script not found at '{CONVERTER_PATH}'. Cannot proceed.")
            return

        print_info("Converting cookies for use with the scraper...")
        result = subprocess.run(
            ["python3", CONVERTER_PATH],
            capture_output=True, text=True, check=False
        )
        if result.returncode == 0 and os.path.exists(COOKIE_TXT_PATH):
            print_success(f"Cookies converted successfully to '{COOKIE_TXT_PATH}'!")
        else:
            print_error("Cookie conversion failed.")
            print("--- Stderr ---\n" + result.stderr)
            print("--- Stdout ---\n" + result.stdout)
    except Exception as e:
        print_error(f"An error occurred during cookie configuration: {e}")

def run_scraper():
    """
    MODIFIED: Handles both a single username and a file path with multiple usernames.
    """
    print_header("Collect LinkedIn Posts")
    
    if not os.path.exists(COOKIE_TXT_PATH):
        print_error(f"Cookie file '{COOKIE_TXT_PATH}' not found. Please run 'Configure Cookies' first.")
        return

    user_input = input("Enter a single username OR the path to a file with usernames (one per line): ").strip()
    if not user_input:
        print_error("Input cannot be empty.")
        return

    usernames_to_process = []
    if os.path.exists(user_input):
        print_info(f"File found. Reading usernames from '{user_input}'...")
        try:
            with open(user_input, 'r', encoding='utf-8') as f:
                usernames_to_process = [line.strip() for line in f if line.strip()]
            if not usernames_to_process:
                print_error("The specified file is empty.")
                return
            print_success(f"Found {len(usernames_to_process)} usernames to process.")
        except Exception as e:
            print_error(f"Failed to read file: {e}")
            return
    else:
        print_info(f"Treating '{user_input}' as a single username.")
        usernames_to_process = [user_input]

    # Handle overwriting the main CSV file once before the batch starts
    if os.path.exists(POSTS_CSV_PATH):
        if input(f"'{POSTS_CSV_PATH}' exists. Overwrite with new scrape results? (y/n): ").lower() != 'y':
            print_info("Scraping cancelled by user.")
            return
        os.remove(POSTS_CSV_PATH)
        print_info("Existing results file has been removed.")

    total_users = len(usernames_to_process)
    for i, username in enumerate(usernames_to_process):
        print_header(f"Processing User {i+1}/{total_users}: {username}")
        
        try:
            process = subprocess.Popen(
                ["python3", SCRAPER_PATH, username],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
            )
            for line in iter(process.stdout.readline, ''):
                print(line, end='')
            process.wait()
            if process.returncode != 0:
                print_error(f"Scraper for '{username}' exited with code {process.returncode}.")
        except FileNotFoundError:
            print_error(f"Scraper script not found at '{SCRAPER_PATH}'. Aborting.")
            return
        except Exception as e:
            print_error(f"An error occurred while running the scraper for '{username}': {e}")
    
    print_header("Batch Scraping Complete")
    print_success(f"Processed {total_users} user(s). Results are in '{POSTS_CSV_PATH}'.")

def generate_persona():
    # This function remains unchanged as it can already handle a multi-user CSV.
    print_header("Generate Persona from Scraped Data")
    if not os.path.exists(POSTS_CSV_PATH):
        print_error(f"No scraped data found at '{POSTS_CSV_PATH}'. Please run the scraper first.")
        return

    try:
        df = pd.read_csv(POSTS_CSV_PATH, header=None, names=['Username', 'Post_Content'])
        users = df['Username'].unique()
    except Exception as e:
        print_error(f"Could not read or parse '{POSTS_CSV_PATH}': {e}")
        return

    if not users.any():
        print_error("No users found in the scraped data file.")
        return
        
    print("Available users in scraped data:")
    for i, user in enumerate(users):
        print(f"  [{i+1}] {user}")
    
    try:
        choice = int(input(f"Select a user to generate a persona for (1-{len(users)}): ")) - 1
        if not 0 <= choice < len(users):
            raise ValueError
        selected_user = users[choice]
    except (ValueError, IndexError):
        print_error("Invalid selection. Aborting.")
        return

    user_posts = df[df['Username'] == selected_user]['Post_Content'].dropna().astype(str)
    all_posts_text = "\n\n---\n\n".join(user_posts)

    if not all_posts_text.strip():
        print_error(f"No post content found for user '{selected_user}'.")
        return

    print_info(f"Generating persona for '{selected_user}'. This involves multiple API calls...")
    logging.info(f"Initiating persona generation for user: {selected_user}")

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        persona_prompt = f"Read the following public LinkedIn posts from a user and construct a detailed professional persona. Describe their communication style, recurring topics of interest, likely technical expertise, and overall tone. Be insightful and structured.\n\nPOSTS:\n{all_posts_text[:8000]}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a data analyst that creates professional personas from public social media data."},
                {"role": "user", "content": persona_prompt}
            ],
            temperature=0.6, max_tokens=1024
        )
        persona_text = response.choices[0].message.content.strip()
        print_success("Core persona description generated.")
        
        print_info("Generating communication examples...")
        
        def generate_example(example_type, topic=None):
            base = f"You are a person with this exact persona:\n\n---\n{persona_text}\n---\n\nBased *only* on this persona, write a realistic example of the following communication:"
            if example_type == "social": return base + f" A short, insightful LinkedIn post about '{topic or 'the future of AI in threat intelligence'}'. Sign it with the user's name."
            elif example_type == "email": return base + " A concise, professional email to a colleague suggesting a new tool for the team's workflow."
            elif example_type == "text": return base + " A casual text message to a friend mentioning an interesting article they read."
        
        social_resp = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": generate_example("social")}], temperature=0.7, max_tokens=150)
        email_resp = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": generate_example("email")}], temperature=0.7, max_tokens=200)
        text_resp = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": generate_example("text")}], temperature=0.8, max_tokens=100)
        
        social_post = social_resp.choices[0].message.content.strip()
        email_example = email_resp.choices[0].message.content.strip()
        text_example = text_resp.choices[0].message.content.strip()

        print_header(f"Generated Persona & Examples for {selected_user}")
        print("\n--- PROFESSIONAL PERSONA ---\n")
        print(persona_text)
        print("\n" + "="*28 + " EXAMPLES " + "="*28)
        print("\n[ LinkedIn Post Example ]")
        print(social_post)
        print("\n[ Professional Email Example ]")
        print(email_example)
        print("\n[ Casual Text Example ]")
        print(text_example)
        print("\n" + "="*66)

        persona_exists = os.path.exists(PERSONA_CSV_PATH)
        with open(PERSONA_CSV_PATH, "a", encoding="utf-8", newline='') as pf:
            writer = csv.writer(pf)
            if not persona_exists:
                writer.writerow(["linked_in_profile_name", "persona", "linkedin_post_example", "professional_email_example", "friend_text_example", "timestamp"])
            writer.writerow([selected_user, persona_text, social_post, email_example, text_example, datetime.now().isoformat()])
        print_success(f"Persona and examples saved to '{PERSONA_CSV_PATH}'.")

    except openai.APIError as e:
        print_error(f"OpenAI API Error: {e}. Check your API key and account status.")
        logging.error(f"OpenAI API Error: {e}")
    except Exception as e:
        print_error(f"An unexpected error occurred during persona generation: {e}")
        logging.error(f"Persona generation failed: {e}")

def view_personas():
    # This function remains unchanged.
    print_header("View Saved Personas")
    if not os.path.exists(PERSONA_CSV_PATH):
        print_error(f"Persona file not found at '{PERSONA_CSV_PATH}'. Please generate a persona first.")
        return
        
    try:
        df = pd.read_csv(PERSONA_CSV_PATH)
        if df.empty:
            print_info("The persona file is empty.")
            return
        
        df['persona'] = df['persona'].str.slice(0, 70) + '...'
        df['linkedin_post_example'] = df['linkedin_post_example'].str.slice(0, 50) + '...'
        
        print(tabulate(df[['linked_in_profile_name', 'persona', 'linkedin_post_example', 'timestamp']], headers='keys', tablefmt='grid'))
        print("\nNOTE: Text is truncated for display. Full content is in the CSV file.")

    except Exception as e:
        print_error(f"Could not read or display the persona file: {e}")

# ---- MAIN APPLICATION LOOP ----

def main():
    load_dotenv()
    setup_directories_and_files()

    if not os.getenv("OPENAI_API_KEY"):
        print_error("OPENAI_API_KEY not found in .env file. Please set it to continue.")
        return

    while True:
        print_header("haKC.ai - LinkedIn Persona Extractor")
        print(" [1] Configure LinkedIn Cookies")
        print(" [2] Collect LinkedIn Posts (Scrape)")
        print(" [3] Generate Persona from Data")
        print(" [4] View Saved Personas")
        print(" [5] Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            configure_cookies()
        elif choice == '2':
            run_scraper()
        elif choice == '3':
            generate_persona()
        elif choice == '4':
            view_personas()
        elif choice == '5':
            print("Exiting. Goodbye!")
            break
        else:
            print_error("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
