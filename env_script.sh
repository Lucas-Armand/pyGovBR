#!/bin/bash
# Esse script foi construido para preparacao do ambiente de trabalho do projeto
# "PyGov". Ele trata da Instalção das ferramentas listadas a seguir e foi
# desenvolvido para um sistema Ubunto 16.4 (mas deve funcionar para versões
# mais atuais).
## Anaconda (3.6.5) 
## Mongo (4.0.0) 
## Conda Enveriment
## pymongo (3.8.0) 
## Django (2.0.7) 
## djongo (1.2.29)
## git (X)
## Clone Github Project

# Install Anaconda:
wget "https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh"
bash ./Anaconda3-5.2.0-Linux-x86_64.sh -b

# Install Mongo:
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongod start

# Criando Ambiente no Conda:
conda create --name caranda -y

# Acessando Ambiente Caranda
source activate caranda

# Install pip3
sudo apt-get install python3-pip -y
pip3 install --upgrade pip

# Instal PyMongo
sudo pip3 install pymongo

# Install Django
pip3 install Django

# Install Djongo
pip3 install djongo

# Cloning Project:
git clone https://github.com/Lucas-Armand/pyGovBR.git

# Executing mongod
sudo service mongod start

# Executando Django
cd pyGovBR/PubMark
python manage.py runserver



