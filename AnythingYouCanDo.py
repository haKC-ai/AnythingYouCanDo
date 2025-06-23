import streamlit as st
import os
import openai
import logging
import pyotp
import socket
import qrcode
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
import subprocess
import time
import pandas as pd
import csv
import json
import random

def random_border_color():
    colors = [
        "#FF0055", "#0099FF", "#00C897", "#FFC300", "#FF9800", "#AE00FF",
        "#FF4C4C", "#42FF00", "#FFD700", "#28A745", "#7211DF"
    ]
    return random.choice(colors)

def show_persona_examples_side_by_side(username, persona_text):
    def persona_prompt(example_type, topic=None):
        base = (
            f"You are {username}. Here is your persona description:\n\n{persona_text}\n\n"
        )
        if example_type == "social":
            return (
                base +
                f"Write a short LinkedIn post, in your style, about '{topic or 'the importance of AI-driven threat detection'}'. Keep it punchy, insightful, and less than 70 words. Sign it as {username}."
            )
        elif example_type == "email":
            return (
                base +
                f"Write a concise, professional email in your persona, responding to a colleague's request for advice on improving incident response processes."
            )
        elif example_type == "text":
            return (
                base +
                f"Write a casual text message (2-3 sentences) from {username} to a friend, mentioning something interesting from the cybersecurity field this week."
            )

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with st.spinner("Generating persona examples..."):
        try:
            social_resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": persona_prompt("social")}],
                temperature=0.8,
                max_tokens=128,
            )
            social_post = social_resp.choices[0].message.content.strip()

            email_resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": persona_prompt("email")}],
                temperature=0.7,
                max_tokens=200,
            )
            email_example = email_resp.choices[0].message.content.strip()

            text_resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": persona_prompt("text")}],
                temperature=0.7,
                max_tokens=80,
            )
            text_example = text_resp.choices[0].message.content.strip()
        except Exception as ex:
            st.error(f"Error generating examples: {ex}")
            social_post = email_example = text_example = "[generation failed]"

    # Three columns
    col1, col2, col3 = st.columns(3)
    colors = [random_border_color() for _ in range(3)]

    with col1:
        st.markdown(
            f"""
            <div style='border:2px solid {colors[0]}; border-radius:10px; padding:16px; background:#111;'>
                <h5 style='margin-bottom:6px;'>LinkedIn Post Example</h5>
                <pre style='white-space:pre-wrap; word-break:break-word; color:#fafafa;'>{social_post}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div style='border:2px solid {colors[1]}; border-radius:10px; padding:16px; background:#111;'>
                <h5 style='margin-bottom:6px;'>Professional Email Example</h5>
                <pre style='white-space:pre-wrap; word-break:break-word; color:#fafafa;'>{email_example}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div style='border:2px solid {colors[2]}; border-radius:10px; padding:16px; background:#111;'>
                <h5 style='margin-bottom:6px;'>Text to Friend Example</h5>
                <pre style='white-space:pre-wrap; word-break:break-word; color:#fafafa;'>{text_example}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )

    return social_post, email_example, text_example

# ---- CONFIG ----
SCRAPER_PATH = "LIS/gimme.py"
CSV_PATH = "LIS/user_posts_extended.csv"
PERSONA_CSV_PATH = "LIS/personas.csv"

# ------------- TOTP Auth Gate ---------------
totp_secrets_path = "analysis/totp_secrets.txt"
os.makedirs("analysis", exist_ok=True)
if not os.path.exists(totp_secrets_path):
    with open(totp_secrets_path, "w"):
        pass

with open(totp_secrets_path) as f:
    ip_totp = dict(
        line.strip().split("::") for line in f if "::" in line
    )

params = st.query_params
if "ip" in params:
    client_ip = params["ip"][0]
else:
    client_ip = socket.gethostbyname(socket.gethostname())

# Session state for auth
if "totp_authenticated" not in st.session_state:
    st.session_state["totp_authenticated"] = False
if "totp_pending" not in st.session_state:
    st.session_state["totp_pending"] = False

if not st.session_state["totp_authenticated"]:
    st.set_page_config(
        layout="wide",
        page_title="haKC.ai - TOTP Authentication",
        page_icon="favicon.png"
    )

    green_css = """
        <style>
            .hacker-green {
                color: #00FF00 !important;
                font-family: 'Fira Mono', 'Consolas', 'Menlo', monospace;
                background: #111 !important;
                padding: 18px 8px 18px 0;
                font-size: 14px;
                border-radius: 8px;
            }
        </style>
    """
    st.markdown(green_css, unsafe_allow_html=True)

    art = """
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
    """

    col1, col2 = st.columns([2, 1.8])
    with col1:
        st.code(art, language="text")
    with col2:
        # Step 1: Buttons to begin
        colB1, colB2 = st.columns(2)
        need_code = colB1.button("I need a code")
        have_code = colB2.button("I have a code")

        if client_ip not in ip_totp and not st.session_state["totp_pending"]:
            st.warning("You are not registered. Generate a TOTP QR to proceed.")
            if need_code:
                new_secret = pyotp.random_base32()
                totp_uri = pyotp.totp.TOTP(new_secret).provisioning_uri(
                    name=client_ip,
                    issuer_name="haKC.ai - AnythingYouCanDo App"
                )
                qr = qrcode.make(totp_uri)
                buf = BytesIO()
                qr.save(buf)
                logo_path = "assets/app_logo.png"
                logo_url = "https://raw.githubusercontent.com/haKC-ai/haKCAssets/refs/heads/main/haKCAI.png"
                if os.path.exists(logo_path):
                    st.image(logo_path, caption="App Logo for Authenticator", width=120)
                else:
                    st.image(logo_url, caption="App Logo for Authenticator", width=120)
                st.markdown("**Scan the QR code below with your TOTP authenticator.**<br>"
                            "If your authenticator app asks for a logo, use the image above.",
                            unsafe_allow_html=True)
                st.image(buf.getvalue(), caption="Scan with your TOTP Authenticator")
                with open(totp_secrets_path, "a") as f:
                    f.write(f"{client_ip}::{new_secret}\n")
                st.info("QR generated. Once added to your authenticator, enter your code below to login.")
                st.session_state["totp_pending"] = True

            elif have_code:
                st.session_state["totp_pending"] = True

            if st.session_state.get("totp_pending", False):
                st.caption("Enter your 6-digit TOTP code")
                code_input = st.text_input("", max_chars=6, type="password", key="pending_totp")
                if st.button("Login", key="pending_login"):
                    secret = None
                    with open(totp_secrets_path) as f:
                        for line in f:
                            ip, s = line.strip().split("::")
                            if ip == client_ip:
                                secret = s
                                break
                    if not secret:
                        st.error("No secret found for this IP. Please use 'I need a code' first.")
                        st.stop()
                    if not code_input:
                        st.warning("Enter your TOTP code to proceed.")
                        st.stop()
                    if not pyotp.TOTP(secret).verify(code_input):
                        st.error("Invalid code")
                        st.stop()
                    st.session_state["totp_authenticated"] = True
                    st.session_state["totp_pending"] = False
                    st.success("Authentication successful!")
                    st.rerun()
                st.stop()
            else:
                st.stop()

        elif st.session_state.get("totp_pending", False):
            st.caption("Enter your 6-digit TOTP code")
            code_input = st.text_input("", max_chars=6, type="password", key="pending_totp2")
            if st.button("Login", key="pending_login2"):
                secret = ip_totp.get(client_ip)
                if not secret:
                    st.error("No secret found for this IP. Please use 'I need a code' first.")
                    st.stop()
                if not code_input:
                    st.warning("Enter your TOTP code to proceed.")
                    st.stop()
                if not pyotp.TOTP(secret).verify(code_input):
                    st.error("Invalid code")
                    st.stop()
                st.session_state["totp_authenticated"] = True
                st.session_state["totp_pending"] = False
                st.success("Authentication successful!")
                st.rerun()
            st.stop()
        else:
            # User is already registered; show standard code prompt
            st.caption("Enter your 6-digit TOTP code")
            code_input = st.text_input("", type="password", max_chars=6, key="std_totp")
            if st.button("Login", key="std_login"):
                secret = ip_totp.get(client_ip)
                if not code_input:
                    st.warning("Enter your TOTP code to proceed.")
                    st.stop()
                if not pyotp.TOTP(secret).verify(code_input):
                    st.error("Invalid code")
                    st.stop()
                st.session_state["totp_authenticated"] = True
                st.success("Authentication successful!")
                st.rerun()
            st.stop()


# --- Auth Passed ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.sidebar.image("assets/sidebar_logo.png")

with st.sidebar.expander("Configuration"):
    cookie_json = st.text_area(
        "Paste the full JSON you copied from EditThisCookie (while on linkedin.com):",
        height=200, key="cookies_paste"
    )
    save_cookie_btn = st.button("Save and Convert Cookies", key="save_cookies_btn")
    if save_cookie_btn:
        try:
            # Parse and save the JSON as a file
            json_obj = json.loads(cookie_json)
            os.makedirs("LIS", exist_ok=True)
            json_path = "LIS/lnkedin_cookies.json"
            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(json_obj, jf, indent=2)
            # Call the converter
            result = subprocess.run(
                ["python3", "LIS/convert.py"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and os.path.exists("LIS/lnkedin_cookies.txt"):
                st.success("Cookies converted successfully! You are ready to scrape.")
                st.text("Output:\n" + result.stdout)
            else:
                st.error("Conversion failed. See details below:")
                st.text(result.stderr + "\n" + result.stdout)
        except Exception as e:
            st.error(f"Error saving/converting cookies: {e}")
            
log_dir = "analysis/logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=f"{log_dir}/session_{datetime.now().isoformat()}.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

st.set_page_config(
    layout="wide",
    page_title="haKC.ai - AnythingYouCanDO",
    page_icon="assets/sidebar_logo.png"
)

if os.path.exists("styles.css"):
    with open("styles.css") as f_css:
        st.markdown(f"<style>{f_css.read()}</style>", unsafe_allow_html=True)

#st.image("assets/main_logo.png", use_container_width=True)
st.code("haKC.ai LinkedIn Persona Extractor")

username = st.sidebar.text_input("LinkedIn username to use (e.g., corykennedy)", key="ln_user")
scrape_trigger = st.sidebar.button("Collect LinkedIn Posts")

if scrape_trigger and username:
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
    with st.spinner("Collecting comments, please wait..."):
        scraper_log = ""
        ignore_patterns = [
            "NotOpenSSLWarning", "chromedriver version", "LibreSSL",
            "See: https://github.com/urllib3/urllib3/issues/3020", " warnings.warn("
        ]
        process = subprocess.Popen(
            ["python3", SCRAPER_PATH, username],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
        )
        with st.expander("Scraper Output (click to expand)", expanded=False):
            scraper_code_box = st.empty()
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                if any(pattern in line for pattern in ignore_patterns):
                    continue
                scraper_log += line
                scraper_code_box.code(scraper_log, language="text")
                if "[*] Finished" in line:
                    break
                time.sleep(0.1)
            process.wait()
        st.success("Collection complete.")

def parse_multiuser_csv(csv_path):
    results = {}
    current_username = None
    current_rows = []
    with open(csv_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("linked_in_profile_name="):
                if current_username and current_rows:
                    results[current_username] = pd.DataFrame(current_rows[1:], columns=current_rows[0])
                current_username = line.split("=", 1)[1]
                current_rows = []
            elif current_username is not None:
                row = next(csv.reader([line]))
                current_rows.append(row)
        if current_username and current_rows:
            results[current_username] = pd.DataFrame(current_rows[1:], columns=current_rows[0])
    return results

st.sidebar.code("Persona Tools")
show_personas = st.sidebar.checkbox("`Show Created Personas`", value=False)

users_data = {}
if os.path.exists(CSV_PATH):
    users_data = parse_multiuser_csv(CSV_PATH)

if users_data:
    usernames = list(users_data.keys())
    user_selected = st.multiselect(
        "Select LinkedIn username(s) to view",
        options=usernames,
        default=[usernames[0]] if usernames else []
    )

    for username in user_selected:
        df = users_data[username]
        st.markdown(f"## Posts for {username}")
        st.dataframe(df)
        all_posts_text = "\n\n".join(df["Post_Content"].dropna().astype(str))
        if st.button(f"Generate Persona for {username}"):
            prompt = (
                f"Read the following public LinkedIn posts and construct a promot persona:\n\n{all_posts_text[:7000]}"
            )
            logging.info(f"Generating persona for user: {username}")
            try:
                client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a cyberpunk data synthesizer that creates insightful "
                                "personas from public LinkedIn posts."
                            ),
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=1,
                )
                persona_text = response.choices[0].message.content.strip()
                st.success("Persona generated!")
            except Exception as e:
                persona_text = f"Error generating persona: {e}"
                st.error(persona_text)
            st.markdown("### Persona")
            st.write(persona_text)
            social_post, email_example, text_example = show_persona_examples_side_by_side(username, persona_text)

            # Save persona and examples to personas.csv
            persona_exists = os.path.exists(PERSONA_CSV_PATH)
            with open(PERSONA_CSV_PATH, "a", encoding="utf-8", newline='') as pf:
                writer = csv.writer(pf)
                if not persona_exists:
                    writer.writerow([
                        "linked_in_profile_name",
                        "persona",
                        "linkedin_post_example",
                        "professional_email_example",
                        "friend_text_example",
                        "timestamp"
                    ])
                writer.writerow([
                    username,
                    persona_text,
                    social_post,
                    email_example,
                    text_example,
                    datetime.now().isoformat()
                ])

# --- Sidebar: show generated personas ---
if show_personas and os.path.exists(PERSONA_CSV_PATH):
    dfp = pd.read_csv(PERSONA_CSV_PATH)
    st.caption("Generated Personas")
    st.dataframe(dfp)
