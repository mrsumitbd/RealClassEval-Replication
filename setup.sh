#!/usr/bin/env bash
# ==========================================================
# Setup script for replication package
# Compatible with Linux/macOS
# ==========================================================

set -e  # Exit immediately on error

# --- Check for Python 3.11 ---
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 is not installed. Please install it before continuing."
    exit 1
fi

# --- Create virtual environment ---
if [ ! -d "venv" ]; then
    echo "Creating virtual environment (Python 3.11)..."
    python3.11 -m venv venv
else
    echo "Virtual environment already exists. Skipping creation."
fi

# --- Upgrade pip ---
echo "Upgrading pip..."
./venv/bin/pip install --upgrade pip

# --- Install dependencies ---
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    ./venv/bin/pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

# --- Finish ---
echo ""
echo "Setup complete!"
echo "To activate the virtual environment, run:"
echo "source venv/bin/activate"
