"""
servicios.py
============
Define la clase abstracta `Servicio` y tres servicios especializados:
  * ReservaSala    -> reserva de salas de reuniones
  * AlquilerEquipo -> alquiler de equipos tecnológicos
  * Asesoria       -> asesorías especializadas

Conceptos de POO que se aplican aquí:
  * ABSTRACCIÓN   : Servicio define QUÉ debe hacer todo servicio.
  * HERENCIA      : las tres clases hijas reutilizan el código de Servicio.
  * POLIMORFISMO  : cada hija SOBRESCRIBE los métodos abstractos con su
                    propia lógica; se puede llamar a `servicio.calcular_costo()`
                    sin saber de qué tipo concreto es.
  * SOBRECARGA    : `calcular_costo` acepta distintas combinaciones de
                    argumentos (Python no tiene sobrecarga nativa, se simula).
"""
import math
from abc import abstractmethod

from entidades import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)

# IVA aplicado por defecto cuando no se indica otro impuesto.
IVA_DEFAULT = 0.19

# Códigos promocionales válidos y su porcentaje de descuento.
CODIGOS_DESCUENTO = {"PROMO10": 0.10, "PROMO20": 0.20}


class Servicio(EntidadBase):
    """
    Clase ABSTRACTA de la que heredan todos los servicios.

    Guarda lo común (nombre, tarifa, disponibilidad) y obliga a las hijas a
    implementar lo que cambia entre servicios (costo base, validación y
    descripción).
    """

    def __init__(self, id_servicio: int, nombre=None, tarifa_hora=None):
        super().__init__(id_servicio)

        # Validación 1: el nombre es obligatorio.
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("El servicio requiere un nombre")

        # Validación 2: la tarifa debe ser número positivo.
        # (bool es subclase de int en Python, por eso se descarta explícitamente)
        if not isinstance(tarifa_hora, (int, float)) or isinstance(tarifa_hora, bool) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r}")

        self._nombre = str(nombre).strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True  # todo servicio nuevo nace disponible

    # Propiedades de solo lectura (encapsulación).
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, valor: bool):
        """Única vía autorizada para habilitar/deshabilitar el servicio."""
        self._disponible = bool(valor)

    # ------------------------------------------------------------------
    # MÉTODOS ABSTRACTOS: cada servicio los implementa a su manera
    # ------------------------------------------------------------------
    @abstractmethod
    def calcular_costo_base(self, horas: float) -> float:
        """Costo del servicio SIN impuestos ni descuentos."""

    @abstractmethod
    def validar_parametros(self, horas: float) -> None:
        """Valida los parámetros propios del servicio; lanza excepción si hay error."""

    # ------------------------------------------------------------------
    # MÉTODO SOBRECARGADO
    # ------------------------------------------------------------------
    def calcular_costo(self, horas, *args) -> float:
        """
        Calcula el costo final. Variantes (sobrecarga simulada con *args):

            calcular_costo(h)                       -> base + IVA por defecto (19%)
            calcular_costo(h, 0.08)                 -> base + impuesto personalizado
            calcular_costo(h, "PROMO10")            -> base con código de descuento + IVA
            calcular_costo(h, 0.08, 0.15)           -> impuesto y descuento numéricos
            calcular_costo(h, 0.08, "PROMO20")      -> impuesto numérico y código

        Fórmula:  total = costo_base * (1 - descuento) * (1 + impuesto)
        """
        impuesto, descuento = IVA_DEFAULT, 0.0

        # --- Despacho según la cantidad y el tipo de argumentos recibidos ---
        if len(args) == 1:
            if isinstance(args[0], str):
                descuento = args[0]      # un texto -> es un código de descuento
            else:
                impuesto = args[0]       # un número -> es el impuesto
        elif len(args) == 2:
            impuesto, descuento = args   # (impuesto, descuento)
        elif len(args) > 2:
            raise ServicioInvalidoError("Demasiados argumentos para calcular_costo")

        # Si el descuento llegó como código, se traduce a porcentaje.
        if isinstance(descuento, str):
            try:
                descuento = CODIGOS_DESCUENTO[descuento.upper()]
            except KeyError:
                # `from None` oculta el KeyError interno: al usuario le basta
                # con nuestro mensaje claro.
                raise ServicioInvalidoError(f"Código de descuento desconocido: {descuento!r}") from None

        # Validaciones de rango para evitar cálculos absurdos.
        if not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError(f"Impuesto fuera de rango [0,1]: {impuesto!r}")
        if not isinstance(descuento, (int, float)) or not 0 <= descuento < 1:
            raise CalculoInconsistenteError(f"Descuento fuera de rango [0,1): {descuento!r}")

        # Cada servicio valida lo suyo (polimorfismo) y calcula su costo base.
        self.validar_parametros(horas)
        total = self.calcular_costo_base(horas) * (1 - descuento) * (1 + impuesto)

        # Verificación final de coherencia del resultado.
        if math.isnan(total) or math.isinf(total) or total <= 0:
            raise CalculoInconsistenteError(f"Costo calculado inconsistente: {total}")
        return round(total, 2)

    def _validar_horas(self, horas):
        """Validación común de duración, reutilizada por las clases hijas."""
        if not isinstance(horas, (int, float)) or isinstance(horas, bool) or not 0 < horas <= 24:
            raise ServicioInvalidoError(f"Duración inválida (0-24 h): {horas!r}")


