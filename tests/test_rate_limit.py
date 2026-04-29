from backend.app.rate_limit import RateLimiter


def test_allows_under_limit():
    rl = RateLimiter(max_attempts=3, window_seconds=60)
    assert not rl.is_rate_limited('test')
    rl.record_attempt('test')
    rl.record_attempt('test')
    assert not rl.is_rate_limited('test')


def test_blocks_over_limit():
    rl = RateLimiter(max_attempts=2, window_seconds=60)
    rl.record_attempt('test')
    rl.record_attempt('test')
    assert rl.is_rate_limited('test')


def test_reset():
    rl = RateLimiter(max_attempts=2, window_seconds=60)
    rl.record_attempt('test')
    rl.record_attempt('test')
    assert rl.is_rate_limited('test')
    rl.reset('test')
    assert not rl.is_rate_limited('test')


def test_remaining():
    rl = RateLimiter(max_attempts=3, window_seconds=60)
    assert rl.remaining_attempts('test') == 3
    rl.record_attempt('test')
    assert rl.remaining_attempts('test') == 2
