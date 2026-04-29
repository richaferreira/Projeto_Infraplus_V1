import json
import queue
import threading
import time


class NotificationBus:
    """Simple in-memory SSE notification hub."""

    def __init__(self):
        self._listeners = []
        self._lock = threading.Lock()

    def subscribe(self):
        q = queue.Queue(maxsize=50)
        with self._lock:
            self._listeners.append(q)
        return q

    def unsubscribe(self, q):
        with self._lock:
            try:
                self._listeners.remove(q)
            except ValueError:
                pass

    def publish(self, event_type, data):
        payload = json.dumps({'type': event_type, 'data': data, 'ts': time.time()})
        with self._lock:
            snapshot = list(self._listeners)
        dead = []
        for q in snapshot:
            try:
                q.put_nowait(payload)
            except queue.Full:
                dead.append(q)
        if dead:
            with self._lock:
                for q in dead:
                    try:
                        self._listeners.remove(q)
                    except ValueError:
                        pass


notification_bus = NotificationBus()
