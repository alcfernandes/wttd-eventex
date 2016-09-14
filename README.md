# Eventex

Sistema de Eventos encomendado pela Morena.

[![Build Status](https://travis-ci.org/alcfernandes/wttd-eventex.svg?branch=master)](https://travis-ci.org/alcfernandes/wttd-eventex)
[![Code Health](https://landscape.io/github/alcfernandes/wttd-eventex/master/landscape.svg?style=flat)](https://landscape.io/github/alcfernandes/wttd-eventex/master)


## Como desenvolver?

1. Clone o repositório.
2. Crie um Virtualenv com Python 3.5.
3. Ative o Virtualenv.
4. Instale as dependências.
5. Configure a instância com o .env
6. Execute os testes.

```console
git clone https://github.com/alcfernandes/wttd-eventex.git wttd
cd wttd
python -m venv .wttd
source .wttd/bin/activate
pip install -r requerements-dev.txt
cp contrib/env-sample .env
python manage.py test

```

## Como fazer o deploy?

1. Crie uma instância no Heroku
2. Envie as configurações para o Heroku
3. Defina uma SECRET_key segura para a instância.
4. Defina DEBUG=False
5. Configure o serviço de e-mail
6. Envie o código para o Heroku.

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
# Configure o e-mail
git push heroku master --force
```
