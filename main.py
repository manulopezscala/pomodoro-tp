"""Demo de consola del temporizador Pomodoro. No forma parte del conjunto de tests."""

import time

from app.pomodoro_timer import Mode, PomodoroTimer, State

WORK_SECONDS = 25 * 60   # 25 minutos
BREAK_SECONDS = 5 * 60   # 5 minutos


def main() -> None:
    timer = PomodoroTimer(work_duration=WORK_SECONDS, break_duration=BREAK_SECONDS)

    def al_finalizar():
        modo = "DESCANSO" if timer.mode == Mode.BREAK else "TRABAJO"
        print(f"\n¡Tiempo! Próximo modo: {modo}")

    timer.set_on_finish(al_finalizar)

    print("=== Temporizador Pomodoro ===")
    print("Presioná Ctrl+C para detener.\n")

    timer.start()

    try:
        while timer.state != State.FINISHED:
            modo_label = "TRABAJO" if timer.mode == Mode.WORK else "DESCANSO"
            print(f"\r[{modo_label}] {timer.format_remaining()}", end="", flush=True)
            time.sleep(1)
            timer.tick(1)
    except KeyboardInterrupt:
        print("\nDemo interrumpido por el usuario.")


if __name__ == "__main__":
    main()
