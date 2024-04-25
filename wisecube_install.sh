#!/bin/bash
echo "Creating to env to install the wisecube stack..."
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required Python packages
pip install -r requirements.txt

echo ""
echo "Succesufluly create the python env!"
sleep 3
clear
# Run the Python script
python wisecube_install.py
installer_exit_code=$?
# Deactivate the virtual environment
deactivate

echo "Deleting the python env..."
rm -rf venv/
if [ $installer_exit_code -eq 0 ]; then
    echo "The wisecube stack is running now, check localhost:8000/dashboard "
else
    echo "Command failed with exit code $installer_exit_code."
fi
