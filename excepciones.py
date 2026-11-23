"""
excepciones.py
==============
Jerarquía de excepciones personalizadas de Software FJ.

¿Por qué una jerarquía?
-----------------------
Todas las excepciones heredan de `ErrorSoftwareFJ`. Así, el código que las
captura puede elegir entre:
  * `except ClienteInvalidoError`  -> manejar un error específico, o
  * `except ErrorSoftwareFJ`       -> manejar CUALQUIER error propio del sistema.
Esto permite distinguir los errores del negocio de los errores inesperados
de Python (ZeroDivisionError, TypeError, etc.).
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base del sistema: de ella derivan todas las demás."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de cliente inválidos, o cliente duplicado/inexistente."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Falta un parámetro obligatorio (None o cadena vacía)."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Parámetros inválidos al crear o usar un servicio (tarifa, capacidad...)."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio existe, pero en este momento no se puede reservar."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """La reserva no pudo crearse o procesarse."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se intentó una transición de estado ilegal (p. ej. cancelar algo ya procesado)."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """El cálculo de costos arrojó un valor imposible (NaN, infinito, negativo...)."""
