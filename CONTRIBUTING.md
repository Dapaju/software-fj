# Guía de colaboración (equipo de 5)

## Ramas
- `main`: versión estable y entregable (protegida, solo por Pull Request).
- `develop`: integración del equipo.
- `feature/<modulo>`: una rama por integrante.

| Integrante | Rama | Módulos |
|---|---|---|
| 1 | `feature/excepciones-logger` | `excepciones.py`, `logger.py` |
| 2 | `feature/cliente` | `entidades.py` |
| 3 | `feature/servicio-abstracto` | `servicios.py` (clase `Servicio` y sobrecarga) |
| 4 | `feature/servicios-especializados` | `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| 5 | `feature/reserva-gestor` | `reserva.py`, `gestor.py`, `main.py` |

## Flujo
1. `git checkout develop && git pull`
2. `git checkout -b feature/<modulo>`
3. Commits pequeños con mensajes claros (`feat:`, `fix:`, `docs:`, `test:`).
4. `git push -u origin feature/<modulo>` y abrir Pull Request hacia `develop`.
5. Otro compañero revisa y aprueba; el CI debe estar en verde.
6. Al final, PR de `develop` a `main`.
