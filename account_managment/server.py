import socket

import uvicorn

from account_managment.main import app  # noqa


def get_port_available(port: int = 8000) -> int:
    # Creamos un socket temporal
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Intentamos asignar el puerto preferido
        sock.bind(("", port))
        print(f"Puerto {port} está disponible.")
        port_available = port
    except OSError:
        # Si el puerto está ocupado, buscamos uno libre
        print(f"Puerto {port} está ocupado. Buscando un puerto libre...")
        sock.bind(("", 0))
        port_available = sock.getsockname()[1]

    # Cerramos el socket
    sock.close()

    return port_available


if __name__ == "__main__":
    port = get_port_available()
    print("Piggy Bank Server is running on port", port)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
