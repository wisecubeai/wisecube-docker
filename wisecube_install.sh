#!/bin/bash


if [ "$1" == "--install" ]; then
    echo "Creating the env to install the wisecube stack..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    echo "Succesufluly create the python env!"
    sleep 3
    clear
    python wisecube_install.py
    installer_exit_code=$?
    deactivate
    echo "Deleting the python env..."
    rm -rf venv/
    if [ $installer_exit_code -eq 0 ]; then
        echo "The wisecube stack is running now, check http://localhost:8000/grafana"
    else
        echo "Command failed with exit code $installer_exit_code."
    fi
elif [ "$1" == "--uninstall" ]; then
    echo -e "Running the uninstall command will result in losing all the data from database\nand also delete:\n\t-networks\n\t-volumes\n"
    read -p "This changes are permannt, are you sure(yes/no): " choice
    if [ "$choice" == "yes" ]; then
        echo -e "$Uninstalling...\n"
        docker-compose -f docker-compose.yaml -p wisecube-stack down --volumes
        docker network rm wisecube-net
        docker volume rm wisecube_postgres_data
    fi
else
    echo -e "Usage: $0 \n\t--install (Create all the resources for the Wisecube Stack)\n\t--uninstall (Remove all resources)"
    exit 1
fi


