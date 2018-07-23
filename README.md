# Carandá Analitycs - WebScrapping, Data Exploring e Machine Learning em Compras Públicas

O objetivo desse projeto é construir uma ferramenta que possa auxiliar as empresas a participarem das licitações de forma mais efetiva. O estudo do mercado nos mostrou duas grandes barreira para pequenas empresas. A primeira barreira de é barreira de conhecimento. Para isso estamos desenvolvendo ferramentas (Carandá Analytics) que auxiliem o empreendedor entender quais são as características do mercado que ele quer atuar e o ajudem a tomar decisão mais assertivas. A segunda barreira é a burocrática. Para isso desenvolvemos ferramentas (Carandá Bots) de automação das etapas da licitação (cadastramento, busca de oportunidade, participação do certame) para diminuir a desvantagem do pequeno empreendedor para com o grande empreendedor (que tem uma equipe de compras públicas).

## Ferramentas

* Anaconda (3.6.5) 
* Mongo (4.0.0) 
* pymongo (3.8.0) 
* Django (2.0.7) 
* djongo (1.2.29)
* git
# Montando o Ambiente

Um rápido tutorial para começar a trabalhar no projeto. !!!Atenção!!! Precisa ser testado.

## Usando bash

A maneira mais fácil de fazer instalação de todas as ferramentas nas versões corretas e criar o ambiente virtual é executando o script [bash](https://github.com/Lucas-Armand/pyGovBR/blob/master/env_script.sh) na raiz (Ubuntu 16.04):

```
sudo bash env_script.sh
```

## Manualmente:

### Install Anaconda:

```
get "https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh"
bash ./Anaconda3-5.2.0-Linux-x86_64.sh -b

```
### Install Mongo:

```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```

### Criando Ambiente no Conda:

```
conda create --name caranda -y
```

### Acessando Ambiente Caranda

```
source activate caranda
```

### Install pip3

```
sudo apt-get install python3-pip
pip3 install --upgrade pip
```

### Instal PyMongo

```
sudo pip3 install pymongo
```

### Install Django

```
pip3 install Django
```

### Install Djongo

```
pip3 install djongo
```

### Cloning Project:

```
git clone https://github.com/Lucas-Armand/pyGovBR.git
```

### Executing mongod

```
sudo service mongod start
```

### Executando Django

```
cd pyGovBR/PubMark
python manage.py runserver
```
# Organização do Projeto

O projeto Carandá Analytics é dividido em tuas partes principais, Capitação de Dados e API de Dados + Analytics.

### Capitação de dados - WebScraping e WebCrawling

O primeiro desafio do projeto é a construção de uma base de dados que seja representativa dos fornecedores que desejamos analizar. Isso sigifica quem alem de integrar o projeto as principais API é necessário ter caplaridade para acessar os diversos portais de prefeituras, empresas estatais e etc. A proposta inicial é que os acessos dos usuários aos portais e API sejam armazenados e isso alimente o banco de dados.

No futuro deve-se existir um manual de como integrar um novo portal á plataforma. 

Uma lista das bases de dados já sincronizadas até agora:

- [x] API de dados do Governo
- [ ] API do Estado de São Paulo

### API de Dados e Anlytics - MongoDB e BI

O segundo desafio é, uma vez que se forme uma base de dados, disponibilizar o acesso desses dados para os usuários e fazer isso de maneira a garantir a intregação desses dados com outras bibliotecas python. Alem disso produzir alguns relatóŕios automáticos usando a própria API.

No futuro devemos ter um passo a passo de como gerar as primeiras visualizações de dados

- [ ] DashBorad de Compras públicas 
- [ ] Mapa de Oporunidades Futuras
- [ ] Rede de Mercado

## Sistema Proposto:

A seguir segue o rascunho de como seria o sistema que pensamos durante o nosso pequeno "braimstorm". A figura representa o (de forma bem básica) o fluxo de informação dentro do sistema e os "codigos" aonde as informações serão processadas, tambem divide a parte que seria referente á API de dados (usuário comum) e a parte referente ao WebScrapping (usuário desenvolvedor). Ela também sinaliza quais partes do trabalho estão mais relacionadas as principais ferramentas do projeto (Django, Mongo e Bilbiotecas de Dados do Python).

![rascunho do sistema](https://github.com/Lucas-Armand/pyGovBR/blob/master/img/rascunho_caranda.jpeg)

# Referências:

lista de referências utilizadas durante o aprendizado e/ou para cosultas futuras das feramentas utilixadas no projeto:
mongo:
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/#start-mdb-edition-from-the-command-interpreter
http://jordankobellarz.github.io/mongodb/2015/08/15/mentiras-que-lhe-contaram-sobre-o-mongodb.html
https://blog.umbler.com/br/boas-praticas-com-mongodb/
https://nesdis.github.io/djongo/different-ways-to-integrate-django-with-mongodb/
https://www.irit.fr/publis/SIG/2015_DAWAK_CEKTT.pdf
http://www.academia.edu/16859114/Benchmark_for_OLAP_on_NoSQL_Technologies_Comparing
Django
https://www.quora.com/How-can-I-use-MongoDB-and-a-relational-RDBMS-in-my-Django-website
https://djangobook.com/model-view-controller-design-pattern/
https://docs.djangoproject.com/en/2.0/intro/tutorial01/
pycharm
https://www.jetbrains.com/help/pycharm-edu/adding-existing-virtual-environment.html
py
https://www.fullstackpython.com/enterprise-python.html
