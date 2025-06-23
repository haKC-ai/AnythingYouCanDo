#!/usr/bin/env bash
set -e

echo "[+] Checking Python 3..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "[!] python3 not found. Install Python 3."
    exit 1
fi

echo "[+] Checking virtualenv..."
if ! command -v virtualenv >/dev/null 2>&1; then
    echo "[+] Installing virtualenv..."
    pip3 install virtualenv
fi

echo "[+] Creating Python virtual environment in venv..."
python3 -m venv venv
source venv/bin/activate

echo "[+] Installing Streamlit app requirements..."
pip install --upgrade pip
pip install -r requirements.txt



# chromedriver check
if ! command -v chromedriver >/dev/null 2>&1; then
    echo "[!] chromedriver not found. Download from https://chromedriver.chromium.org/downloads and add to PATH."
    echo "[!] Exiting so you can install chromedriver."
    exit 1
fi


echo "[+] Setup complete."
echo ""
echo "To launch your Streamlit app:"
echo "    source venv/bin/activate"
echo "    streamlit run AnythingYouCanDo.py --server.address 0.0.0.0 --server.port 13337"
echo "Note: If you need to export LinkedIn cookies, see the instructions above."

source venv/bin/activate
streamlit run AnythingYouCanDo.py --server.address 0.0.0.0 --server.port 13337