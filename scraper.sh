#!/bin/bash

# Set the path to your Python script (use forward slashes or double backslashes for Windows)
PYTHON_SCRIPT="D:/KMAI3/EMB-DataWarehouse/scripts/telegram_scrapper.py"

# Set the path to your virtual environment (use forward slashes or double backslashes for Windows)
VENV_PATH="D:/KMAI3/EMB-DataWarehouse/.venv"

# Check if virtual environment exists
if [ -d "$VENV_PATH" ]; then
    # Activate the virtual environment (Windows)
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        source "$VENV_PATH/Scripts/activate"
    else
        source "$VENV_PATH/bin/activate"
    fi
fi

# Get the directory where the script is located
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)


# Construct the full path to the Python script
FULL_PATH_TO_PYTHON_SCRIPT="$SCRIPT_DIR/$PYTHON_SCRIPT"

# Execute the Python script
python "$FULL_PATH_TO_PYTHON_SCRIPT"

# Deactivate virtual environment if activated
if [ -d "$VENV_PATH" ]; then
    deactivate
fi