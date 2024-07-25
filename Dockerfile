# Etapa 1: Construcción
FROM python:3.10-slim AS builder

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y los instala
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copia el código fuente de la aplicación
COPY . /app

# Etapa 2: Producción
FROM python:3.10-slim

# Establece las variables de entorno
ARG DB_URI
ARG DB_SCHEME=psycopg2
ARG DB_MOTOR=postgres
ARG APP_NAME="Piggy Bank"
ARG SECRET_KEY
ARG EXPIRES_ACCESS_TOKEN
ARG EXPIRES_REFRESH_TOKEN

# Establece el directorio de trabajo
WORKDIR /app

# Copia las dependencias desde la etapa de construcción
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia el código fuente de la aplicación
COPY --from=builder /app /app

# Copiar el wait-for-it.sh script
COPY ./wait-for-it.sh /app

# Permisos para el script de ejecución
RUN chmod +x /app/wait-for-it.sh

# Exponer el puerto que usará FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["/app/wait-for-it.sh", "db:5432", "--", "uvicorn", "account_managment.main:app", "--host", "0.0.0.0", "--port", "8000"]
