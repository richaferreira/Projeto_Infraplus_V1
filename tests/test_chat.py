import json


def test_chat_page_loads(client):
    r = client.get('/chat')
    assert r.status_code == 200
    assert b'Assistente' in r.data


def test_chat_api_greeting(client, app):
    with app.app_context():
        r = client.post('/api/chat',
                        data=json.dumps({'message': 'oi'}),
                        content_type='application/json')
        assert r.status_code == 200
        data = r.get_json()
        assert 'ajudar' in data['reply'].lower() or 'olá' in data['reply'].lower()


def test_chat_api_help(client, app):
    with app.app_context():
        r = client.post('/api/chat',
                        data=json.dumps({'message': 'ajuda'}),
                        content_type='application/json')
        assert r.status_code == 200
        data = r.get_json()
        assert 'denúncias' in data['reply'].lower() or 'buscar' in data['reply'].lower()


def test_chat_api_stats(client, app):
    with app.app_context():
        r = client.post('/api/chat',
                        data=json.dumps({'message': 'resumo geral'}),
                        content_type='application/json')
        assert r.status_code == 200
        data = r.get_json()
        assert 'Total' in data['reply'] or 'total' in data['reply']


def test_chat_api_empty(client, app):
    with app.app_context():
        r = client.post('/api/chat',
                        data=json.dumps({'message': ''}),
                        content_type='application/json')
        assert r.status_code == 400
