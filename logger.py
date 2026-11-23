"""
logger.py
=========
Configura el archivo de logs, que es la ÚNICA persistencia permitida
(no hay base de datos). Todos los eventos y errores del sistema se escriben
en `logs/software_fj.log`.

Se usa el módulo estándar `logging`, que ya incluye niveles de severidad:
  INFO     -> eventos normales (operación iniciada/terminada, reserva confirmada)
  ERROR    -> errores controlados del negocio (excepciones propias)
  CRITICAL -> errores inesperados (bugs, excepciones no previstas)
"""
import logging
import os

# Ruta absoluta del log, construida a partir de la ubicación de este archivo.
# Así funciona sin importar desde qué carpeta se ejecute el programa.
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Crea (una sola vez) y devuelve el logger de la aplicación."""
    logger = logging.getLogger("software_fj")

    # Si ya tiene handlers, ya fue configurado: lo devolvemos tal cual para
    # no duplicar cada línea del log al importar el módulo varias veces.
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Crea la carpeta `logs/` si todavía no existe (exist_ok evita error si ya está).
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)

    # El handler escribe en el archivo; encoding utf-8 para tildes y ñ.
    manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")

    # Formato de cada línea: fecha y hora | nivel | mensaje
    manejador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(manejador)
    return logger


# Instancia única que el resto de módulos importa: `from logger import log`
log = obtener_logger()
