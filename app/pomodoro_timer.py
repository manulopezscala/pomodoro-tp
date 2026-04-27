"""Lógica del temporizador Pomodoro, 100% testeable sin hilos ni sleeps."""

from enum import Enum, auto
from typing import Callable, Optional


class State(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    FINISHED = auto()


class Mode(Enum):
    WORK = auto()
    BREAK = auto()


class PomodoroTimer:
    """Temporizador Pomodoro controlado por tick() para facilitar tests unitarios."""

    def __init__(self, work_duration: int, break_duration: int) -> None:
        """Inicializa el timer con duraciones en segundos.

        Args:
            work_duration: Duración del ciclo de trabajo en segundos.
            break_duration: Duración del ciclo de descanso en segundos.

        Raises:
            ValueError: Si alguna duración es <= 0.
        """
        if work_duration <= 0 or break_duration <= 0:
            raise ValueError("Las duraciones deben ser mayores a 0.")

        self._work_duration = work_duration
        self._break_duration = break_duration
        self._on_finish: Optional[Callable[[], None]] = None

        self.state: State = State.IDLE
        self.mode: Mode = Mode.WORK
        self.remaining: int = work_duration

    # ------------------------------------------------------------------
    # Propiedades internas
    # ------------------------------------------------------------------

    @property
    def _current_duration(self) -> int:
        """Duración total del modo activo."""
        return self._work_duration if self.mode == Mode.WORK else self._break_duration

    # ------------------------------------------------------------------
    # Interfaz pública
    # ------------------------------------------------------------------

    def set_on_finish(self, callback: Callable[[], None]) -> None:
        """Registra un callback que se invoca cuando el tiempo llega a 0."""
        self._on_finish = callback

    def start(self) -> None:
        """Inicia el timer. Si estaba FINISHED, reinicia con la duración del modo actual."""
        if self.state == State.FINISHED:
            self.remaining = self._current_duration
        self.state = State.RUNNING

    def pause(self) -> None:
        """Pausa el timer. Solo tiene efecto si está en RUNNING."""
        if self.state == State.RUNNING:
            self.state = State.PAUSED

    def resume(self) -> None:
        """Reanuda el timer. Solo tiene efecto si está en PAUSED."""
        if self.state == State.PAUSED:
            self.state = State.RUNNING

    def tick(self, seconds: int = 1) -> None:
        """Descuenta `seconds` del tiempo restante si el timer está RUNNING.

        Al llegar a 0: pasa a FINISHED, dispara on_finish y alterna el modo
        para el próximo ciclo.

        Args:
            seconds: Cantidad de segundos a descontar (por defecto 1).
        """
        if self.state != State.RUNNING:
            return

        self.remaining = max(0, self.remaining - seconds)

        if self.remaining == 0:
            self.state = State.FINISHED
            # Alternar modo para el próximo ciclo antes de notificar
            self.mode = Mode.BREAK if self.mode == Mode.WORK else Mode.WORK
            if self._on_finish is not None:
                self._on_finish()

    def format_remaining(self) -> str:
        """Retorna el tiempo restante con formato MM:SS."""
        minutes, secs = divmod(self.remaining, 60)
        return f"{minutes:02d}:{secs:02d}"
