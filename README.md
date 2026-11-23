# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Sistema orientado a objetos en **Python** para la empresa ficticia **Software FJ**, que ofrece reservas de salas, alquiler de equipos y asesorías especializadas.
Aplica **abstracción, herencia, polimorfismo y encapsulación**, con **manejo avanzado de excepciones**, sin base de datos: la información vive en objetos y listas, y el único archivo es el **log** de eventos y errores.

![CI](https://github.com/Dapaju/software-fj/actions/workflows/ci.yml/badge.svg)

## Características
- Clase abstracta general `EntidadBase` y clase `Cliente` con datos encapsulados y validaciones estrictas.
- Clase abstracta `Servicio` con tres servicios especializados: `ReservaSala`, `AlquilerEquipo` y `Asesoria`.
- `Reserva` con ciclo de vida: confirmar, cancelar y procesar.
- Cálculo de costos **sobrecargado** (impuestos, descuentos y códigos promocionales).
- Excepciones personalizadas, `try/except/else/finally` y encadenamiento con `raise ... from`.
- Registro de eventos y errores en `logs/software_fj.log`; la aplicación nunca se detiene por un error.
- Simulación de 12 bloques de operaciones válidas e inválidas.

## Requisitos
- Python 3.9 o superior (no requiere librerías externas).

## Instalación y ejecución
```bash
git clone https://github.com/Dapaju/software-fj.git
cd software-fj
python main.py
```
En Windows, si `python` no funciona, usa `py main.py`.

## Pruebas
```bash
python -m unittest discover -s tests -v
```
Incluye 17 pruebas unitarias. También se ejecutan automáticamente con GitHub Actions en cada push y Pull Request.

## Estructura del proyecto
```
software-fj/
├── main.py                 # Simulación de operaciones
├── gestor.py               # Listas internas y ejecución segura de operaciones
├── reserva.py              # Clase Reserva y sus estados
├── servicios.py            # Servicio (abstracta) + 3 servicios especializados
├── entidades.py            # EntidadBase (abstracta) y Cliente
├── excepciones.py          # Jerarquía de excepciones personalizadas
├── logger.py               # Configuración del archivo de logs
├── tests/                  # Pruebas unitarias
├── logs/                   # Aquí se genera software_fj.log
└── .github/workflows/      # Integración continua
```

## Conceptos de POO aplicados
| Concepto | Dónde se aplica |
|---|---|
| Abstracción | `EntidadBase` y `Servicio` con métodos abstractos |
| Herencia | `Cliente` y `Servicio` heredan de `EntidadBase`; los 3 servicios heredan de `Servicio` |
| Polimorfismo | Cada servicio sobrescribe `calcular_costo_base`, `validar_parametros` y `describir` |
| Encapsulación | Atributos privados de `Cliente` con `property` y validación en los setters |
| Sobrecarga | `calcular_costo(horas, *args)` admite varias combinaciones de argumentos |

## Ejemplo de uso
```python
from servicios import ReservaSala

sala = ReservaSala(1, "Sala Innovación", 50000, capacidad=10, asistentes=6)
sala.calcular_costo(3)                    # 178500.0  (IVA 19 % por defecto)
sala.calcular_costo(3, 0.0)               # 150000.0  (sin impuesto)
sala.calcular_costo(3, "PROMO10")         # 160650.0  (código de descuento + IVA)
sala.calcular_costo(3, 0.08, 0.15)        # impuesto 8 % y descuento 15 %
```

## Manejo de errores
| Excepción | Cuándo se lanza |
|---|---|
| `ClienteInvalidoError` | Datos de cliente inválidos o duplicados |
| `ParametroFaltanteError` | Falta un dato obligatorio |
| `ServicioInvalidoError` | Parámetros de servicio inválidos |
| `ServicioNoDisponibleError` | El servicio no está disponible |
| `ReservaInvalidaError` | La reserva no se puede crear o procesar |
| `OperacionNoPermitidaError` | Cambio de estado no permitido |
| `CalculoInconsistenteError` | Costo o porcentajes fuera de rango |

Todas heredan de `ErrorSoftwareFJ`. Ejemplo de línea del log:
```
2026-11-22 10:15:02 | ERROR    | Reservar asesoría 0.5 h FALLÓ -> ReservaInvalidaError: Parámetros de reserva inválidos | causa: ServicioInvalidoError: La asesoría requiere mínimo 1 hora
```

## Autor
**Diana Paola Espinosa** – Ingenieria de Sistemas / UNAD – 213023

## Referencias
- Python Software Foundation. (s. f.). *Python 3 documentation*. https://docs.python.org/3/
- Meyer, B. (1997). *Object-oriented software construction* (2.ª ed.). Prentice Hall.
