from queue import PriorityQueue
from threading import Thread, Event
from typing import Callable
import time
from core.signal import Signal


class SignalManager:
    def __init__(self, handler: Callable[[Signal], None]):
        self.queue = PriorityQueue()
        self.running = Event()
        self.running.set()
        self.handler = handler  # Fonction de traitement du signal
        self.worker_thread = Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def send_signal(self, signal: Signal, priority: int = 10):
        self.queue.put((priority, signal))
        print(f"[SignalManager] Signal ajouté: {signal.id} avec priorité {priority}")

    def _worker_loop(self):
        while self.running.is_set():
            if self.queue.empty():
                time.sleep(0.05)
                continue

            priority, signal = self.queue.get()
            print(f"[SignalManager] Traitement signal: {signal.id} avec priorité {priority}")
            try:
                self.handler(signal)
            except Exception as e:
                print(f"[SignalManager] Erreur pendant le traitement du signal: {e}")

    def stop(self):
        self.running.clear()
        self.worker_thread.join()
