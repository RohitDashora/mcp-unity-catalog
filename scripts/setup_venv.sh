#!/bin/bash

# This script creates a virtual environment named 'mcp', activates it,
# and installs the required packages from code/requirements.txt.

# The name of the virtual environment
VENV_NAME="mcp"

# The path to the requirements.txt file
REQUIREMENTS_FILE="code/requirements.txt"

# Check if the virtual environment directory already exists
if [ -d "$VENV_NAME" ]; then
    echo "Virtual environment '$VENV_NAME' already exists."
else
    echo "Creating virtual environment '$VENV_NAME'..."
    python3 -m venv "$VENV_NAME"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        exit 1
    fi
fi

# Activate the virtual environment
source "$VENV_NAME/bin/activate"
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

echo "Virtual environment activated."
echo "Installing requirements from $REQUIREMENTS_FILE..."

# Install the required packages
pip install -r "$REQUIREMENTS_FILE"
if [ $? -ne 0 ]; then
    echo "Failed to install requirements."
    exit 1
fi

echo "Requirements installed successfully."
echo "You can now run your scripts in the '$VENV_NAME' environment."
echo "To deactivate the environment, run: deactivate"
