# Temporizador Pomodoro — TP Testing de Aplicaciones

![CI - Tests Pomodoro](https://github.com/TU_USUARIO/TU_REPO/actions/workflows/ci.yml/badge.svg)

Implementación de un temporizador Pomodoro con tests unitarios automatizados usando **pytest**.

## Estructura del proyecto

```
pomodoro-tp/
├── app/
│   ├── __init__.py
│   └── pomodoro_timer.py     # Lógica del timer (sin UI ni hilos)
├── tests/
│   ├── __init__.py
│   └── test_pomodoro_timer.py
├── resources/
│   └── test_data.json        # Datos para data-driven testing
├── reports/                  # Generado automáticamente por pytest
├── main.py                   # Demo por consola (no se testea)
├── requirements.txt
├── pytest.ini
└── README.md
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar los tests

```bash
# Corre todos los tests y genera el reporte HTML en reports/report.html
pytest

# Salida detallada (verbose)
pytest -v

# Solo un test específico
pytest tests/test_pomodoro_timer.py::test_timer_finaliza_al_llegar_a_cero -v
```

El reporte HTML se genera automáticamente en `reports/report.html`.

## Demo por consola

```bash
python main.py
```

## Tests incluidos

| # | Nombre | Tipo |
|---|--------|------|
| 1 | `test_iniciar_timer_descuenta_tiempo_correctamente` | Caso exitoso |
| 2 | `test_crear_timer_con_duracion_invalida_lanza_error` | Caso de error (parametrizado ×5) |
| 3 | `test_timer_finaliza_al_llegar_a_cero` | Edge case + callback |
| 4 | `test_pausar_y_reanudar_no_descuenta_durante_pausa` | Flujo de pausa |
| 5 | `test_alternancia_entre_modos_work_y_break` | Alternancia de ciclos |

## CI/CD

El pipeline de integración continua corre automáticamente en cada `push` y `pull_request` a `main` usando **GitHub Actions**.

**Qué hace el pipeline** (`.github/workflows/ci.yml`):
1. Checkout del código
2. Setup Python 3.11 con cache de pip
3. `pip install -r requirements.txt`
4. `pytest -v` — falla el job si algún test falla
5. Sube el reporte HTML como artifact (incluso si los tests fallaron)

**Cómo descargar el reporte HTML:**
1. Ir a la pestaña **Actions** del repositorio en GitHub
2. Hacer clic en la ejecución deseada
3. Al final de la página, en la sección **Artifacts**, descargar **pytest-report**
4. Descomprimir y abrir `report.html` en el navegador

> **Nota:** antes de hacer push, reemplazá `TU_USUARIO/TU_REPO` en el badge del README con el usuario y nombre real del repositorio.

## Decisiones de diseño

- `tick(seconds)` simula el paso del tiempo sin `time.sleep` ni hilos, lo que hace los tests **determinísticos e instantáneos**.
- El callback `on_finish` permite desacoplar efectos secundarios de la lógica del timer.
