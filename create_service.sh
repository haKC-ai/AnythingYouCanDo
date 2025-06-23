#!/usr/bin/env bash
set -e

APP_DIR=$(cd "$(dirname "$0")" && pwd)
SERVICE_NAME=persona-app
USER=$(whoami)

SERVICE_FILE=/etc/systemd/system/${SERVICE_NAME}.service

echo "[Unit]" | sudo tee ${SERVICE_FILE}
echo "Description=haKC.ai Persona Extractor" | sudo tee -a ${SERVICE_FILE}
echo "After=network.target" | sudo tee -a ${SERVICE_FILE}
echo "" | sudo tee -a ${SERVICE_FILE}
echo "[Service]" | sudo tee -a ${SERVICE_FILE}
echo "WorkingDirectory=${APP_DIR}" | sudo tee -a ${SERVICE_FILE}
echo "ExecStart=${APP_DIR}/venv/bin/streamlit run ${APP_DIR}/linkedin_persona_streamlit.py --server.address 0.0.0.0 --server.port 1337" | sudo tee -a ${SERVICE_FILE}
echo "Environment=OPENAI_API_KEY=$(grep OPENAI_API_KEY ${APP_DIR}/.env | cut -d '=' -f2)" | sudo tee -a ${SERVICE_FILE}
echo "Restart=always" | sudo tee -a ${SERVICE_FILE}
echo "RestartSec=5" | sudo tee -a ${SERVICE_FILE}
echo "User=${USER}" | sudo tee -a ${SERVICE_FILE}
echo "" | sudo tee -a ${SERVICE_FILE}
echo "[Install]" | sudo tee -a ${SERVICE_FILE}
echo "WantedBy=multi-user.target" | sudo tee -a ${SERVICE_FILE}

echo "[+] Reloading systemd..."
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
echo "[+] Service ${SERVICE_NAME} installed. Start it with: sudo systemctl start ${SERVICE_NAME}"
