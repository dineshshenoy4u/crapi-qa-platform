""" Resualble checks that are not tied to one endpoint"""

import httpx


def assert_response_time(response: httpx.Response, max_seconds: float) -> None:
    '''Fail if the response is longer than max_seconds'''
    elapsed = response.elapsed.total_seconds()
    request = response.request
    assert elapsed <= max_seconds, f"Request method {request.method} {request.url} took ({elapsed:.2f}s), limit is {max_seconds}"
