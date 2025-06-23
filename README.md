```

                 ██████████                                                              
                █▓       ░██                                                             
                █▒        ██                                                  
    █████████████░        █████████████████ ████████████ ████████████      ████████████  
   ██         ███░        ███▓▒▒▒▒▒▒▒▒▒▒▒██ █▒▒▒▒▒▒▒▒▓████        █████████▓          ▒█  
   ██         ███         ███▒▒▒▒▒▒▒▒▒▒▒▒▓██████████████▓        ███▓▒      ▒▓░       ▒█  
   ██         ███        ░██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓██▓▒▒▒▒▒▒▒▒█▓        ███░       ░██░       ▒█  
   ██         ███        ▒██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▓▒▒▒▒▒▒▒▓▒        ██  ▓        ██░       ▓█  
   ██         ██▓        ███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▓▒▒▒▒▒▒▒▓▒       ██   █        ██░       ▓  
   ██         ██▒        ██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▓▒      ██    █        ▓█████████  
   ██                    ██▒▒▒▒▒▒▒▒█▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒   ▒███████ █░       ░▓        █  
   ██         ░░         ██▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█ ▓        ░█ ▓       ░▒       ░█  
   ██         ██░       ░█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█ █░        ▒ █                ░█ 
   ██         ██        ▓█▒▒▒▒▒▒▒▒▒██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█ █░        ▒ █░               ▒█  
    ██████████  ███████████▓██▓▓█▓█  █▓▒▒▒▒▒▒▒▒▒▓██▓██   █▓▓▓▓▓▓▓█    █▓▓▓▓▓▓▓▓▓▓▓▓▓▓██ 
  .:/====================█▓██▓██=========████▓█▓█ ███======> [ P R E S E N T S ] ====\:.
        /\                 ██▓██           █▓▓▓██ ██                                    
 _ __  /  \__________________█▓█_____________██▓██______________________________ _  _    _ 
_ __ \/ /\____________________██_____________ ███________ _________ __ _______ _  
    \  /         T H E   P I N A C L E    O F   H A K C I N G   Q U A L I T Y  
     \/             
            Name :                            haKC.ai AnythingYouCanDO
            Collective:                       haKC.ai
            System:                           UNIX / Linux / MacOS / WinD0$3
            Size:                             1 Script + 1 Disk Worth of Cool
            Supplied by:                      corykennedy     
            Release date:                     Jun 2025 or 1994   

      GROUP NEWS: haKC.ai is Still Looking For haKC Coders & Vibe Artists, 
                  Drop corykennedy A Message on Any Fine BBS in the USA
                        Or On The Internet at cory@haKC.ai.                  
                                                                          /\        
       _ __ ___________________________________________________________  /  \__ _ _ 
       __ __ __ ______________________________________________________ \/ /\____ ___
         |  Notes from the author:                                    \  /         |
         |                                                             \/          |
         |  - Streamlit app to use public LinkedIn posts from anyone as loot.      |
         |  - TOTP MFA required for all users, QR-based IP authentication          |
         |  - Export LinkedIn cookies as JSON, convert in-app, and scrape posts.   |
         |    with Selenium                                                        |
         |  - Collects up to 50 recent posts for any LinkedIn user, saves to CSV.  |
         |  - Instantly generates persona prompts and example outputs              |
         |   (post, email, text)                                                   |
         |  - Logs every action for audit and session tracking                     |
         |                                                                         |
         |  Designed for hackers, privacy, and maximum operational security        |
         |  While you sit back and edit your .nanorc                               |
         |                                       Greetz to the real ones. cory     |
         |*~'`^`'~*-,._.,-*~'`^`'~*-,._.,-*~'`^`'~*-,._.,-*~'`^`'~*-,._.,-*~'`^`'~*|

                     GR33TZ: SecKC, LEGACY CoWTownComputerCongress,ACiD,
                                              iCE, T$A, +o--, badge lords
                     SHOUTZ:
                             [*] 14.4k Modem Jammers
                             [*] l33t soulz still patching proggies & 
                               huntin’ sick ANSIs for their AOHELL punter
                                      FU to [LAMERZ] still using WordPad
                             If your editor auto wraps lines, bounce now.
                          ───── ▓ signed, /dev/CØR.23: ▓ ─────
                                  "nano > vim. come fight us."

```

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/built%20with-streamlit-0f9d58) ![License: MIT](https://img.shields.io/badge/license-MIT-green) ![Made in KC](https://img.shields.io/badge/made%20in-Kansas%20City-lightgrey)



## Table of Contents

* Features
* Quickstart
* How it Works
* Usage Guide
* Security Model
* File Inventory
* Credits

---

## Features

* TOTP-based zero trust authentication. Every IP must scan a QR code or present a valid one-time code.
* LinkedIn persona scraping with robust session persistence and tamper detection.
* On-demand persona synthesis and prompt generation using OpenAI GPT-4o.
* Converts exported LinkedIn session cookies for seamless scraping.
* No cookies? No dice. Paste, convert, and go.
* Session and persona logs for ironclad auditability.
* All wrapped in a Streamlit app with a cyberpunk edge.

---

## Quickstart

1. **Clone the Repo**

   ```shell
   git clone https://github.com/haKC-ai/AnythingYouCanDo.git
   cd AnythingYouCanDo
   ```

2. **Run the Installer**

   ```shell
   bash installer.sh
   ```

   The script will:

   * Check for Python 3
   * Create a virtual environment
   * Install dependencies
   * Verify chromedriver is present
   * Launch the Streamlit app on port 13337

3. **Authenticate**

   * On first visit, generate a QR code with your TOTP app.
   * Each session is IP-bound. QR is one-time for your address.

4. **Paste LinkedIn Cookies**

   * Export cookies from LinkedIn (using EditThisCookie extension in JSON).
   * Paste into the Streamlit sidebar.
   * Click **Save and Convert Cookies**. You’ll see a success message when ready.

5. **Scrape a Persona**

   * Enter the LinkedIn username in the sidebar.
   * Click **Collect LinkedIn Posts**. The app runs the `gimme.py` scraper headlessly.
   * Watch the logs for progress.
   * Review the posts and click **Generate Persona** to synthesize a high-fidelity AI persona.

---

## How it Works

* **AnythingYouCanDo.py**: Main Streamlit UI. Handles authentication, cookie management, persona generation, logging, and persona previewing.
* **gimme.py**: Selenium-driven scraper. Harvests up to 50 recent LinkedIn posts for a given user using exported cookies. Designed to look human, not bot.
* **convert.py**: Cookie converter. Converts EditThisCookie JSON to Netscape-format for Selenium.
* **installer.sh**: Setup wizard. Handles Python environment, dependency installation, chromedriver check, and app startup.

---

## Usage Guide

1. **Authentication**

   * If you see the ASCII art, you’re not in yet.
   * Click **I need a code** to generate a QR. Scan with your TOTP app (like Authy or Google Authenticator).
   * Enter the 6-digit code. You’re now authenticated.

2. **Cookie Export & Import**

   * Install EditThisCookie browser extension.
   * Visit linkedin.com, export all cookies as JSON.
   * Paste into the Streamlit sidebar, convert, and save.

3. **Persona Scraping**

   * Input the LinkedIn username only (not the full URL).
   * Start collection. The app logs everything. If chromedriver is missing, you’ll get a clear prompt.

4. **Persona Synthesis**

   * Once posts are visible, click **Generate Persona**.
   * The app builds a persona prompt using OpenAI and shows examples: LinkedIn post, professional email, and a text message, all in your persona’s voice.

5. **View Personas**

   * Check **Show Created Personas** to see previous persona syntheses and their corresponding prompts and examples.

---

## Security Model

* TOTP MFA for all sessions
* No passwords stored
* OpenAI API key must be provided via `.env`
* Logs every session, action, and persona creation
* Local-only scraping. No data leaves your box except OpenAI prompt content
* Session and persona logs for forensic reconstruction

---

## File Inventory

| File                | Description                                |
| ------------------- | ------------------------------------------ |
| AnythingYouCanDo.py | Main Streamlit app                         |
| installer.sh        | Virtual environment and dependency setup   |
| requirements.txt    | All Python dependencies                    |
| gimme.py            | LinkedIn scraper (Selenium, BeautifulSoup) |
| convert.py          | Cookie converter (JSON to Netscape)        |
| LIS/                | Stores cookies and scraped CSVs            |
| analysis/logs/      | Full logging of app sessions               |
| .env                | Store your OpenAI API key here             |

---

## Credits

* Borrowed some scaping code from this 
* Built by haKC.ai. For hackers, by hackers.
* No warranty. No compliance with LinkedIn’s TOS. Use at your own risk.

---

**If you can do anything, do it responsibly. Welcome to the pinnacle of haKCing quality.**
