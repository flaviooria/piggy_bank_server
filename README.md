# Piggy Bank API 🚀

# Índice

1. [Requisitos](#requisitos) 📚
2. [Instalación y configuración](#instalación-y-configuración) 🔧
3. [Ejecutar con docker](#ejecutar-con-docker) 🔥
4. [Variables de entorno](#variables-de-entorno) 🗒️

> [!NOTE] Si no deseas instalar python y ejecutar las dependencias solo sigue las instrucciones para ejecutar con
> docker. [Ejecutar con docker](#ejecutar-con-docker)

## Requisitos

- **Python 3.10**
- **Docker**

## Instalación y configuración

### Crear entorno virtual

```bash
python -m venv .venv
```

### Activar entorno virtual en linux o macos

```bash
source .venv/bin/activate
```

### Activar entorno virtual en windows

```bash
.\.venv\Scripts\activate
```

### Instalar dependencias con poetry

```bash
poetry install
```

```bash
poetry self add poetry-plugin-export
```

```bash
poetry export --without-hashes -f requirements.txt -o requirements.txt
```

### Instalar dependencias con pip

```bash
pip install -r requirements.txt
```

```bash
uvicorn account_managment.main:app --reload --host 0.0.0.0 --port 8000
```

## Ejecutar con docker

### Modo local

* ### Crear imagen de piggy bank server
```bash
docker build -t piggy_bank:lastest -f Dockerfile .
```

* ### Crear docker compose
```bash
docker compose up -d
```

### Modo desarrollo

* ### Usando Ngrok para exponer el servidor local

    * Ngrok es un servicio que nos crea un url público de manera segura enrutando a nuestro servidor local.

```bash
docker compose up -f docker-compose-ngrok.yml -d
```


### Modo producción

```bash
docker compose up -f docker-compose.production.yml -d
```


## Variables de entorno

> [!NOTE] Debeis de crear las variables de entorno a partir del ejemplo del fichero [".env.example"](.env.example), luego crear .env, .env.production y .env.development. Cada una de ellas tendra los valores de acuerdo a tus necesidades, pero son indispensables tenerlas creadas de lo contrario no se ejecutara el docker compose puesto que usan estos ficheros para cargar las variables de entorno en la aplicación.

> [!NOTE] Reemplazar POSTGRES_HOST por el nombre del servicio de tu base de datos que este establecida en el docker
> compose, en nuestro caso antes de ejecutar el docker compose en modo desarrollo reemplazarlo por ***POSTGRES_HOST=db***

- Crear los ficheros **.env** y **.env.prod**. ⬅️ 👀

### Modo desarrollo ".env"
```dotenv
POSTGRES_HOST=localhost
POSTGRES_USERNAME=root
POSTGRES_PASSWORD=root
POSTGRES_DBNAME=piggy_bank
POSTGRES_PORT=5432

PG_URI_DB=postgres://root:root@localhost:5432/piggy_bank

SECRET_KEY=03c14a18fd40931ffdb9fa5d71c031b5c898e22dd1fb872d3bb16cdad855eb85

APP_NAME="Piggy Bank"
API_VERSION="/api/v1"

EXPIRES_ACCESS_TOKEN="1 minutes"
EXPIRES_REFRESH_TOKEN="1 days"

SMTP_HOST=smtp.ethereal.email
SMTP_PORT=587
SMTP_USER=leo.medhurst@ethereal.email
SMTP_PASSWORD=8JCJZ33NjsTcR9qUgR
SMTP_SSL=false
SMTP_TLS=true

NGROK_AUTHTOKEN=2n1GeQAiXB65gLEiBm9ooGLpQqj_7B4KiiyA9udVwAVv8HqaK
ENVIRONMENT=local


PYTHONPATH=.
```

### Modo desarrollo ".env.development"
```dotenv
POSTGRES_HOST=db
POSTGRES_USERNAME=root
POSTGRES_PASSWORD=root
POSTGRES_DBNAME=piggy_bank
POSTGRES_PORT=5432

PG_URI_DB=postgres://root:root@db:5432/piggy_bank

SECRET_KEY=03c14a18fd40931ffdb9fa5d71c031b5c898e22dd1fb872d3bb16cdad855eb85

APP_NAME="Piggy Bank"
API_VERSION="/api/v1"

EXPIRES_ACCESS_TOKEN="1 days"
EXPIRES_REFRESH_TOKEN="1 days"

SMTP_HOST=smtp.ethereal.email
SMTP_PORT=587
SMTP_USER=leo.medhurst@ethereal.email
SMTP_PASSWORD=8JCJZ33NjsTcR9qUgR
SMTP_SSL=false
SMTP_TLS=true

NGROK_AUTHTOKEN=2n1GeQAiXB65gLEiBm9ooGLpQqj_7B4KiiyA9udVwAVv8HqaK
ENVIRONMENT=development

PYTHONPATH=.
```

### Modo producción ".env.prod"
```dotenv
POSTGRES_HOST=aws-0-eu-central-1.pooler.supabase.com
POSTGRES_USERNAME=postgres.vwjopmbnrgvcqdkjjshy
POSTGRES_PASSWORD=i2iAp_12flavio_laura
POSTGRES_DBNAME=postgres
POSTGRES_PORT=5432

PG_URI_DB=postgres://postgres.vwjopmbnrgvcqdkjjshy:i2iAp_12flavio_laura@aws-0-eu-central-1.pooler.supabase.com:5432/postgres

SECRET_KEY=03c14a18fd40931ffdb9fa5d71c031b5c898e22dd1fb872d3bb16cdad855eb85

APP_NAME="Piggy Bank"
API_VERSION="/api/v1"

EXPIRES_ACCESS_TOKEN="1 days"
EXPIRES_REFRESH_TOKEN="7 days"

# API URL
API_URL=https://piggy-bank-server-eg93.onrender.com/api/v1/docs

# Credentials api email with brevo.com
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=5cc410002@smtp-brevo.com
SMTP_PASSWORD=xsmtpsib-10a49ea97a8ed3c76ecd3a321cbb4a46818b59a4b46cabaa7b3fd0092fb5c1f9-fgkYm09Lt5shDqK3
SMTP_SSL=false
SMTP_TLS=true

ENVIRONMENT=production


PYTHONPATH=.
```
