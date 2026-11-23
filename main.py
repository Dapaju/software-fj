"""
main.py
=======
Punto de entrada. Simula 12 bloques de operaciones (válidas e inválidas) para
demostrar que el sistema sigue funcionando aunque ocurran errores graves.

Convención: cada operación se envuelve en `g.ejecutar(...)`. Si falla, devuelve
None y el programa continúa con la siguiente.

Ejecutar con:  python main.py
"""
from gestor import GestorSoftwareFJ
from logger import RUTA_LOG, log
from servicios import Asesoria, AlquilerEquipo, ReservaSala


def main():
    g = GestorSoftwareFJ()
    log.info("===== INICIO DE SIMULACIÓN SOFTWARE FJ =====")

    # ---------- CLIENTES: casos válidos e inválidos ----------
    print("\n1) Cliente válido")
    ana = g.ejecutar("Registrar cliente Ana", g.registrar_cliente,
                     nombre="ana gómez", documento="1088123456", email="ana@correo.com", telefono="3101234567")

    print("\n2) Cliente inválido (email malo)")
    g.ejecutar("Registrar cliente Luis", g.registrar_cliente,
               nombre="Luis Pérez", documento="12345678", email="luis#correo", telefono="3009876543")

    print("\n3) Cliente con parámetro faltante (sin teléfono)")
    g.ejecutar("Registrar cliente Marta", g.registrar_cliente,
               nombre="Marta Ruiz", documento="99887766", email="marta@correo.com")

    print("\n4) Cliente válido (Carlos)")
    carlos = g.ejecutar("Registrar cliente Carlos", g.registrar_cliente,
                        nombre="Carlos Díaz", documento="55667788", email="carlos@fj.co", telefono="3205550000")

    print("\n5) Cliente duplicado (mismo documento que Ana)")
    g.ejecutar("Registrar cliente duplicado", g.registrar_cliente,
               nombre="Ana Copia", documento="1088123456", email="copia@correo.com", telefono="3101112222")

    # ---------- SERVICIOS: creación correcta e incorrecta ----------
    print("\n6) Servicio válido: sala")
    sala = g.ejecutar("Crear sala", g.registrar_servicio, ReservaSala,
                      nombre="Sala Innovación", tarifa_hora=50000, capacidad=10, asistentes=6)

    print("\n7) Servicio inválido: tarifa negativa")
    g.ejecutar("Crear equipo inválido", g.registrar_servicio, AlquilerEquipo,
               nombre="Proyector", tarifa_hora=-100, cantidad=1)

    print("\n8) Servicios válidos: equipo y asesoría")
    equipo = g.ejecutar("Crear equipo", g.registrar_servicio, AlquilerEquipo,
                        nombre="Portátil Pro", tarifa_hora=15000, cantidad=3, seguro=20000)
    asesoria = g.ejecutar("Crear asesoría", g.registrar_servicio, Asesoria,
                          nombre="Arquitectura de Software", tarifa_hora=80000, nivel="senior")

    # ---------- RESERVAS: exitosas y fallidas ----------
    print("\n9) Reserva exitosa + procesamiento con IVA por defecto")
    r1 = g.ejecutar("Reservar sala", g.crear_reserva, ana, sala, 3)
    g.ejecutar("Confirmar reserva 1", r1.confirmar)
    g.ejecutar("Procesar reserva 1", r1.procesar)  # 150.000 * 1.19 = 178.500

    print("\n10) Reserva fallida: duración inválida (error encadenado)")
    g.ejecutar("Reservar asesoría 0.5 h", g.crear_reserva, carlos, asesoria, 0.5)

    print("\n11) Reserva con descuento (sobrecarga) y servicio no disponible")
    r2 = g.ejecutar("Reservar equipo", g.crear_reserva, carlos, equipo, 4)
    g.ejecutar("Confirmar reserva 2", r2.confirmar)
    g.ejecutar("Procesar reserva 2 con PROMO10", r2.procesar, "PROMO10")
    equipo.cambiar_disponibilidad(False)  # se deshabilita el servicio
    g.ejecutar("Reservar equipo no disponible", g.crear_reserva, ana, equipo, 2)

    print("\n12) Operaciones no permitidas y cálculo inconsistente")
    g.ejecutar("Cancelar reserva ya procesada", r1.cancelar)
    r3 = g.ejecutar("Reservar asesoría", g.crear_reserva, ana, asesoria, 2)
    g.ejecutar("Confirmar reserva 3", r3.confirmar)
    g.ejecutar("Procesar reserva 3 con impuesto 5.0 (inválido)", r3.procesar, 5.0, 0.1)
    # Si un registro previo falló, la variable es None: el sistema lo detecta y sigue.
    g.ejecutar("Reserva sin cliente (None)", g.crear_reserva, None, sala, 2)

    g.resumen()
    log.info("===== FIN DE SIMULACIÓN =====")
    print(f"\nLog de errores y eventos: {RUTA_LOG}")


# Solo se ejecuta si el archivo se corre directamente (no si se importa).
if __name__ == "__main__":
    main()
