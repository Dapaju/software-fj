"""
entidades.py
============
Contiene:
  * EntidadBase -> clase ABSTRACTA que representa cualquier entidad general
                   del sistema (clientes, servicios, reservas).
  * Cliente     -> entidad concreta con datos personales ENCAPSULADOS
                   y validaciones estrictas.
"""
import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError, ParametroFaltanteError


class EntidadBase(ABC):
    """
    ABSTRACCIÓN: define lo mínimo que toda entidad del sistema debe tener.

    Al heredar de ABC y tener un método abstracto, esta clase NO se puede
    instanciar directamente (EntidadBase() lanzaría TypeError); solo sirve
    como contrato para sus clases hijas.
    """

    def __init__(self, id_entidad: int):
        # Un guion bajo (_id) indica "atributo protegido": no se debe tocar
        # desde fuera de la clase ni de sus hijas.
        self._id = id_entidad

    @property
    def id(self) -> int:
        """Solo lectura: el id no se puede modificar una vez creado."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada clase hija DEBE implementar su propia descripción (polimorfismo)."""

    def __str__(self) -> str:
        # print(objeto) usará automáticamente la descripción de la clase hija.
        return self.describir()


class Cliente(EntidadBase):
    """
    Cliente de Software FJ.

    ENCAPSULACIÓN: los datos personales se guardan en atributos PRIVADOS
    (doble guion bajo: __nombre, __email...). Solo se acceden mediante
    `property`; cada setter valida el dato antes de guardarlo, de modo que
    es imposible que un objeto Cliente exista con datos inválidos.
    """

    # Expresión regular para validar el formato básico de un email:
    # texto@dominio.ext (compilada una sola vez, compartida por la clase).
    _EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, id_cliente: int, nombre=None, documento=None, email=None, telefono=None):
        super().__init__(id_cliente)  # inicializa el id en la clase padre
        # Estas asignaciones NO escriben directamente: invocan los setters
        # de abajo, que validan. Si algo falla, se lanza una excepción y el
        # objeto nunca llega a crearse.
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    @staticmethod
    def _requerido(valor, campo):
        """Verifica que el parámetro exista (no None ni cadena vacía)."""
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise ParametroFaltanteError(f"Falta el parámetro obligatorio: {campo}")
        return valor

    # ---------------- nombre ----------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._requerido(valor, "nombre")
        # Debe ser texto, tener al menos 3 caracteres y no contener números.
        if not isinstance(valor, str) or len(valor.strip()) < 3 or any(c.isdigit() for c in valor):
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r}")
        # Se normaliza: sin espacios sobrantes y con formato "Nombre Apellido".
        self.__nombre = valor.strip().title()

    # ---------------- documento ----------------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        valor = str(self._requerido(valor, "documento")).strip()
        # Solo dígitos, entre 6 y 12 caracteres.
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError(f"Documento inválido (6-12 dígitos): {valor!r}")
        self.__documento = valor

    # ---------------- email ----------------
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = self._requerido(valor, "email")
        if not isinstance(valor, str) or not self._EMAIL.match(valor.strip()):
            raise ClienteInvalidoError(f"Email inválido: {valor!r}")
        self.__email = valor.strip().lower()  # los emails se guardan en minúscula

    # ---------------- teléfono ----------------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(self._requerido(valor, "teléfono")).strip()
        if not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido (7-10 dígitos): {valor!r}")
        self.__telefono = valor

    def describir(self) -> str:
        """Implementación concreta del método abstracto de EntidadBase."""
        return f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | {self.email}"
