# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

POO en Python 3.9+, sin base de datos ni librerías externas. Solo se usa un archivo para logs (`logs/software_fj.log`).

## Ejecución
    python main.py

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`ErrorSoftwareFJ` y derivadas) |
| `logger.py` | Configuración del archivo de logs |
| `entidades.py` | `EntidadBase` (abstracta) y `Cliente` (encapsulación + validaciones) |
| `servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | `Reserva`: confirmar, cancelar, procesar (try/except/else/finally) |
| `gestor.py` | Listas internas y `ejecutar()`, que mantiene la app estable ante cualquier error |
| `main.py` | Simulación de 12 operaciones válidas e inválidas |

## Conceptos aplicados
- **Abstracción**: `EntidadBase`, `Servicio` (métodos abstractos `calcular_costo_base`, `validar_parametros`, `describir`).
- **Herencia y polimorfismo**: cada servicio sobrescribe costo, validación y descripción.
- **Encapsulación**: atributos privados con `property` y validación en los setters.
- **Sobrecarga**: `calcular_costo(horas, *args)` admite (), (impuesto), ("PROMO10"), (impuesto, descuento).
- **Excepciones**: personalizadas, `try/except/else/finally` en `Reserva.procesar` y `GestorSoftwareFJ.ejecutar`, encadenamiento con `raise ... from e`.
- **Logs**: cada evento y error queda registrado con fecha, nivel y causa original.

## Reparto sugerido (5 integrantes)
1. Excepciones y logger · 2. Cliente y EntidadBase · 3. Servicio abstracto y sobrecarga · 4. Servicios especializados · 5. Reserva, gestor y main.

## Pruebas
    python -m unittest discover -s tests -v

## GitHub
- CI automático (`.github/workflows/ci.yml`): corre las pruebas y la simulación en cada push/PR.
- Flujo de ramas y reparto en `CONTRIBUTING.md`.
- El archivo `logs/software_fj.log` se genera al ejecutar y no se versiona.
