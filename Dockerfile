#
FROM python:3.10-slim AS builder

# Establece el directorio de trabajo
WORKDIR /app

# instala poetry
RUN pip install poetry

# Copia el archivo de dependencias
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry self add poetry-plugin-export

# exporta las dependencias a un archivo requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# ejecuta pip install para instalar las dependencias
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copia el código fuente de la aplicación
COPY . /app


# Etapa 2: Producción
FROM python:3.10-slim

# Establece las variables de entorno
ARG DB_URI
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

# Exponer el puerto que usará FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "account_managment.main:app", "--host", "0.0.0.0", "--port", "8000"]