class ReservaSala(Servicio):
    """Servicio 1: sala de reuniones con capacidad máxima de asistentes."""

    def __init__(self, id_servicio, nombre=None, tarifa_hora=None, capacidad=None, asistentes=1):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad
        self._asistentes = asistentes

    def validar_parametros(self, horas):
        # SOBRESCRIBE el método abstracto: valida duración y aforo.
        self._validar_horas(horas)
        if not isinstance(self._asistentes, int) or not 0 < self._asistentes <= self._capacidad:
            raise ServicioInvalidoError(
                f"Asistentes ({self._asistentes}) exceden la capacidad ({self._capacidad})"
            )

    def calcular_costo_base(self, horas):
        # Costo simple: tarifa por hora * horas.
        return self._tarifa_hora * horas

    def describir(self):
        return f"Sala '{self.nombre}' (cap. {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Servicio 2: alquiler de equipos, con cantidad de unidades y seguro opcional."""

    def __init__(self, id_servicio, nombre=None, tarifa_hora=None, cantidad=1, seguro=0.0):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioInvalidoError(f"Cantidad inválida: {cantidad!r}")
        if not isinstance(seguro, (int, float)) or seguro < 0:
            raise ServicioInvalidoError(f"Seguro inválido: {seguro!r}")
        self._cantidad = cantidad
        self._seguro = float(seguro)

    def validar_parametros(self, horas):
        self._validar_horas(horas)

    def calcular_costo_base(self, horas):
        # Tarifa * horas * unidades, más el seguro (cargo fijo).
        return self._tarifa_hora * horas * self._cantidad + self._seguro

    def describir(self):
        return f"Equipo '{self.nombre}' x{self._cantidad} - ${self._tarifa_hora:,.0f}/h (+seguro ${self._seguro:,.0f})"


class Asesoria(Servicio):
    """Servicio 3: asesoría cuyo precio depende del nivel del asesor."""

    # Multiplicador de tarifa según el nivel (atributo de clase compartido).
    _NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, id_servicio, nombre=None, tarifa_hora=None, nivel="junior"):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if str(nivel).lower() not in self._NIVELES:
            raise ServicioInvalidoError(f"Nivel de asesor inválido: {nivel!r}")
        self._nivel = str(nivel).lower()

    def validar_parametros(self, horas):
        self._validar_horas(horas)
        # Regla propia de este servicio: duración mínima de 1 hora.
        if horas < 1:
            raise ServicioInvalidoError("La asesoría requiere mínimo 1 hora")

    def calcular_costo_base(self, horas):
        return self._tarifa_hora * horas * self._NIVELES[self._nivel]

    def describir(self):
        return f"Asesoría '{self.nombre}' nivel {self._nivel} - ${self._tarifa_hora:,.0f}/h"
