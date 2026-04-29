def test_home_page(client):
    r = client.get('/')
    assert r.status_code == 200
    assert b'InfraPlus' in r.data


def test_reports_open(client):
    r = client.get('/denuncias/abertas')
    assert r.status_code == 200


def test_reports_in_progress(client):
    r = client.get('/denuncias/andamento')
    assert r.status_code == 200


def test_reports_resolved(client):
    r = client.get('/denuncias/resolvidas')
    assert r.status_code == 200


def test_404_page(client):
    r = client.get('/pagina-inexistente')
    assert r.status_code == 404
    assert b'404' in r.data


def test_nearby_api(client):
    r = client.get('/api/nearby?lat=-22.0&lon=-43.0&radius=5')
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list)


def test_nearby_api_invalid_params(client):
    r = client.get('/api/nearby?lat=abc&lon=def')
    assert r.status_code == 400
