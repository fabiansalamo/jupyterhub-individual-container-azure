#!/bin/bash

# read parameters

if [ -z "$vm_domain_name" ]; then
  echo "Please provide a vm_domain_name, this is used to request a ssl cert:"
      read -s vm_domain_name
      vm_domain_name=${vm_domain_name:-""}
      if [ -z "$vm_domain_name" ]; then
          echo "vm_domain_name cannot be empty, exiting..."
          exit 1
      fi
fi

# install dependencies in the host machine

# install Docker
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# install Certbot
sudo apt-get update && sudo apt-get install -y certbot

# get a new certificate 
certbot certonly --standalone --non-interactive --agree-tos --email fabian278@gmail.com --domains $vm_domain_name


