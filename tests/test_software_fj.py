"""Pruebas unitarias de Software FJ (ejecutar: python -m unittest discover -s tests -v)."""
import os
import sys
import unittest

# Permite importar los módulos que están en la raíz del proyecto.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entidades import Cliente, EntidadBase
from excepciones import (CalculoInconsistenteError, ClienteInvalidoError, ErrorSoftwareFJ,
                         OperacionNoPermitidaError, ParametroFaltanteError, ReservaInvalidaError,
                         ServicioInvalidoError, ServicioNoDisponibleError)
from gestor import GestorSoftwareFJ
from reserva import CONFIRMADA, FALLIDA, PROCESADA, Reserva
from servicios import Asesoria, AlquilerEquipo, ReservaSala, Servicio


def cliente_valido():
    return Cliente(1, nombre="ana gomez", documento="1088123456", email="Ana@Correo.com", telefono="3101234567")


class TestAbstraccion(unittest.TestCase):
    def test_clases_abstractas_no_se_instancian(self):
        with self.assertRaises(TypeError):
            EntidadBase(1)
        with self.assertRaises(TypeError):
            Servicio(1, "x", 10)


class TestCliente(unittest.TestCase):
    def test_normaliza_datos(self):
        c = cliente_valido()
        self.assertEqual(c.nombre, "Ana Gomez")
        self.assertEqual(c.email, "ana@correo.com")

    def test_email_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente(1, "Luis Perez", "12345678", "luis#correo", "3009876543")

    def test_parametro_faltante(self):
        with self.assertRaises(ParametroFaltanteError):
            Cliente(1, "Marta Ruiz", "99887766", "m@c.com")

    def test_encapsulacion_name_mangling(self):
        self.assertFalse(hasattr(cliente_valido(), "nombre_privado"))
        with self.assertRaises(AttributeError):
            cliente_valido().id = 5  # id es solo lectura


class TestServicios(unittest.TestCase):
    def test_polimorfismo_costos(self):
        self.assertEqual(ReservaSala(1, "S", 50000, 10, 5).calcular_costo(3), 178500.0)
        self.assertEqual(AlquilerEquipo(2, "E", 15000, 3, 20000).calcular_costo(4, "PROMO10"), 214200.0)
        self.assertEqual(Asesoria(3, "A", 80000, "senior").calcular_costo(2, 0.0), 240000.0)

    def test_sobrecarga_variantes(self):
        s = ReservaSala(1, "S", 100000, 10)
        self.assertEqual(s.calcular_costo(1), 119000.0)             # IVA por defecto
        self.assertEqual(s.calcular_costo(1, 0.0), 100000.0)        # impuesto propio
        self.assertEqual(s.calcular_costo(1, 0.0, 0.5), 50000.0)    # impuesto + descuento
        self.assertEqual(s.calcular_costo(1, 0.0, "PROMO20"), 80000.0)

    def test_errores_de_calculo(self):
        s = ReservaSala(1, "S", 1000, 10)
        with self.assertRaises(CalculoInconsistenteError):
            s.calcular_costo(1, 5.0)
        with self.assertRaises(ServicioInvalidoError):
            s.calcular_costo(1, "NOEXISTE")
        with self.assertRaises(ServicioInvalidoError):
            s.calcular_costo(30)

    def test_creacion_invalida(self):
        with self.assertRaises(ServicioInvalidoError):
            AlquilerEquipo(1, "P", -100)
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala(1, "S", 100, 0)
        with self.assertRaises(ServicioInvalidoError):
            Asesoria(1, "A", 100, "novato")


class TestReserva(unittest.TestCase):
    def setUp(self):
        self.c = cliente_valido()
        self.s = Asesoria(1, "Arq", 80000, "senior")

    def test_flujo_exitoso(self):
        r = Reserva(1, self.c, self.s, 2)
        r.confirmar()
        self.assertEqual(r.estado, CONFIRMADA)
        r.procesar()
        self.assertEqual(r.estado, PROCESADA)

    def test_error_encadenado(self):
        with self.assertRaises(ReservaInvalidaError) as ctx:
            Reserva(1, self.c, self.s, 0.5)
        self.assertIsInstance(ctx.exception.__cause__, ServicioInvalidoError)

    def test_servicio_no_disponible(self):
        self.s.cambiar_disponibilidad(False)
        with self.assertRaises(ServicioNoDisponibleError):
            Reserva(1, self.c, self.s, 2)

    def test_transiciones_no_permitidas(self):
        r = Reserva(1, self.c, self.s, 2)
        with self.assertRaises(ReservaInvalidaError):  # procesar sin confirmar
            r.procesar()
        r.confirmar()
        r.procesar()
        with self.assertRaises(OperacionNoPermitidaError):
            r.cancelar()

    def test_procesar_fallido(self):
        r = Reserva(1, self.c, self.s, 2)
        r.confirmar()
        with self.assertRaises(ReservaInvalidaError):
            r.procesar(5.0)
        self.assertEqual(r.estado, FALLIDA)


class TestGestor(unittest.TestCase):
    def test_nunca_propaga_excepciones(self):
        g = GestorSoftwareFJ()
        self.assertIsNone(g.ejecutar("error de negocio", g.registrar_cliente, nombre="x"))
        self.assertIsNone(g.ejecutar("error inesperado", lambda: 1 / 0))
        self.assertIsNotNone(g.ejecutar("ok", lambda: 42))

    def test_cliente_duplicado(self):
        g = GestorSoftwareFJ()
        datos = dict(nombre="Ana Gomez", documento="1088123456", email="a@c.com", telefono="3101234567")
        g.registrar_cliente(**datos)
        with self.assertRaises(ClienteInvalidoError):
            g.registrar_cliente(**datos)

    def test_jerarquia_de_excepciones(self):
        for exc in (ClienteInvalidoError, ServicioInvalidoError, ReservaInvalidaError):
            self.assertTrue(issubclass(exc, ErrorSoftwareFJ))


if __name__ == "__main__":
    unittest.main()
