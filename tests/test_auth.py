def test_login_page_loads(client):
    r = client.get('/login')
    assert r.status_code == 200
    assert b'Login' in r.data or b'login' in r.data


def test_login_success(client):
    r = client.post('/login', data={
        'email': 'admin@infra.plus',
        'password': '123',
    }, follow_redirects=True)
    assert r.status_code == 200


def test_login_invalid_credentials(client):
    r = client.post('/login', data={
        'email': 'admin@infra.plus',
        'password': 'wrong',
    }, follow_redirects=True)
    assert r.status_code == 200
    assert 'Credenciais inv' in r.data.decode('utf-8') or 'tentativa' in r.data.decode('utf-8')


def test_login_open_redirect_blocked(client):
    r = client.post('/login?next=https://evil.com', data={
        'email': 'admin@infra.plus',
        'password': '123',
    }, follow_redirects=False)
    assert r.status_code in (302, 303)
    assert 'evil.com' not in (r.headers.get('Location') or '')


def test_register_page_loads(client):
    r = client.get('/cadastro')
    assert r.status_code == 200


def test_rate_limiting(client):
    from backend.app.rate_limit import login_limiter
    login_limiter.reset('127.0.0.1')
    for _ in range(6):
        client.post('/login', data={
            'email': 'nobody@test.com',
            'password': 'wrong',
        })
    r = client.post('/login', data={
        'email': 'nobody@test.com',
        'password': 'wrong',
    }, follow_redirects=True)
    assert 'Muitas tentativas' in r.data.decode('utf-8') or 'Aguarde' in r.data.decode('utf-8')
    login_limiter.reset('127.0.0.1')
