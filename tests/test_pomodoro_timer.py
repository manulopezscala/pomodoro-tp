"""Tests unitarios para PomodoroTimer — Trabajo Práctico Testing de Aplicaciones."""

import pytest

from app.pomodoro_timer import Mode, PomodoroTimer, State


# ===========================================================================
# 1. CASO EXITOSO — inicio y cuenta regresiva normal
# ===========================================================================

def test_iniciar_timer_descuenta_tiempo_correctamente():
    """El timer descuenta correctamente tras start() + tick(10)."""
    timer = PomodoroTimer(work_duration=1500, break_duration=300)

    timer.start()
    timer.tick(10)

    assert timer.remaining == 1490
    assert timer.state == State.RUNNING
    assert timer.mode == Mode.WORK


# ===========================================================================
# 2. CASO DE ERROR — duraciones inválidas con parametrize
# ===========================================================================

@pytest.mark.parametrize("work,break_dur", [
    (0, 300),
    (-1, 300),
    (1500, 0),
    (1500, -5),
    (0, 0),
])
def test_crear_timer_con_duracion_invalida_lanza_error(work, break_dur):
    """Constructor lanza ValueError para cualquier duración <= 0."""
    with pytest.raises(ValueError):
        PomodoroTimer(work_duration=work, break_duration=break_dur)


# ===========================================================================
# 3. EDGE CASE — el timer llega exactamente a cero
# ===========================================================================

def test_timer_finaliza_al_llegar_a_cero():
    """Al expirar: state=FINISHED, mode cambia a BREAK y se invoca on_finish."""
    timer = PomodoroTimer(work_duration=1, break_duration=1)

    callback_ejecutado = {"valor": False}

    def marcar_callback():
        callback_ejecutado["valor"] = True

    timer.set_on_finish(marcar_callback)
    timer.start()
    timer.tick(1)

    assert timer.remaining == 0
    assert timer.state == State.FINISHED
    assert timer.mode == Mode.BREAK          # modo alternado para el próximo ciclo
    assert callback_ejecutado["valor"] is True


# ===========================================================================
# 4. PAUSA — los ticks durante pausa no descuentan tiempo
# ===========================================================================

def test_pausar_y_reanudar_no_descuenta_durante_pausa():
    """Los ticks en estado PAUSED son ignorados; solo cuentan RUNNING."""
    timer = PomodoroTimer(work_duration=1500, break_duration=300)
    inicial = timer.remaining  # 1500

    timer.start()
    timer.tick(5)    # descuenta: 1495
    timer.pause()
    timer.tick(10)   # pausado: no descuenta
    timer.resume()
    timer.tick(3)    # descuenta: 1492

    assert timer.remaining == inicial - 8   # solo 5 + 3 = 8 segundos efectivos
    assert timer.state == State.RUNNING


# ===========================================================================
# 5. ALTERNANCIA DE MODOS — WORK → BREAK → WORK
# ===========================================================================

def test_alternancia_entre_modos_work_y_break():
    """Después de cada ciclo completo el modo alterna: WORK→BREAK→WORK."""
    timer = PomodoroTimer(work_duration=1, break_duration=1)

    # Primer ciclo: WORK expira → modo pasa a BREAK
    timer.start()
    timer.tick(1)
    assert timer.state == State.FINISHED
    assert timer.mode == Mode.BREAK

    # Segundo ciclo: start con BREAK → expira → modo vuelve a WORK
    timer.start()
    timer.tick(1)
    assert timer.state == State.FINISHED
    assert timer.mode == Mode.WORK
