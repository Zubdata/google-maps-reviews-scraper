#!/bin/bash

# Function to display messages
function echo_info {
    echo "[INFO] $1"
}

# Ensure you're in the repository directory
echo_info "Setting up the project in the current directory..."

# Install dependencies
echo_info "Installing dependencies..."
pip3 install -r requirements.txt

# Install chromium
echo_info "Installing chromium..."
playwright install chromium

# Launch the GUI
echo_info "Launching the GUI..."
python src/main.py
