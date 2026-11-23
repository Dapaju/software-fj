"""
reserva.py
==========
Clase `Reserva`: integra un cliente, un servicio, una duración y un estado.

Ciclo de vida (máquina de estados):

    PENDIENTE --confirmar()--> CONFIRMADA --procesar()--> PROCESADA
        |                          |  \\--(error)--> FALLIDA
        +------cancelar()----------+
                   v
               CANCELADA

Las transiciones inválidas lanzan `OperacionNoPermitidaError`.
"""
from entidades import Cliente, EntidadBase
from excepciones import (
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from logger import log
from servicios import Servicio

# Constantes de estado (evitan errores de tipeo con cadenas sueltas).
PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA, FALLIDA = (
    "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA", "FALLIDA",
)


class Reserva(EntidadBase):
    def __init__(self, id_reserva, cliente, servicio, horas):
        super().__init__(id_reserva)

        # 1) Verificación de tipos: evita reservas con objetos incorrectos.
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido")

        # 2) El servicio debe estar disponible.
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible")

        # 3) Validación polimórfica: cada servicio valida a su manera.
        try:
            servicio.validar_parametros(horas)
        except ErrorSoftwareFJ as e:
            # ENCADENAMIENTO DE EXCEPCIONES: `from e` conserva el error original
            # como causa (__cause__). Se ve en el log y en el traceback.
            raise ReservaInvalidaError("Parámetros de reserva inválidos") from e

        self._cliente, self._servicio, self._horas = cliente, servicio, horas
        self._estado = PENDIENTE  # toda reserva nace pendiente
        self._costo = None        # se calcula al procesarla

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        """PENDIENTE -> CONFIRMADA (si el servicio sigue disponible)."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self._estado}")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' ya no está disponible")
        self._estado = CONFIRMADA
        log.info(f"Reserva #{self.id} confirmada")

    def cancelar(self):
        """Cancela la reserva, salvo que ya esté cancelada o procesada."""
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self._estado}")
        self._estado = CANCELADA
        log.info(f"Reserva #{self.id} cancelada")

    def procesar(self, *args):
        """
        CONFIRMADA -> PROCESADA calculando el costo final.

        Los `*args` se pasan tal cual a `calcular_costo` (sobrecarga):
            reserva.procesar()                  -> IVA por defecto
            reserva.procesar("PROMO10")         -> con descuento
            reserva.procesar(0.08, 0.1)         -> impuesto y descuento

        Demuestra el esquema completo try / except / else / finally.
        """
        try:
            # Zona de riesgo: puede lanzar cualquier ErrorSoftwareFJ.
            if self._estado != CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas CONFIRMADAS (actual: {self._estado})"
                )
            costo = self._servicio.calcular_costo(self._horas, *args)
        except ErrorSoftwareFJ as e:
            # Si falló mientras estaba confirmada, queda marcada como FALLIDA.
            if self._estado == CONFIRMADA:
                self._estado = FALLIDA
            # Se envuelve el error original con contexto (encadenamiento).
            raise ReservaInvalidaError(f"No se pudo procesar la reserva #{self.id}") from e
        else:
            # `else` se ejecuta SOLO si el try terminó sin errores.
            self._costo = costo
            self._estado = PROCESADA
            log.info(f"Reserva #{self.id} procesada. Costo total: ${costo:,.2f}")
            return costo
        finally:
            # `finally` se ejecuta SIEMPRE (con éxito o con error): ideal para
            # dejar constancia de que el intento terminó.
            log.info(f"Fin del intento de procesamiento de la reserva #{self.id} (estado: {self._estado})")

    def describir(self):
        costo = f" | Total: ${self._costo:,.2f}" if self._costo is not None else ""
        return (f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} ({self._horas} h){costo}")
