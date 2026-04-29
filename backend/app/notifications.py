import json
import queue
import time


class NotificationBus:
    """Simple in-memory SSE notification hub."""

    def __init__(self):
        self._listeners = []

    def subscribe(self):
        q = queue.Queue(maxsize=50)
        self._listeners.append(q)
        return q

    def unsubscribe(self, q):
        try:
            self._listeners.remove(q)
        except ValueError:
            pass

    def publish(self, event_type, data):
        payload = json.dumps({'type': event_type, 'data': data, 'ts': time.time()})
        dead = []
        for q in self._listeners:
            try:
                q.put_nowait(payload)
            except queue.Full:
                dead.append(q)
        for q in dead:
            self._listeners.remove(q)


notification_bus = NotificationBus()
