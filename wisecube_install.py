import docker
import yaml
import os
import subprocess


POSTGRES_VOLUME = "wisecube_postgres_data"
WISECUBE_NETWORK="wisecube-net"
PROJECT_NAME="wisecube-stack"

docker_client = docker.from_env()


def create_docker_volume(volume_name):
    existing_volume = docker_client.volumes.list(filters={"name": volume_name})
    if existing_volume:
        print(f"Volume '{volume_name}' already exists.")
        return None
    
    docker_client.volumes.create(name=volume_name)
    print("Docker volume '{}' created successfully!".format(volume_name))


def create_docker_network(network_name):
    existing_networks = docker_client.networks.list(names=[network_name])
    if existing_networks:
        print(f"Network '{network_name}' already exists.")
        return
    docker_client.networks.create(name=network_name)
    print("Docker network '{}' created successfully!".format(network_name))

def update_docker_compose(apy_key):
    # Load the Docker Compose file
    with open('compose_template.yaml', 'r') as file:
        compose_data = yaml.safe_load(file)

    compose_data['services']['wisecube-pythia']['environment'] = ["OPENAI_API_KEY=" + apy_key]

    with open('docker-compose.yaml', 'w') as file:
        yaml.dump(compose_data, file)

def run_docker_compose(compose_file):
    compose_file = os.path.abspath(compose_file)
    try:
        result = subprocess.run(['docker-compose', '-f', compose_file,'-p', PROJECT_NAME, 'up', '-d'], capture_output=True, text=True, check=True)
        print(result)
        container_ids = [line.split()[1] for line in result.stderr.splitlines() if line.startswith('Creating')]
        print(set(container_ids))
        print("Docker Compose file is running.")
    except subprocess.CalledProcessError  as e:
        print("Failed to run Docker Compose file:", e)
        raise Exception("Failed to run Docker Compose file:", e)

def main():
    print("Configure the Wisecube Stack!")
    api_key = input("1. Enter your key: ")
    if api_key is None:
        raise Exception("No api key was provided!")
    
    create_docker_volume(POSTGRES_VOLUME)
    create_docker_network(WISECUBE_NETWORK)
    update_docker_compose(apy_key=api_key)
    run_docker_compose("docker-compose.yaml")


if __name__ == "__main__":
    main()
