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
## Actions
[![Create image server and push to dockerhub](https://github.com/flaviooria/piggy_bank_server/actions/workflows/deployment.yml/badge.svg?branch=develop)](https://github.com/flaviooria/piggy_bank_server/actions/workflows/deployment.yml)
