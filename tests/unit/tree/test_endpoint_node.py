import pytest
from scanapi.tree.endpoint_node import join_urls


class TestJoinUrls:
    test_data = [
        (
            "http://demo.scanapi.dev/api/",
            "health",
            "http://demo.scanapi.dev/api/health",
        ),
        (
            "http://demo.scanapi.dev/api/",
            "/health",
            "http://demo.scanapi.dev/api/health",
        ),
        (
            "http://demo.scanapi.dev/api/",
            "/health/",
            "http://demo.scanapi.dev/api/health/",
        ),
        ("http://demo.scanapi.dev/api", "health", "http://demo.scanapi.dev/api/health"),
        (
            "http://demo.scanapi.dev/api",
            "/health",
            "http://demo.scanapi.dev/api/health",
        ),
        (
            "http://demo.scanapi.dev/api",
            "/health/",
            "http://demo.scanapi.dev/api/health/",
        ),
    ]

    @pytest.mark.parametrize("url_1, url_2, expected", test_data)
    def test_build_url_properly(self, url_1, url_2, expected):
        assert join_urls(url_1, url_2) == expected
