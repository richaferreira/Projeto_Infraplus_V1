import json

from backend.app.notifications import NotificationBus


def test_publish_subscribe():
    bus = NotificationBus()
    q = bus.subscribe()
    bus.publish('test', {'key': 'value'})
    payload = q.get_nowait()
    data = json.loads(payload)
    assert data['type'] == 'test'
    assert data['data']['key'] == 'value'
    bus.unsubscribe(q)


def test_multiple_subscribers():
    bus = NotificationBus()
    q1 = bus.subscribe()
    q2 = bus.subscribe()
    bus.publish('hello', {})
    assert not q1.empty()
    assert not q2.empty()
    bus.unsubscribe(q1)
    bus.unsubscribe(q2)


def test_unsubscribe():
    bus = NotificationBus()
    q = bus.subscribe()
    bus.unsubscribe(q)
    bus.publish('test', {})
    assert q.empty()
