def test_admin_requires_login(client):
    r = client.get('/admin', follow_redirects=False)
    assert r.status_code in (302, 303)


def test_admin_dashboard(auth_client):
    r = auth_client.get('/admin')
    assert r.status_code == 200
    assert 'Painel' in r.data.decode('utf-8') or 'admin' in r.data.decode('utf-8').lower()


def test_admin_companies_list(auth_client):
    r = auth_client.get('/admin/terceirizadas')
    assert r.status_code == 200


def test_admin_export_csv(auth_client):
    r = auth_client.get('/admin/export.csv')
    assert r.status_code == 200
    assert r.content_type.startswith('text/csv')


def test_admin_invalid_page(auth_client):
    r = auth_client.get('/admin?page=abc')
    assert r.status_code == 200
