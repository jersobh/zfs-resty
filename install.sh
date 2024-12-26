#!/bin/bash

# Installation script for ZFS REST API Service with Virtualenv

set -e

# Get the current directory
CURRENT_DIR=$(pwd)

# Create a virtual environment
VENV_DIR="$CURRENT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
. "$VENV_DIR/bin/activate"

# Install dependencies
pip install -r "$CURRENT_DIR/requirements.txt"

# Create systemd service file
SERVICE_FILE="/etc/systemd/system/zfs-resty.service"
echo "Creating systemd service file at $SERVICE_FILE"

sudo bash -c "cat > $SERVICE_FILE" << EOL
[Unit]
Description=ZFS REST API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$CURRENT_DIR
ExecStart=$VENV_DIR/bin/python $CURRENT_DIR/zfs-resty.py
Restart=always
Environment="LOG_LEVEL=INFO"
Environment="LOG_FILENAME=/var/log/zfs-resty.log"

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable zfs-resty

# Start the service
sudo systemctl start zfs-resty

# Check service status
sudo systemctl status zfs-resty

echo "ZFS REST API Service installed and started successfully!"
