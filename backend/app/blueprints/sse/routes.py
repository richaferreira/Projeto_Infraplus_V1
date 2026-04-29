import time

from flask import Blueprint, Response, stream_with_context
from flask_login import login_required

from backend.app.notifications import notification_bus

sse_bp = Blueprint('sse', __name__)


@sse_bp.route('/api/notifications/stream')
@login_required
def stream():
    def generate():
        q = notification_bus.subscribe()
        try:
            yield 'data: {"type":"connected"}\n\n'
            while True:
                try:
                    payload = q.get(timeout=30)
                    yield f'data: {payload}\n\n'
                except Exception:
                    yield ': keepalive\n\n'
        finally:
            notification_bus.unsubscribe(q)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        },
    )
