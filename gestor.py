"""
gestor.py
=========
`GestorSoftwareFJ` es el coordinador del sistema. Mantiene en memoria las
listas de clientes, servicios y reservas (NO hay base de datos) y ofrece
`ejecutar()`, un envoltorio que garantiza que ningún error detenga el programa.
"""
from entidades import Cliente
from excepciones import ClienteInvalidoError, ErrorSoftwareFJ, ReservaInvalidaError
from logger import log
from reserva import Reserva
from servicios import Servicio


class GestorSoftwareFJ:
    def __init__(self):
        # Listas internas: son la "base de datos en memoria" del sistema.
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []

    # ------------------------------------------------------------------
    # EJECUCIÓN SEGURA
    # ------------------------------------------------------------------
    def ejecutar(self, operacion, funcion, /, *args, **kwargs):
        """
        Ejecuta `funcion(*args, **kwargs)` protegiéndola con try/except/else/finally.

        - Si todo sale bien -> registra OK y devuelve el resultado.
        - Si falla con un error del negocio -> lo registra (con su causa
          encadenada), lo muestra y devuelve None.
        - Si falla con un error inesperado -> lo registra como CRITICAL y
          continúa igualmente.
        En ningún caso la excepción sube al programa principal, por lo que
        la aplicación permanece estable.

        (El `/` en la firma hace que `operacion` y `funcion` sean solo
        posicionales; así no chocan con kwargs como `nombre=`.)
        """
        log.info(f"INICIO operación: {operacion}")
        try:
            resultado = funcion(*args, **kwargs)
        except ErrorSoftwareFJ as e:
            # __cause__ contiene la excepción original si se usó `raise ... from`.
            causa = f" | causa: {type(e.__cause__).__name__}: {e.__cause__}" if e.__cause__ else ""
            log.error(f"{operacion} FALLÓ -> {type(e).__name__}: {e}{causa}")
            print(f"  [ERROR CONTROLADO] {type(e).__name__}: {e}"
                  + (f"\n      causa: {e.__cause__}" if e.__cause__ else ""))
            return None
        except Exception as e:  # red de seguridad para errores no previstos
            log.critical(f"{operacion} ERROR INESPERADO -> {type(e).__name__}: {e}")
            print(f"  [ERROR INESPERADO] {type(e).__name__}: {e}")
            return None
        else:
            log.info(f"{operacion} OK")
            print(f"  [OK] {resultado}")
            return resultado
        finally:
            log.info(f"FIN operación: {operacion}")

    # ------------------------------------------------------------------
    # REGISTROS
    # ------------------------------------------------------------------
    def registrar_cliente(self, **datos):
        """Crea un cliente (validado por su propia clase) y evita documentos repetidos."""
        cliente = Cliente(len(self._clientes) + 1, **datos)
        if any(c.documento == cliente.documento for c in self._clientes):
            raise ClienteInvalidoError(f"Ya existe un cliente con documento {cliente.documento}")
        self._clientes.append(cliente)
        return cliente

    def registrar_servicio(self, clase, **datos):
        """Crea un servicio de cualquier clase hija de Servicio (polimorfismo)."""
        servicio = clase(len(self._servicios) + 1, **datos)
        self._servicios.append(servicio)
        return servicio

    def crear_reserva(self, cliente, servicio, horas):
        """Crea una reserva; si algún objeto es None (registro previo fallido), lo rechaza."""
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("Cliente o servicio inexistente (None)")
        reserva = Reserva(len(self._reservas) + 1, cliente, servicio, horas)
        self._reservas.append(reserva)
        return reserva

    def resumen(self):
        """Imprime el estado final de todas las listas."""
        print("\n=== RESUMEN FINAL ===")
        print(f"Clientes: {len(self._clientes)} | Servicios: {len(self._servicios)} | Reservas: {len(self._reservas)}")
        for lista in (self._clientes, self._servicios, self._reservas):
            for item in lista:
                print(" -", item)  # usa __str__ -> describir() de cada clase
