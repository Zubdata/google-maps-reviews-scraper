# Ensure you're in the repository directory
Write-Host "[INFO] Setting up the project in the current directory..."

# Install dependencies
Write-Host "[INFO] Installing dependencies..."
pip install -r requirements.txt

# Install chromium
Write-Host "[INFO] Installing chromium..."
playwright install chromium

# Launch the GUI
Write-Host "[INFO] Launching the GUI..."
python src/main.py
