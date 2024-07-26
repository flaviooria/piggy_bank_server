# Piggy Bank API 🚀

# Índice

1. [Requisitos](#requisitos) 📚
2. [Instalación y configuración](#instalación-y-configuración) 🔧
3. [Ejecutar con docker](#ejecutar-con-docker) 🔥

> [!NOTE] Si no deseas instalar python y ejecutar las dependencias solo sigue las instrucciones para ejecutar con docker. [Ejecutar con docker](#ejecutar-con-docker)

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


