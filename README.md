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

### Instalar dependencias con pip

```bash
pip install -r requirements.txt
```

```bash
uvicorn account_managment.main:app --reload --host 0.0.0.0 --port 8000
```

### Instalar dependencias con poetry

```bash
poetry install
```

```bash
uvicorn account_managment.main:app --reload --host 0.0.0.0 --port 8000
```

## Ejecutar con docker

### Modo desarrollo

```bash
docker build -t piggy_bank:0.1.0 -f Dockerfile .
```

```bash
docker compose up -d 
```

### Modo producción

```bash
docker compose up -f docker-compose.production.yml -d
```

## Variables de entorno

> [!NOTE] Reemplazar DB_LOCALHOST por el nombre del servicio de tu base de datos que este establecida en el docker
> compose, en nuestro caso antes de ejecutar el docker compose en modo desarrollo reemplazarlo por ***DB_LOCALHOST=db***

- Crear los ficheros **.env** y **.env.prod**. ⬅️ 👀

### Modo desarrollo ".env"
```dotenv
DB_LOCALHOST=localhost
DB_USERNAME=admin
DB_PASSWORD=admin_pass
DB_NAME=account_manager_db
DB_PORT=5432
DB_URI=
DB_SCHEME=psycopg2
DB_MOTOR=postgres
APP_NAME='Piggy Bank'

POSTGRES_HOST=${DB_LOCALHOST}
POSTGRES_USERNAME=${DB_USERNAME}
POSTGRES_PASSWORD=${DB_PASSWORD}
POSTGRES_NAME=${DB_NAME}
POSTGRES_PORT=${DB_PORT}

SECRET_KEY=8d165e200c674ac4195c9b6bec3829c6d904a53679a0a6e0fd30d99b9a2aba04

# 1hour
EXPIRES_ACCESS_TOKEN='hours 1'

# 1day
EXPIRES_REFRESH_TOKEN='days 1'

# Credentials api email
SMTP_HOST=smtp.ethereal.email
SMTP_PORT=587
SMTP_USER=natalie24@ethereal.email
SMTP_PASSWORD=qhWmvemsKTzyCkgZdE
SMTP_SSL=false
SMTP_TLS=true
```
### Modo producción ".env.prod"
```dotenv
# Variables para que funcione la conexión a la db usada por el ORM
DB_LOCALHOST=eu-west-1.sql.xata.sh
DB_USERNAME=q4bqou
DB_PASSWORD=xau_IhOMiHq92MMpl34rubreWSXE28vTHvaC7
DB_NAME=piggy_bank:main
DB_PORT=5432
DB_SCHEME=psycopg2
DB_MOTOR=postgres

# Nombre de la api
APP_NAME='Piggy Bank'

# Variables para que funcione la conexión a la db
POSTGRES_HOST=${DB_LOCALHOST}
POSTGRES_USERNAME=${DB_USERNAME}
POSTGRES_PASSWORD=${DB_PASSWORD}
POSTGRES_NAME=${DB_NAME}
POSTGRES_PORT=${DB_PORT}

# Clave secreta para generar los token
# openssl rand -hex 32
SECRET_KEY=8d165e200c674ac4195c9b6bec3829c6d904a53679a0a6e0fd30d99b9a2aba04

# 1hour
EXPIRES_ACCESS_TOKEN='hours 1'

# 1day
EXPIRES_REFRESH_TOKEN='days 1'

# API URL 
API_URL=https://piggy-bank-server-eg93.onrender.com/api/v1/docs

# Credentials from xata.io hosting db
XATA_API_KEY=xau_IhOMiHq92MMpl34rubreWSXE28vTHvaC7
DATABASE_URL_POSTGRES=postgresql://q4bqou:xau_IhOMiHq92MMpl34rubreWSXE28vTHvaC7@eu-west-1.sql.xata.sh/piggy_bank:main?sslmode=require
DATABASE_URL=https://Flavio-Oria-s-workspace-q4bqou.eu-west-1.xata.sh/db/piggy_bank:main

# Credentials api email
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=5cc410001@smtp-brevo.com
SMTP_PASSWORD=xsmtpsib-10a49ea97a8ed3c76ecd3a321cbb4a46818b59a4b46cabaa7b3fd0092fb5c1f9-j2nXshI4wqKWU51H
```